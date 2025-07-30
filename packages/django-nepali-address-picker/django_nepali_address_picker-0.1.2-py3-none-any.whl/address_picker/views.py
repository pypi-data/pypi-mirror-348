from django.shortcuts import render
from django.http import JsonResponse
from .forms import NepaliAddressForm
from .models import District, Municipality, SubMetropolitan, RuralMunicipality

def address_picker(request):
    form = NepaliAddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # You can handle the submitted data here
        pass
    return render(request, 'address_picker/address_picker.html', {'form': form})

def load_districts(request):
    province_id = request.GET.get('province')
    districts = District.objects.filter(province_id=province_id).order_by('name')
    return JsonResponse(list(districts.values('id', 'name')), safe=False)

def load_local_bodies(request):
    district_id = request.GET.get('district')
    municipalities = Municipality.objects.filter(district_id=district_id)
    submetros = SubMetropolitan.objects.filter(district_id=district_id)
    rurals = RuralMunicipality.objects.filter(district_id=district_id)
    data = [
        {'id': f'municipality-{m.id}', 'name': m.name, 'type': 'Municipality'} for m in municipalities
    ] + [
        {'id': f'submetro-{s.id}', 'name': s.name, 'type': 'SubMetropolitan'} for s in submetros
    ] + [
        {'id': f'rural-{r.id}', 'name': r.name, 'type': 'RuralMunicipality'} for r in rurals
    ]
    return JsonResponse(data, safe=False)
 