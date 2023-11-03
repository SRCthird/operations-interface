from django.shortcuts import get_object_or_404, render
from operations import models


def downtimeForm(request, id):
    downtime_record = get_object_or_404(models.downtime, id=id)

    reasons = models.line_downtime.objects \
        .filter(
            line = downtime_record.line
        ) \
        .all()

    downtime_reasons = [obj.reason for obj in reasons]

    content = {
        'downtime_reasons': downtime_reasons,
        'downtime_id': id,
    }
    return render(request, 'htmx/downtimeForm.html', content)


