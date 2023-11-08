from django.urls import path
from . import views

urlpatterns = [
    path('downtime/<int:id>/', views.downtimeForm, name='downtime_form'),
    path('output/<str:line>/<str:shift>', views.outputForm, name='output_form'),
    path('reject/<str:line>/<str:shift>', views.rejectForm, name='reject_form'),
]
