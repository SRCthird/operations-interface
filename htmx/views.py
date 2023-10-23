from django.shortcuts import render, get_object_or_404
from .models import Element
from django.http import HttpResponse

def index(request, element_id=None):
    if element_id == None:
        element = get_object_or_404(Element, id=1)
    else:
        element = get_object_or_404(Element, id=element_id)
    return render(request, 'htmx/index.html', {'element': element})
