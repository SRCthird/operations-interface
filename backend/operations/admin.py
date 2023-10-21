from manager import settings
from django.contrib import admin
from django.db.models import Sum
from django.utils.dateformat import DateFormat
from .models import *

admin.AdminSite.site_header = settings.OPERATIONS_ADMIN_HEADER
admin.AdminSite.site_title = settings.OPERATIONS_ADMIN_TITLE
admin.AdminSite.index_title = settings.OPERATIONS_ADMIN_INDEX_TITLE

# Register your models here.        
@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'icon')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')

    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'description', 'icon')
        }),
    )

@admin.register(employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_id', 'role')
    list_filter = ('user', 'department_id', 'role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Additional Information', {
            'fields': ('department_id', 'role')
        }),
    )

@admin.register(line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'department')
    list_filter = ('name', 'description', 'department')
    search_fields = ('name', 'description', 'department__name')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'department')
        }),
    )

@admin.register(line_goal)
class LineGoalAdmin(admin.ModelAdmin):
    list_display = ('line', 'shift', 'total_good', 'total_downtime', 'percent_reject')
    list_filter = ('line', 'shift')
    search_fields = ('line__name','shift')

    fieldsets = (
        ('Line information', {
            'fields': ('line','shift') 
        }),
        ('Line statistics', {
            'fields': ('total_good', 'total_downtime', 'percent_reject')
        }),
    )

@admin.register(line_reject)
class LineRejectAdmin(admin.ModelAdmin):
    list_display = ('line', 'reason')
    list_filter = ('line','reason')
    search_fields = ('line__name','reason')

    fieldsets = (
        ('Line information', {
            'fields': ('line','reason') 
        }),
    )

@admin.register(line_downtime)
class LineDowntimeAdmin(admin.ModelAdmin):
    list_display = ('line','reason')
    list_filter = ('line','reason')
    search_fields = ('line__name','reason')

    fieldsets = (
        ('Line information', {
            'fields': ('line','reason') 
        }),
    )

@admin.register(catalog_number)
class CatalogNumberAdmin(admin.ModelAdmin):
    list_display = ('catalog_number', 'description')
    list_filter = ('catalog_number',)
    search_fields = ('catalog_number', 'description')

    fieldsets = (
        ('Catalog Number Information', {
            'fields': ('catalog_number', 'description')
        }),
    )

@admin.register(catalog_material)
class CatalogMaterialAdmin(admin.ModelAdmin):
    list_display = ('catalog_number', 'material_name', 'avg_per_unit', 'unit_of_measure')
    list_filter = ('catalog_number', 'material_name')
    search_fields = ('catalog_material', 'material_name', 'unit_of_measure')

    fieldsets = (
        ('Catalog Number Information', {
            'fields': ('catalog_number', 'material_name', 'avg_per_unit', 'unit_of_measure')
        }),
    )

@admin.register(workorder)
class WorkorderAdmin(admin.ModelAdmin):
    list_display = ('workorder', 'lot_number', 'status', 'catalog_number', 'quantity_start', 'sum_quantity_output', 'priority', 'scheduled_start_dd_mm_yy', 'due_date_dd_mm_yy', 'actual_start_dd_mm_yy', 'wj_printed', 'br_printed', 'labels_ordered', 'labels_received')
    list_filter = ('workorder', 'lot_number', 'status', 'catalog_number', 'priority', 'scheduled_start', 'due_date')
    search_fields = ('workorder', 'lot_number', 'status', 'catalog_number', 'priority','scheduled_start', 'due_date')

    ordering = ['status', 'due_date']

    fieldsets = (
        ('Workorder Information', {
            'fields': ('workorder', 'lot_number', 'catalog_number'),
        }),
        ('Workorder Statistics', {
            'fields': ('scheduled_start', 'due_date', 'quantity_start', 'priority')
        }),
        ('Workorder Preparation', {
            'fields': ('wj_printed', 'br_printed', 'labels_ordered', 'labels_received')
        }),
        ('Workorder Processing', {
            'fields': ('actual_start', 'status')
        }),
    )
    
    def scheduled_start_dd_mm_yy(self, obj):
        if obj.scheduled_start is not None:
            # Format the date as "dd-mmm-yy"
            return DateFormat(obj.scheduled_start).format('d-M-y')
        else:
            return '-'
    scheduled_start_dd_mm_yy.admin_order_field ='scheduled_start'
    scheduled_start_dd_mm_yy.short_description = 'Scheduled Start Date'
    
    def due_date_dd_mm_yy(self, obj):
        if obj.due_date is not None:
            # Format the date as "dd-mmm-yy"
            return DateFormat(obj.due_date).format('d-M-y')
        else:
            return '-'
    due_date_dd_mm_yy.admin_order_field = 'due_date'
    due_date_dd_mm_yy.short_description = 'Scheduled Due Date'
    
    def actual_start_dd_mm_yy(self, obj):
        if obj.actual_start is not None:
            # Format the date as "dd-mmm-yy"
            return DateFormat(obj.actual_start).format('d-M-y')
        else:
            return '-'
    actual_start_dd_mm_yy.admin_order_field = 'actual_start'
    actual_start_dd_mm_yy.short_description = 'Actual Start Date'

    def sum_quantity_output(self, obj):
        # Calculate the sum of quantity from related operations_output
        total_quantity = output \
            .objects \
            .filter(workorder=obj) \
            .aggregate(Sum('quantity'))['quantity__sum']

        # Check if total_quantity is None (no matching rows) and return 0 instead
        return total_quantity if total_quantity is not None else 0
    sum_quantity_output.short_description = 'Total Quantity'

@admin.register(schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('workorder', 'line')
    list_filter = ('workorder', 'line')
    search_fields = ('workorder', 'line')

    fieldsets = (
        ('Schedule Information', {
            'fields': ('workorder', 'line')
        }),
    )

@admin.register(material)
class MaterialAdmin(admin.ModelAdmin):
    
    class Media:
        js = ('operations/js/dynamic_updates.js',)

    list_display = ('line', 'request_type', 'workorder', 'part_number', 'quantity', 'line_down_at', 'uid', 'comments', 'delivery_status')
    list_filter = ('line','request_type', 'workorder', 'delivery_status')
    search_fields = ('line__name','request_type', 'workorder__workorder_number',)

    fieldsets = (
        ('Line Information', {
            'fields': ('line', 'workorder', 'line_down_at')
        }),
        ('Material Request', {
            'fields': ('request_type', 'part_number', 'quantity')
        }),
        ('Request Information', {
            'fields': ('uid', 'comments', 'delivery_status')
        })
    )