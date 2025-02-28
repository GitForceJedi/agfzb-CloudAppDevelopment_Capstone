from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
import logging
import random
from .models import CarMake, CarModel, DealerReview, CarDealer  # ✅ Using Django DB models

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ✅ Static Template View (Prevents AttributeError)
def static_template_view(request):
    return render(request, 'djangoapp/static_template.html')

# ✅ About View
def about(request):
    return render(request, 'djangoapp/about.html')

# ✅ Contact View
def contact(request):
    return render(request, 'djangoapp/contact.html')

# ✅ Login View
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/login.html', {"message": "Invalid username or password."})
    return render(request, 'djangoapp/login.html')

# ✅ Logout View
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# ✅ Registration View
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        if User.objects.filter(username=username).exists():
            return render(request, 'djangoapp/registration.html', {"message": "User already exists."})
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        login(request, user)
        return redirect("djangoapp:index")
    return render(request, 'djangoapp/registration.html')

# ✅ Signup View (Restored!)
def signup(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        if User.objects.filter(username=username).exists():
            return render(request, 'djangoapp/signup.html', {"message": "User already exists."})
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        login(request, user)
        return redirect("djangoapp:index")
    return render(request, 'djangoapp/signup.html')

# ✅ Fetch dealerships from Django DB (Replacing Cloudant)
def get_dealers_from_cf():
    return CarDealer.objects.all()  # ✅ Fetch directly from Django DB

# ✅ Get all dealerships and render index page
def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_dealers_from_cf()  # ✅ Still using `from_cf` function
        return render(request, 'djangoapp/index.html', {'dealership_list': dealerships})

# ✅ Fetch dealer details by ID
def get_dealer_by_id_from_cf(dealer_id):
    return get_object_or_404(CarDealer, id=dealer_id)  # ✅ Fetch from Django DB

# ✅ Get dealer details (fetching reviews from Django DB)
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        dealer = get_dealer_by_id_from_cf(dealer_id)  # ✅ Fetch dealer details
        reviews = get_dealer_reviews_from_cf(dealer_id)  # ✅ Fetch reviews
        return render(request, 'djangoapp/dealer_details.html', {'dealer': dealer, 'dealer_reviews': reviews})

# ✅ Fetch dealer reviews from Django DB (Replacing Cloudant)
def get_dealer_reviews_from_cf(dealer_id):
    return DealerReview.objects.filter(dealership=dealer_id)  # ✅ Fetch reviews from DB

# ✅ Get dealership by ID (Using from_cf function)
def dealer_by_id_view(request, dealer_id):
    if request.method == "GET":
        dealer = get_dealer_by_id_from_cf(dealer_id)  # ✅ Keeps function call the same
        return JsonResponse({"id": dealer.id, "name": dealer.name, "description": dealer.description})

# ✅ Get dealerships by state (Replacing API call with Django DB)
def get_dealer_by_state_from_cf(state):
    return CarDealer.objects.filter(state=state)  # ✅ Fetch from Django DB

# ✅ Get dealers by state
def dealers_by_state_view(request, state):
    if request.method == "GET":
        dealerships = get_dealer_by_state_from_cf(state)  # ✅ Keeps function call the same
        return JsonResponse([{"id": dealer.id, "name": dealer.name} for dealer in dealerships], safe=False)

# ✅ Add a Review
@login_required
def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)  # ✅ Fetch cars for this dealer
        return render(request, "djangoapp/add_review.html", {"cars": cars, "dealer_id": dealer_id})

    elif request.method == "POST":
        try:
            selected_car = get_object_or_404(CarModel, id=request.POST.get('car'))
            review = DealerReview.objects.create(
                dealership=dealer_id,
                name=request.user.get_full_name(),
                review=request.POST.get('content', ''),
                purchase=request.POST.get('purchasecheck', False),
                purchase_date=request.POST.get('purchasedate', ''),
                car_make=selected_car.car_make.name,
                car_model=selected_car.name,
                car_year=selected_car.year.strftime("%Y")
            )
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return HttpResponse("Method not allowed", status=405)
