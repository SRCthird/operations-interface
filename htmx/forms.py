from .models import Element
from ckeditor.widgets import CKEditorWidget
from django import forms

class ElementForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Element
        fields = '__all__'