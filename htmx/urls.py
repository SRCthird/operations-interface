from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:element_id>/', views.index, name='index'),
]
