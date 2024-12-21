import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from places.models import Place, Souvenir


class Command(BaseCommand):
    help = 'Load Places and Souvenirs from data.json without setting images'

    def handle(self, *args, **options):
        # Path to the data.json file
        data_file = os.path.join(settings.BASE_DIR, 'data.json')

        if not os.path.exists(data_file):
            self.stdout.write(self.style.ERROR(f"File {data_file} not found."))
            return

        with open(data_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"Error parsing {data_file}: {str(e)}"))
                return

        place_dict = {}  # To track already created places in this run
        new_places = []  # For bulk creation of new places
        new_souvenirs = []  # For bulk creation of new souvenirs

        for entry in data:
            # Extract data with defaults
            place_name = entry.get("Place Name")
            place_description = entry.get("Description Place", "No description available")
            souvenir_name = entry.get("Product Name")
            price = entry.get("Price", 0)
            stock = entry.get("Stock", 10)  # Default stock to 10 if not provided

            # Skip invalid entries
            if not place_name or not souvenir_name or price is None:
                self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {entry}"))
                continue

            # Process Place
            if place_name not in place_dict:
                place, created = Place.objects.get_or_create(
                    name=place_name,
                    defaults={
                        'description': place_description
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Place: {place.name}"))
                else:
                    self.stdout.write(f"Place already exists: {place.name}")

                place_dict[place_name] = place  # Add to tracking dictionary
            else:
                place = place_dict[place_name]

            # Process Souvenir
            if not Souvenir.objects.filter(place=place, name=souvenir_name).exists():
                new_souvenirs.append(
                    Souvenir(
                        place=place,
                        name=souvenir_name,
                        price=price,
                        stock=stock
                    )
                )
            else:
                self.stdout.write(f"Souvenir already exists: {souvenir_name}")

        # Bulk create souvenirs
        if new_souvenirs:
            Souvenir.objects.bulk_create(new_souvenirs)
            self.stdout.write(self.style.SUCCESS(f"Created {len(new_souvenirs)} new souvenirs."))

        self.stdout.write(self.style.SUCCESS("Data loading completed successfully."))
