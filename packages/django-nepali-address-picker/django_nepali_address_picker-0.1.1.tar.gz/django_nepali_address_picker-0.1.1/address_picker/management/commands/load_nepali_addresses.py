import json
import os
from django.core.management.base import BaseCommand
from address_picker.models import Province, District, Municipality, SubMetropolitan, RuralMunicipality
from django.conf import settings

class Command(BaseCommand):
    help = 'Load Nepali addresses from JSON files in the data folder.'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'data')

        # Load provinces
        with open(os.path.join(data_dir, 'provinces.json'), 'r', encoding='utf-8') as f:
            provinces_data = json.load(f)
            for province in provinces_data:
                Province.objects.get_or_create(
                    code=province['Provinces'],
                    defaults={'name': province['Name']}
                )

        # Province mapping from number to code
        province_number_to_code = {
            'Province No. 1': 'Koshi',
            'Province No. 2': 'Madhesh',
            'Province No. 3': 'Bagmati',
            'Province No. 4': 'Gandaki',
            'Province No. 5': 'Lumbini',
            'Province No. 6': 'Karnali',
            'Province No. 7': 'SudurPaschim',
        }
        # Load districts
        with open(os.path.join(data_dir, 'districts.json'), 'r', encoding='utf-8') as f:
            districts_data = json.load(f)
            for district in districts_data:
                province_value = district['Province']
                # If the value is a number mapping, convert it; otherwise, use as is
                province_code = province_number_to_code.get(province_value, province_value)
                province = Province.objects.get(code=province_code)
                District.objects.get_or_create(
                    code=district['Name'],
                    defaults={
                        'name': district['Name'],
                        'province': province
                    }
                )

        # Mapping for alternate district names to correct codes
        district_name_corrections = {
            'Pancthar': 'Panchthar',
            'Kavrepalanchowk': 'Kavrepalanchok',
            'Sindhupalchowk': 'Sindhupalchok',
            'Makawanpur': 'Makwanpur',
            'Rukum West': 'Western Rukum',
            'Dhanusa': 'Dhanusha',
            'Terathum': 'Terhathum',
            # Add more as needed
        }
        # Load municipalities
        with open(os.path.join(data_dir, 'municipalities.json'), 'r', encoding='utf-8') as f:
            municipalities_data = json.load(f)
            for municipality in municipalities_data:
                district_name = municipality['District'].strip()
                district_name = district_name_corrections.get(district_name, district_name)
                try:
                    district = District.objects.get(code__iexact=district_name)
                except District.DoesNotExist:
                    print(f"District not found for municipality: {municipality['Name']} (District: {district_name})")
                    continue
                Municipality.objects.get_or_create(
                    code=municipality['Name'],
                    defaults={
                        'name': municipality['Name'],
                        'district': district
                    }
                )

        # Load sub-metropolitans
        with open(os.path.join(data_dir, 'subMetropolitan.json'), 'r', encoding='utf-8') as f:
            sub_metropolitans_data = json.load(f)
            for sub_metropolitan in sub_metropolitans_data:
                district_name = sub_metropolitan['District'].strip()
                district_name = district_name_corrections.get(district_name, district_name)
                try:
                    district = District.objects.get(code__iexact=district_name)
                except District.DoesNotExist:
                    print(f"District not found for sub-metropolitan: {sub_metropolitan['Name']} (District: {district_name})")
                    continue
                SubMetropolitan.objects.get_or_create(
                    code=sub_metropolitan['Name'],
                    defaults={
                        'name': sub_metropolitan['Name'],
                        'district': district
                    }
                )

        # Load rural municipalities
        with open(os.path.join(data_dir, 'ruralMunicipalities.json'), 'r', encoding='utf-8') as f:
            rural_municipalities_data = json.load(f)
            for rural_municipality in rural_municipalities_data:
                district_name = rural_municipality['District'].strip()
                district_name = district_name_corrections.get(district_name, district_name)
                try:
                    district = District.objects.get(code__iexact=district_name)
                except District.DoesNotExist:
                    print(f"District not found for rural municipality: {rural_municipality['Name']} (District: {district_name})")
                    continue
                RuralMunicipality.objects.get_or_create(
                    code=rural_municipality['Name'],
                    defaults={
                        'name': rural_municipality['Name'],
                        'district': district
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded all address data')) 