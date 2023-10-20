from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.

def get_part_numbers(request):
    """
    This view pulls the finds the all materials that are part of the selected Workorder.
    @param request: The request work order.
    @return: A list of part numbers.
    """
    workorder_id = request.GET.get('workorder_id')
    if workorder_id:
        workorder_instance = workorder.objects.get(pk=workorder_id)
        catalog_num = workorder_instance.catalog_number
        
        part_numbers = catalog_material \
            .objects \
            .filter(catalog_number=catalog_num) \
            .values_list('id', 'material_name')
        
        return JsonResponse(list(part_numbers), safe=False)
    
    return JsonResponse([], safe=False)
