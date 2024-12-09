# places/management/commands/load_data.py

import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from places.models import Place, Souvenir

class Command(BaseCommand):
    help = 'Load Places and Souvenirs from data.json without setting images'

    def handle(self, *args, **options):
        # Path ke file data.json
        data_file = os.path.join(settings.BASE_DIR, 'data.json')

        if not os.path.exists(data_file):
            self.stdout.write(self.style.ERROR(f"File {data_file} tidak ditemukan."))
            return

        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        place_dict = {}

        for entry in data:
            place_name = entry.get("Place Name")
            place_description = entry.get("Description Place")
            # Field 'City', 'Description Product', 'Business Name' diabaikan sesuai permintaan

            # Menggunakan nama tempat sebagai identifier unik secara manual
            if place_name not in place_dict:
                # Cek apakah Place sudah ada
                place, created = Place.objects.get_or_create(
                    name=place_name,
                    defaults={
                        'description': place_description
                        # 'image' tidak diatur, akan menggunakan default di template
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Place: {place.name}"))
                else:
                    self.stdout.write(f"Place already exists: {place.name}")

                place_dict[place_name] = place
            else:
                place = place_dict[place_name]

            # Membuat Souvenir yang terkait
            souvenir_name = entry.get("Product Name")
            price = entry.get("Price")

            # Menentukan stok, jika tidak ada informasi, bisa diisi default, misalnya 10
            stock = 10  # Default stock

            # Menggunakan get_or_create untuk Souvenir unik per Place dan nama Souvenir
            souvenir, s_created = Souvenir.objects.get_or_create(
                place=place,
                name=souvenir_name,
                defaults={
                    'price': price,
                    'stock': stock
                    # 'image' tidak diatur, akan menggunakan default di template
                }
            )

            if s_created:
                self.stdout.write(self.style.SUCCESS(f"  Created Souvenir: {souvenir.name}"))
            else:
                self.stdout.write(f"  Souvenir already exists: {souvenir.name}")

        self.stdout.write(self.style.SUCCESS("Data loading completed successfully."))
