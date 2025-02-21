from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    # Methods
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    # Many-to-One relationship to CarMake model
    car_make = models.ForeignKey('CarMake', on_delete=models.CASCADE)
    # Fields
    name = models.CharField(max_length=255)
    dealer_id = models.CharField(max_length=50)  # Assuming dealer_id is a string
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Truck'),
        # Add more choices as needed
    ]
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    color = models.CharField(max_length=255)
    doors = models.IntegerField()
    average_rating = models.FloatField()
    # Methods
    def __str__(self):
        return f"{self.car_make.name} - {self.name}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self):
        return f"Dealer: {self.short_name} Address: {self.address}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
# In models.py
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.review_id = id

    def __str__(self):
        return f"Review by {self.name} for Dealership: {self.dealership} Review: {self.review} Sentiment: {self.sentiment}"

#class DealerReview(models.Model):
 #   dealership = models.CharField(max_length=255)
  #  name = models.CharField(max_length=255)
   # purchase = models.BooleanField(default=False)
    #review = models.TextField()
    #purchase_date = models.DateField()
   #car_make = models.CharField(max_length=255)
    #car_model = models.CharField(max_length=255)
    #car_year = models.IntegerField()
    #sentiment = models.CharField(max_length=20)  # Assuming sentiment is a string, you can adjust the max_length
    #review_id = models.CharField(max_length=50, unique=True)

    #def __str__(self):
    #    return f"Review by {self.name} for {self.dealership} - {self.review}"


class CarReview:
    def __init__(self, review_id, name, dealership, review_text, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.review_id = review_id
        self.name = name
        self.dealership = dealership
        self.review_text = review_text
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return f"Review by {self.name} - {self.review_text}"