from django.shortcuts import render
from operations import models

def index(request, element_id=None):
    line = request.GET.get('line')
    downtime_id = request.GET.get('downtime_id')
    reasons = models.line_downtime.objects.filter(line=line).all()
    downtime_reasons = [obj.reason for obj in reasons]

    if element_id == None or element_id == 1:
        html = 'htmx/index.html'
    if element_id == 2:
        html = 'htmx/downtimeForm.html'
    else:
        html = 'htmx/index.html'

    context = {
        'downtime_reasons': downtime_reasons,
        'downtime_id': downtime_id,
    }
    return render(request, html, context)
