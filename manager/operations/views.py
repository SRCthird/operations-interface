from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.

def get_part_numbers(request):
    id_workorder = request.GET.get('id_workorder')
    if id_workorder:
        part_numbers = catalog_material.objects.filter(
            catalog_number__workorder__id=id_workorder
        ).values_list('id', 'material_name')
        return JsonResponse(list(part_numbers), safe=False)
    return JsonResponse([], safe=False)
