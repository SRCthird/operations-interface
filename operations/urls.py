from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demo/', views.demo, name='demo'),
    path('material/', views.MaterialListView.as_view(), name='material_list'),
    path('material/add/', views.MaterialCreateView.as_view(), name='material_create'),
    path('material/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
]