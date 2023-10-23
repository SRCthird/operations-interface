from django import forms
from . import models

class MaterialAdminForm(forms.ModelForm):
    class Meta:
        model = models.material
        fields = '__all__'
        widgets = {
            'line_down_at': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }
        
    class Media:
        js = ('operations/js/dynamic_updates.js',)
