from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
import logging
import random
from .models import CarMake, CarModel, DealerReview  # ✅ Fetch data from Django instead of Cloudant

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    if request.method == 'POST':
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

# ✅ Get all dealerships from the Django database
def get_dealerships(request):
    if request.method == "GET":
        dealerships = CarMake.objects.all()  # ✅ Fetch from Django DB instead of API
        return render(request, 'djangoapp/index.html', {'dealership_list': dealerships})

# ✅ Get dealer details (fetching reviews from Django DB)
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        reviews = DealerReview.objects.filter(dealership=dealer_id)  # ✅ Fetch from Django DB
        dealer = get_object_or_404(CarMake, id=dealer_id)  # Fetch dealer details
        return render(request, 'djangoapp/dealer_details.html', {'dealer': dealer, 'dealer_reviews': reviews})

# ✅ Get dealership by ID
def dealer_by_id_view(request, dealer_id):
    if request.method == "GET":
        dealer = get_object_or_404(CarMake, id=dealer_id)  # ✅ Fetch from Django DB
        return JsonResponse({"id": dealer.id, "name": dealer.name, "description": dealer.description})

# ✅ Get dealerships by state
def dealers_by_state_view(request, state):
    if request.method == "GET":
        dealerships = CarMake.objects.filter(company=state)  # ✅ Assuming state is stored in `company`
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
