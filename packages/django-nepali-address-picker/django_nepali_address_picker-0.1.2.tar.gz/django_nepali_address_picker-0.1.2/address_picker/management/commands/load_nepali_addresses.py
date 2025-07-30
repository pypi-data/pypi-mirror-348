import json
import os
import importlib.resources
from django.core.management.base import BaseCommand
from address_picker.models import Province, District, Metropolitan, SubMetropolitan, Municipality, RuralMunicipality

class Command(BaseCommand):
    help = 'Load Nepali address data from JSON files'

    def handle(self, *args, **options):
        # Use importlib.resources to access the data folder inside the installed package
        package = 'address_picker'
        data_dir = importlib.resources.files(package) / 'data'

        # Load provinces
        with importlib.resources.open_text(package, 'data/provinces.json', encoding='utf-8') as f:
            provinces_data = json.load(f)
            for province_data in provinces_data:
                Province.objects.get_or_create(
                    id=province_data['id'],
                    defaults={
                        'name': province_data['name'],
                        'name_ne': province_data['name_ne']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded provinces'))

        # Load districts
        with importlib.resources.open_text(package, 'data/districts.json', encoding='utf-8') as f:
            districts_data = json.load(f)
            for district_data in districts_data:
                province = Province.objects.get(id=district_data['province_id'])
                District.objects.get_or_create(
                    id=district_data['id'],
                    defaults={
                        'name': district_data['name'],
                        'name_ne': district_data['name_ne'],
                        'province': province
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded districts'))

        # Load metropolitan cities
        with importlib.resources.open_text(package, 'data/metropolitan.json', encoding='utf-8') as f:
            metropolitan_data = json.load(f)
            for metro_data in metropolitan_data:
                district = District.objects.get(id=metro_data['district_id'])
                Metropolitan.objects.get_or_create(
                    id=metro_data['id'],
                    defaults={
                        'name': metro_data['name'],
                        'name_ne': metro_data['name_ne'],
                        'district': district
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded metropolitan cities'))

        # Load sub-metropolitan cities
        with importlib.resources.open_text(package, 'data/subMetropolitan.json', encoding='utf-8') as f:
            sub_metro_data = json.load(f)
            for sub_metro in sub_metro_data:
                district = District.objects.get(id=sub_metro['district_id'])
                SubMetropolitan.objects.get_or_create(
                    id=sub_metro['id'],
                    defaults={
                        'name': sub_metro['name'],
                        'name_ne': sub_metro['name_ne'],
                        'district': district
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded sub-metropolitan cities'))

        # Load municipalities
        with importlib.resources.open_text(package, 'data/municipalities.json', encoding='utf-8') as f:
            municipalities_data = json.load(f)
            for municipality_data in municipalities_data:
                district = District.objects.get(id=municipality_data['district_id'])
                Municipality.objects.get_or_create(
                    id=municipality_data['id'],
                    defaults={
                        'name': municipality_data['name'],
                        'name_ne': municipality_data['name_ne'],
                        'district': district
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded municipalities'))

        # Load rural municipalities
        with importlib.resources.open_text(package, 'data/ruralMunicipalities.json', encoding='utf-8') as f:
            rural_municipalities_data = json.load(f)
            for rural_municipality_data in rural_municipalities_data:
                district = District.objects.get(id=rural_municipality_data['district_id'])
                RuralMunicipality.objects.get_or_create(
                    id=rural_municipality_data['id'],
                    defaults={
                        'name': rural_municipality_data['name'],
                        'name_ne': rural_municipality_data['name_ne'],
                        'district': district
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded rural municipalities'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all address data')) 