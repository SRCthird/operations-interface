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


def outputForm(request, line):

    pass


def rejectForm(request, line):

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
        'reject_reasons': reject_reasons,
    }
    return render(request, 'htmx/rejectForm.html', content)
