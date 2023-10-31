from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class department(models.Model):
    id = models.CharField(
        max_length=25,
        primary_key=True
    )
    name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    icon = models.TextField()

    def __str__(self):
        return self.name

class line(models.Model):
    name = models.CharField(
        max_length=255,
        primary_key=True,
        help_text="Enter the name of the line. This field must be unique."
    )
    description = models.TextField()
    department = models.ForeignKey(
        department,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name

class line_goal(models.Model):
    shift_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    id = models.AutoField(
        primary_key=True
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    shift = models.CharField(
        max_length=1,
        choices=shift_choices,
        default='A'
    )
    total_good = models.IntegerField()
    total_downtime = models.IntegerField()
    percent_reject = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.line}: {self.shift} Shift"

    class Meta:
        verbose_name = "Line Goal"
        ordering = ['line', 'shift']

class line_reject(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    reason = models.CharField(
        max_length=25
    )

    def __str__(self):
        return f"{self.line}: {self.reason}"

    class Meta:
        verbose_name = "Line Reject"

class line_downtime(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    reason = models.CharField(
        max_length=25
    )

    def __str__(self):
        return f"{self.line}: {self.reason}"

    class Meta:
        verbose_name = "Line Downtime"

class employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    department_id = models.ForeignKey(
        department,
        on_delete=models.CASCADE,
        to_field='id'
    )
    role = models.CharField(
        max_length=25
    )

    def __str__(self):
        return self.user.username

class catalog_number(models.Model):
    catalog_number = models.CharField(
        max_length=255,
        primary_key=True
    )
    description = models.CharField(
        max_length=500
    )

    def __str__(self):
        return self.catalog_number

    class Meta:
        verbose_name = "Catalog Number"

class catalog_material(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    catalog_number = models.ForeignKey(
        catalog_number,
        on_delete=models.CASCADE,
        to_field='catalog_number'
    )
    material_name = models.CharField(
        max_length=255
    )
    avg_per_unit = models.DecimalField(
        max_digits=15, decimal_places=6
    )
    unit_of_measure = models.CharField(
        max_length=25
    )

    def __str__(self):
        return f"{self.catalog_number}: {self.material_name}"

    class Meta:
        verbose_name = "Catalog Material"

class workorder(models.Model):
    status_choice = [
        ('Released', 'Released'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Rework', 'Rework'),
        ('Lot Release', 'Lot Release'),
        ('Scrapped', 'Scrapped'),
        ('Completed', 'Completed'),
    ]
    workorder = models.CharField(
        max_length=25,
        primary_key=True
    )
    lot_number = models.CharField(
        max_length=25
    )
    status = models.CharField(
        max_length=25,
        choices=status_choice,
        default='Scheduled'
    )
    catalog_number = models.ForeignKey(
        catalog_number,
        on_delete=models.CASCADE,
        to_field='catalog_number'
    )
    quantity_start = models.IntegerField()
    priority = models.IntegerField()
    scheduled_start = models.DateField()
    actual_start = models.DateField(
        null=True,
        blank=True,
        help_text="The actual start date of the workorder."
    )
    due_date = models.DateField()
    wj_printed = models.BooleanField(
        default=False
    )
    br_printed = models.BooleanField(
        default=False
    )
    labels_ordered = models.BooleanField(
        default=False
    )
    labels_received = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.workorder

class schedule(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    workorder = models.ForeignKey(
        workorder,
        on_delete=models.CASCADE,
        to_field='workorder'
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )

    def __str__(self):
        return f"{self.workorder} on {self.line}"

class material(models.Model):
    request_choice = [
        ('New Lot', 'New Lot'),
        ('New Rack', 'New Rack'),
        ('Replacement Rack', 'Replacement Rack'),
        ('Project Lot', 'Project Lot'),
    ]

    def default_time_down():
        """Get the current time + 90 minutes"""
        return timezone.now() + datetime.timedelta(minutes=90)

    id = models.AutoField(
        primary_key=True
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    request_type = models.CharField(
        max_length=25,
        choices=request_choice
    )
    workorder = models.ForeignKey(
        workorder,
        on_delete=models.CASCADE,
        to_field='workorder'
    )
    part_number = models.ForeignKey(
        catalog_material,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    line_down_at = models.DateTimeField(
        default=default_time_down
    )
    uid = models.ForeignKey(
        employee,
        on_delete=models.CASCADE
    )
    comments = models.TextField()
    delivery_status = models.CharField(
        max_length=25
    )

    def __str__(self):
        return f"{self.workorder} on {self.line}: {self.part_number} {self.quantity}"

class output(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    employee = models.ForeignKey(
        employee,
        on_delete=models.CASCADE
    )
    shift = models.CharField(
        max_length=1
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    date = models.DateTimeField()
    workorder = models.ForeignKey(
        workorder,
        on_delete=models.CASCADE,
        to_field='workorder'
    )
    start_unit = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    end_unit = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    comments = models.TextField()

class reject(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    employee = models.ForeignKey(
        employee,
        on_delete=models.CASCADE
    )
    shift = models.CharField(
        max_length=1
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    date = models.DateField()
    workorder = models.ForeignKey(
        workorder,
        on_delete=models.CASCADE,
        to_field='workorder'
    )
    quantity = models.IntegerField()
    reason = models.TextField()
    created = models.DateTimeField()

class downtime(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    line = models.ForeignKey(
        line,
        on_delete=models.CASCADE,
        to_field='name'
    )
    start_time = models.DateTimeField()
    employee_start = models.ForeignKey(
        employee,
        on_delete=models.CASCADE,
        related_name='downtime_start_set'
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True
    )
    reason = models.TextField(
        null=True,
        blank=True
    )
    comment = models.TextField(
        null=True,
        blank=True
    )
    employee_end = models.ForeignKey(
        employee,
        on_delete=models.CASCADE,
        related_name='downtime_end_set',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Downtime for {self.line} on {self.start_time}"
