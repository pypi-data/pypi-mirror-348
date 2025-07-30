from django import forms
from .models import Province, District, Municipality, SubMetropolitan, RuralMunicipality

class NepaliAddressForm(forms.Form):
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label='Province',
        empty_label='Select Province',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.none(),
        label='District',
        empty_label='Select District',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    local_body = forms.ChoiceField(
        label='Local Body',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(province_id=province_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get('province'):
            province_id = self.initial.get('province').id
            self.fields['district'].queryset = District.objects.filter(province_id=province_id)
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                municipalities = Municipality.objects.filter(district_id=district_id)
                submetros = SubMetropolitan.objects.filter(district_id=district_id)
                rurals = RuralMunicipality.objects.filter(district_id=district_id)
                choices = [(f"municipality-{m.id}", m.name) for m in municipalities]
                choices += [(f"submetro-{s.id}", s.name) for s in submetros]
                choices += [(f"rural-{r.id}", r.name) for r in rurals]
                self.fields['local_body'].choices = [('', 'Select Local Body')] + choices
            except (ValueError, TypeError):
                pass 