from django.urls import path
from line_management import views as line_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demo/', views.demo, name='demo'),
    path('material/', views.MaterialListView.as_view(), name='material_list'),
    path('material/add/', views.MaterialCreateView.as_view(), name='material_create'),
    path('material/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
    path('line/<str:pk>/<str:shift>/', line_views.line_view, name='line_view'),
    path('update_downtime/<int:downtime_id>/', line_views.update_downtime, name='update_downtime'),
    path('create_downtime/', line_views.create_downtime, name='create_downtime'),
]
