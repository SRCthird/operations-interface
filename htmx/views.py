from django.shortcuts import get_object_or_404, render
from operations import models


def downtimeForm(request, id):
    downtime_record = get_object_or_404(models.downtime, id=id)

    reasons = models.line_downtime \
        .objects \
        .filter(
            line=downtime_record.line
        ) \
        .all()

    downtime_reasons = [obj.reason for obj in reasons]

    content = {
        'title': 'Downtime Form',
        'downtime_reasons': downtime_reasons,
        'downtime_id': id,
    }
    return render(request, 'htmx/downtimeForm.html', content)


def outputForm(request, line, shift):

    workorder_obj = models.schedule \
        .objects \
        .filter(
            line=line,
            status='In-Process'
        ) \
        .first() \

    try:
        workorder = workorder_obj.workorder
        start_unit = models.output \
             .objects \
             .filter(workorder=workorder.workorder) \
             .order_by("-date") \
             .first() \
             .end_unit
        start_unit += 1
    except Exception as e:
        print("Error:", e)
        workorder = ""
        start_unit = 1

    content = {
        'title': 'Hourly Output Form',
        'shift': shift,
        'line': line,
        'workorder': workorder,
        'start_unit': start_unit,
    }

    return render(request, 'htmx/outputForm.html', content)


def rejectForm(request, line, shift):

    reasons = models.line_reject \
        .objects \
        .filter(
            line=line
        ) \
        .all()
    print(reasons)
    reject_reasons = [obj.reason for obj in reasons]

    content = {
        'title': 'Reject Form',
        'line': line,
        'shift': shift,
        'reject_reasons': reject_reasons,
    }
    return render(request, 'htmx/rejectForm.html', content)
