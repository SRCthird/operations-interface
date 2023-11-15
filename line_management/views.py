from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F, Sum, ExpressionWrapper, fields, Func, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.db import connection

from operations import models
from . import forms


class TimeDiff(Func):
    """Returns the difference of two DateTimes in dd:mm:ss.ms format"""
    function = 'TIMEDIFF'
    output_field = fields.CharField()


class TimeFormat(Func):
    """
    Formats the given DateTime
    :param ExpressionWrapper: {optional} The expression to be formatted.
    :param format: The format to be used. I.E. django.db.models.Value('%H:%i')

    :return: The formatted DateTime
    """
    function = 'TIME_FORMAT'
    output_field = fields.CharField()


class TimeDiffSeconds(Func):
    """Returns the difference of two DateTimes in seconds"""
    function = 'TIMESTAMPDIFF'
    template = '%(function)s(SECOND, %(expressions)s)'
    output_field = fields.IntegerField()


@login_required
def line_view(request, pk, shift):
    """
    A Basic dashboard of the given line.
    :param pk: The primary key of the line being displayed.
    :param shift: the name of the shift being displayed.
    :return: The rendered dashboard.

    :test1: INSERT INTO operations_output (shift, date, comments, employee_id, line_id, workorder_id, start_unit, end_unit)
            VALUES ('B', now(), 'Ran perfectly', 1, 'Demo', 'WJ4012346', 0001, 0401);
    :test2: INSERT INTO operations_reject (shift, date, quantity, reason, created, employee_id, line_id, workorder_id)
            VALUES ('B', now(), 2, 'Step Seam', now(), 1, 'Demo', 'WJ4012346');
    :test3: INSERT INTO operations_downtime (start_time, employee_start_id, line_id)
            VALUES (now(), 1, 'Demo');
    :test4: UPDATE operations_downtime SET
            end_time = now(), employee_end_id = 1, reason = 'Down for Maintenance', comments = 'This is a demonstation' 
            WHERE id = 1;
    """

    # Initializing variables
    today = timezone.now().date()
    line = get_object_or_404(models.line, pk=pk)
    goal = get_object_or_404(models.line_goal, line=line, shift=shift)
    goal_value = goal.total_good / 8

    # Getting all data from output table and appending end_unit-start_unit + 1
    outputs = models.output.objects \
        .filter(
            line=line,
            date__date=today
        ) \
        .annotate(
            total_good=Coalesce(
                F('end_unit') - F('start_unit') + Value(1),
                Value(0)
            )
        ) \
        .order_by('date')

    # Initialize loop variables
    actual_total = []
    last_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for output in outputs:
        # Define new variables at the start of loop
        current_time = output.date

        # Get the number of good units in the line between this entry and last
        current_reject = models.reject.objects \
            .filter(
                date__gt=last_time,
                date__lte=current_time,
                line_id=line
            ) \
            .aggregate(
                total_reject=Coalesce(Sum('quantity'), Value(0))
            )['total_reject']

        # actual good is total made - rejected units
        actual_total_good = output.total_good - current_reject

        employee = f"{output.employee}"

        # Append to actual_total
        actual_total.append({
            'date': output.date,
            'id': output.id,
            'employee': employee.upper(),
            'workorder': output.workorder,
            'actual_total_good': actual_total_good,
            'current_reject': current_reject,
            'start_unit': output.start_unit,
            'end_unit': output.end_unit,
            'comments': output.comments,
        })

        # Save this time as last time
        last_time = current_time

    actual_good_sum = sum(row['actual_total_good'] for row in actual_total)

    # Calculate the avg or return 0
    try:
        avg_units = round(actual_good_sum / len(actual_total))
    except ZeroDivisionError:
        avg_units = 0

    # Get the last downtime entry of the current line
    last_entry = models.downtime.objects \
        .filter(line=line) \
        .annotate(
            time_difference=TimeFormat(
                ExpressionWrapper(  # Return the difference in DateTime
                    Func(F('end_time'), F('start_time'), function='TIMEDIFF'),
                    output_field=fields.CharField()
                ),
                Value('%H:%i')
            )
        ) \
        .annotate(
            time_difference_seconds=TimeDiffSeconds(
                F('start_time'),  # Return the difference in seconds
                F('end_time')
            )
        ) \
        .order_by('-start_time') \
        .first()

    # Get all downtime entries of the current line and day
    downtime_entries = models.downtime.objects \
        .filter(line=line, start_time__date=today) \
        .annotate(
            time_difference=TimeFormat(
                ExpressionWrapper(  # Return the difference in DateTime
                    Func(F('end_time'), F('start_time'), function='TIMEDIFF'),
                    output_field=fields.CharField()
                ),
                Value('%H:%i')
            )
        ) \
        .annotate(
            time_difference_seconds=TimeDiffSeconds(
                F('start_time'),  # Return the difference in seconds
                F('end_time')
            )
        ) \
        .order_by('-start_time')

    # If there are no downtime entries for today, then always display at least 1 entry
    if not downtime_entries.exists():
        if last_entry:
            downtime_entries = last_entry
        last_downtime_entry = last_entry
    else:
        last_downtime_entry = downtime_entries.first()

    # Verify if the machine is currently down
    currently_down = last_downtime_entry is not None and last_downtime_entry.end_time is None

    try:
        downtime_id = last_downtime_entry.id
    except Exception as e:
        downtime_id = -1
        print(e)

    # Get all reject entries of this shift, line and day
    reject_entries = models.reject.objects \
        .filter(
            line=line,
            shift=shift,
            date__gt=today
        )

    # Get the sum of all reject entries
    total_reject = reject_entries.aggregate(
        Sum('quantity'))['quantity__sum'] or 0

    # Calculate the total downtime or return 0
    try:
        total_seconds = downtime_entries.aggregate(total_downtime=Sum(
            'time_difference_seconds'))['total_downtime'] or 0
    except Exception as e:
        print(e)
        total_seconds = 0
        downtime_entries = []

    if total_seconds is not None:
        # Convert seconds to hh:mm format
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        total_time_str = "{:02}:{:02}".format(int(hours), int(minutes))
    else:
        total_time_str = "00:00"

    context = {
        'line': line,
        'shift': shift,
        'goal': goal_value,
        'total_units': actual_good_sum,
        'avg_units': avg_units,
        'total_reject': total_reject,
        'total_downtime': total_time_str,
        'currently_down': currently_down,
        'downtime_id': downtime_id,
        'actual_total': actual_total,
        'downtime_entries': downtime_entries,
    }

    return render(request, 'line_management/line.html', context)


def create_downtime(request):
    """
    Creates a new downtime entry.
    :param request: The body of the POST request.
    :return: A JSON response with the status of the request.
    """
    if request.method == 'POST':
        form = forms.DowntimeCreateForm(request.POST)
        if form.is_valid():
            downtime = models.downtime()
            downtime.start_time = timezone.now()
            downtime.line = get_object_or_404(
                models.line, pk=form.cleaned_data['line'])

            username = form.cleaned_data['employee']
            employee = get_object_or_404(
                models.employee, user__username=username)

            downtime.employee_start_id = employee.id
            downtime.save()
            return JsonResponse({'status': 'success'})
        else:
            print(form.errors)
    return JsonResponse({'status': 'failed'})


def update_downtime(request, downtime_id):
    """
    Updates the current downtime entry.
    :param request: The body of the POST request.
    :param downtime_id: The primary key of the downtime entry being updated.
    :return: A JSON response with the status of the request.
    """
    if request.method == 'POST':
        form = forms.DowntimeUpdateForm(request.POST)
        if form.is_valid():
            downtime = models.downtime.objects.get(
                pk=downtime_id, end_time__isnull=True)
            downtime.end_time = timezone.now()

            username = form.cleaned_data['employee']
            employee_obj = get_object_or_404(
                models.employee, user__username=username)
            downtime.employee_end_id = employee_obj.id

            downtime.reason = form.cleaned_data['reason']
            downtime.comment = form.cleaned_data['comments']
            downtime.save()
            return JsonResponse({'status': 'success'})
        else:
            print(form.errors)
    return JsonResponse({'status': 'failed'})


def create_reject(request):
    """
    Creates a new reject entry.
    :param request: The body of the POST request.
    :return: A JSON response with the status of the request.
    """
    if request.method == 'POST':
        data = request.POST
        employee_str = data.get('employee')
        try:
            line = get_object_or_404(models.line, name=data.get('line'))
            workorder = get_object_or_404(
                models.workorder, workorder=data.get('workorder'))
            employee = get_object_or_404(
                models.employee, user__username=employee_str)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})

        reject = models.reject(
            employee=employee,
            shift=data.get('shift'),
            line=line,
            date=timezone.now(),
            workorder=workorder,
            quantity=data.get('quantity'),
            reason=data.get('reason')
        )

        try:
            reject.full_clean()
            reject.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})


def create_output(request):
    """
    Creates a new output entry.
    :param request: The body of the POST request.
    :return: A JSON response with the status of the request.
    """
    if request.method == 'POST':
        data = request.POST
        employee_str = data.get('employee')
        try:
            line = get_object_or_404(models.line, name=data.get('line'))
            workorder = get_object_or_404(
                models.workorder, workorder=data.get('workorder'))
            employee = get_object_or_404(
                models.employee, user__username=employee_str)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})

        output = models.output(
            employee=employee,
            shift=data.get('shift'),
            line=line,
            date=timezone.now(),
            workorder=workorder,
            start_unit=data.get('start_unit'),
            end_unit=data.get('end_unit'),
            safety=data.get('safety'),
            quality=data.get('quality'),
            comments=data.get('comments')
        )

        try:
            output.full_clean()
            output.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})
