from django.contrib import admin
from .models import *

admin.AdminSite.site_header = 'Jaffrey Operations Administration'
admin.AdminSite.site_title = 'Jaffrey Operations Administration'
admin.AdminSite.index_title = 'Site Administration'

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
    ordering = ('line', 'shift')
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