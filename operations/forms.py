import datetime
from django import forms
from . import models

class MaterialAdminForm(forms.ModelForm):
    class Meta:
        model = models.material
        fields = '__all__'
        
    class Media:
        js = ('operations/js/dynamic_updates.js',)
    
