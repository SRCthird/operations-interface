from django.urls import path
from . import views

urlpatterns = [
    path('downtime/<int:id>/', views.downtimeForm, name='downtime_form'),
]
