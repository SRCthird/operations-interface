import datetime
from django import forms
from . import models


class MaterialAdminForm(forms.ModelForm):
    class Meta:
        model = models.material
        fields = '__all__'

    class Media:
        js = ('operations/js/dynamic_updates.js',)


class LineForm(forms.Form):
    line_choices = [(i.name, i.name) for i in models.line.objects.all()]
    current_line = forms.ChoiceField(
        choices=line_choices,
        label='What line are you on?'
    )
    save_line = forms.BooleanField(
        label='Would you like to save this line as this PCs default?',
        required=False
    )
