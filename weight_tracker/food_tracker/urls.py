from django.urls import path
from . import views

app_name = 'food_tracker'

urlpatterns = [
    path('log', views.food_log, name='food_log'),

    path('search/', views.search_food, name='search_food'),
    path('add/<int:fdc_id>', views.add_food_entry, name='add_food_entry'),
    path('entry_detail/<int:pk>', views.entry_detail, name='entry_detail'),

    path('delete/<int:pk>/', views.delete_food_entry, name='delete_food_entry'),
    path('calculate_tdee/', views.calculate_tdee, name='calculate_tdee'),
]