from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Avg, F, Sum, ExpressionWrapper, fields
from operations import models
from datetime import timedelta

def line_view(request, pk, shift):
    """
    A Basic dashboard of the given line.
    :param pk: The primary key of the line being displayed.
    :param shift: the name of the shift being displayed.
    :return: The rendered dashboard.

    :test1: INSERT INTO operations_output (shift, date, comments, employee, line, workorder, start_unit, end_unit)
            VALUES ('B', now(), 'Ran perfectly', 1, 'Demo', 'WJ4012346', 0401, 0001);
    :test2: INSERT INTO operations_reject (shift, date, quantity, reason, created, employee_id, line_id, workorder_id)
            VALUES ('B', now(), 2, 'Step Seam', now(), 1, 'Demo', 'WJ4012346');
    :test3: INSERT INTO operations_downtime (start_time, employee_start_id, line_id)
            VALUES (now(), 1, 'Demo');
    :test4: UPDATE operations_downtime SET 
            end_time = now(), employee_end_id = 1, reason = 'Down for Maintenance', comments = 'This is a demonstation' 
            WHERE id = 1;
    """
    today = timezone.now().date()
    line = get_object_or_404(models.line, pk=pk)
    
    goal = get_object_or_404(models.line_goal, line=line, shift=shift)
    goal_value = goal.total_good / 8 
    
    unit_entries = models.output.objects \
        .filter(line=line, date__date=today) \
        .annotate( 
            actual_good=ExpressionWrapper(
                F('end_unit') - F('start_unit'),
                output_field=fields.IntegerField()
            )
        )
    
    downtime_entries = models.downtime.objects \
        .filter(line=line, start_time__date=today) \
        .annotate( 
            time_difference=ExpressionWrapper(
                F('end_time') - F('start_time'),
                output_field=fields.DurationField()
            )
        ) \
        .order_by('-start_time')
    
    last_downtime_entry = downtime_entries.first()
    currently_down = last_downtime_entry is not None and last_downtime_entry.end_time is None
    downtime_id = last_downtime_entry if last_downtime_entry is not None else -1

    #currently_down = True

    reject_entries = models.reject.objects \
        .filter(
            line=line, 
            shift=shift, 
            date=today
        )

    total_reject = reject_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
    avg_units = unit_entries.aggregate(average_difference=Avg(F('end_unit') - F('start_unit')))['average_difference'] or 0
    total_units = unit_entries.aggregate(Sum('actual_good'))['actual_good__sum'] or 0
    total_downtime = downtime_entries.aggregate(total_downtime=Sum('time_difference'))['total_downtime'] or timedelta(seconds=0)

    context = {
        'line': line,
        'shift': shift,
        'goal': goal_value,
        'total_units': total_units,
        'avg_units': avg_units,
        'total_reject': total_reject,
        'total_downtime': total_downtime,
        'currently_down': currently_down,
        'downtime_id': downtime_id,
        'unit_entries': unit_entries,
        'downtime_entries': downtime_entries,
    }

    return render(request, 'line_management/line.html', context)
