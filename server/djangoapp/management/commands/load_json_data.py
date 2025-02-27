import os
import json
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from djangoapp.models import CarMake, CarModel

class Command(BaseCommand):
    help = "Load initial data from JSON files into the database."

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        data_dir = os.path.join(base_dir, "cloudant", "data")  # ✅ Corrected path!

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        # Load Dealership Data (Currently not a Django model, skipping)

        # Load Car Make and Car Model Data
        for file_name in ["car_makes.json", "car_models.json"]:
            file_path = os.path.join(data_dir, file_name)
            if os.path.exists(file_path):
                with open(file_path, "r") as json_file:
                    try:
                        data = json.load(json_file)

                        if "makes" in data:  # If dealing with car makes
                            for item in data["makes"]:
                                car_make, created = CarMake.objects.get_or_create(
                                    name=item["name"],
                                    defaults={
                                        "description": item.get("description", ""),
                                        "company": item.get("company", "")
                                    }
                                )
                                self.stdout.write(self.style.SUCCESS(
                                    f"{'Created' if created else 'Updated'} CarMake: {car_make.name}"))

                        if "models" in data:  # If dealing with car models
                            for item in data["models"]:
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
                                    self.stdout.write(self.style.SUCCESS(
                                        f"{'Created' if created else 'Updated'} CarModel: {car_model.name}"))
                                else:
                                    self.stdout.write(self.style.WARNING(
                                        f"CarMake not found for {item['car_make']}, skipping model {item['name']}"))
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(f"Database IntegrityError: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error loading data from {file_name}: {e}"))
