from django.urls import path
from .import views

app_name = 'foods'

urlpatterns = [
    path('food_input/', views.FoodCreateView.as_view(), name='food_input'),
    path('food_delete/', views.FoodDeleteListView.as_view(), name='food_delete_list'), 
    path('food_delete/<int:pk>/', views.FoodDeleteView.as_view(), name='food_delete'),
    path('food_update/<int:pk>', views.FoodUpdateView.as_view(), name='food_update'),
]
