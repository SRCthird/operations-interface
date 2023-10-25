import os
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from . import models
import requests

# Create your views here.
def index(request):
    return render(request, 'operations/index.html')

def get_part_numbers(request):
    """
    This view pulls the finds the all materials that are part of the selected Workorder.
    @param request: The request work order.
    @return: A list of part numbers.
    """
    workorder_id = request.GET.get('workorder_id')
    if workorder_id:
        workorder_instance = models.workorder.objects.get(pk=workorder_id)
        catalog_num = workorder_instance.catalog_number
        
        part_numbers = models.catalog_material \
            .objects \
            .filter(catalog_number=catalog_num) \
            .values_list('id', 'material_name')
        
        return JsonResponse(list(part_numbers), safe=False)
    
    return JsonResponse([], safe=False)

def user_info(request_or_token):
    """
    Get user info from Microsoft Graph
    :param request_or_token: Django request object or a direct access token string
    :return: User info in JSON format or an error response
    """
    # If the function is called with a Django HttpRequest object
    if isinstance(request_or_token, HttpRequest):
        access_token = request_or_token.GET.get('access_token', None)
        if not access_token:
            return HttpResponseBadRequest("access_token parameter is required")
    else:
        # If the function is called with a string token
        access_token = request_or_token

    url = "https://graph.microsoft.com/beta/me"
    
    headers = {
        'Authorization': f"Bearer {access_token}",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # If called with HttpRequest, return JsonResponse
        if isinstance(request_or_token, HttpRequest):
            return JsonResponse(response.json())
        # If called as a normal function, return the dict
        return response.json()
    except requests.HTTPError as e:
        error_msg = f"Error fetching data from Microsoft Graph: {e}"
        # If called with HttpRequest, return HttpResponseServerError
        if isinstance(request_or_token, HttpRequest):
            return HttpResponseServerError(error_msg)
        # If called as a normal function, raise the exception
        raise requests.HTTPError(error_msg)

@csrf_exempt
def user_photo(request):
    """
    Get user profile picture from Microsoft Graph
    :param request: Django request object
    :return: location of user profile picture or an error response
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Method Not Allowed

    token = request.POST.get('access_token', None)
    if not token:
        return HttpResponseBadRequest('Token not provided')

    try:
        user = user_info(token)

        profile_image_url = 'https://graph.microsoft.com/v1.0/me/photo/$value'
        target_directory = 'operations/static/profiles'
        target_file_path = os.path.join(target_directory, f"{user['mailNickname']}.jpeg")

        if not os.path.exists(target_directory):
            os.makedirs(target_directory, exist_ok=True)

        response = requests.get(profile_image_url, headers={'Authorization': f'Bearer {token}'}, stream=True)

        if response.status_code == 200:
            with open(target_file_path, 'wb') as file:
                for chunk in response.iter_content(8192):
                    file.write(chunk)

            return JsonResponse({'url': f'/static/profile/{user["mailNickname"]}.jpeg'}, status=200)

        else:
            return HttpResponseServerError('Error fetching image')

    except Exception as e:
        return HttpResponseServerError(str(e))

def demo(request):
    return render(request, 'operations/demo.html')

def _404(request, exception="The requested page could not be found."):
    """404 view, for pages that aren't implemented yet or don't exsist."""
    context = {
        'exception': str(exception)
    }
    return render(request, 'operations/404.html', context, status=404)

class MaterialListView(ListView):
    model = models.material
    template_name = 'operations/material_list.html'

class MaterialUpdateView(UpdateView):
    model = models.material
    fields = ['line', 'request_type', 'workorder', 'part_number', 'quantity', 'line_down_at', 'uid', 'comments', 'delivery_status']
    template_name = 'operations/material_form.html'
    success_url = reverse_lazy('material_list')

class MaterialCreateView(CreateView):
    model = models.material
    fields = ['line', 'request_type', 'workorder', 'part_number', 'quantity', 'line_down_at', 'uid', 'comments', 'delivery_status']
    template_name = 'operations/material_form.html'
    success_url = reverse_lazy('material_list')

class MaterialDeleteView(DeleteView):
    model = models.material
    template_name = 'operations/material_confirm_delete.html'
    success_url = reverse_lazy('material_list')