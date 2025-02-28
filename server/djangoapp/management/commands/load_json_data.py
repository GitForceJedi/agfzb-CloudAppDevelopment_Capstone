import os
import json
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from djangoapp.models import CarMake, CarModel  # Ensure models are correctly imported

class Command(BaseCommand):
    help = "Load dealership and review data from JSON into the database."

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        data_dir = os.path.join(base_dir, "cloudant", "data")  # ✅ Corrected path!

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        # ✅ Load Dealership Data
        dealership_file = os.path.join(data_dir, "dealerships.json")
        if os.path.exists(dealership_file):
            with open(dealership_file, "r") as json_file:
                try:
                    dealerships = json.load(json_file).get("dealerships", [])
                    for dealer in dealerships:
                        # No Django model for dealership, skipping database insert
                        self.stdout.write(self.style.SUCCESS(f"Loaded dealership: {dealer['full_name']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading dealerships: {e}"))

        # ✅ Load Car Makes & Models
        car_make_file = os.path.join(data_dir, "car_makes.json")
        car_model_file = os.path.join(data_dir, "car_models.json")

        if os.path.exists(car_make_file):
            with open(car_make_file, "r") as json_file:
                try:
                    data = json.load(json_file).get("makes", [])
                    for item in data:
                        car_make, created = CarMake.objects.get_or_create(
                            name=item["name"],
                            defaults={"description": item.get("description", ""), "company": item.get("company", "")}
                        )
                        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} CarMake: {car_make.name}"))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Database IntegrityError: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading car makes: {e}"))

        if os.path.exists(car_model_file):
            with open(car_model_file, "r") as json_file:
                try:
                    data = json.load(json_file).get("models", [])
                    for item in data:
                        car_make = CarMake.objects.filter(name=item["car_make"]).first()
                        if car_make:
                            car_model, created = CarModel.objects.get_or_create(
                                car_make=car_make,
                                name=item["name"],
                                defaults={
                                    "dealer_id": item["dealer_id"],
                                    "car_type": item["car_type"],
                                    "year": item["year"],
                                    "color": item["color"],
                                    "doors": item["doors"],
                                    "average_rating": item["average_rating"]
                                }
                            )
                            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} CarModel: {car_model.name}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"CarMake not found for {item['car_make']}, skipping model {item['name']}"))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Database IntegrityError: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading car models: {e}"))

        # ✅ Load Reviews Data
        reviews_file = os.path.join(data_dir, "reviews.json")
        if os.path.exists(reviews_file):
            with open(reviews_file, "r") as json_file:
                try:
                    reviews = json.load(json_file).get("reviews", [])
                    for review in reviews:
                        self.stdout.write(self.style.SUCCESS(f"Loaded review: {review['name']} - {review['review']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading reviews: {e}"))
