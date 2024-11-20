from django.urls import path
from .import views

app_name = 'foods'

urlpatterns = [
    path('food_input/', views.CreateFoodView.as_view(), name='food_input'),
    path('input_done/', views.InputSuccessView.as_view(), name='input_done'),
    path('food_delete/', views.FoodDeleteListView.as_view(), name='food_delete_list'), 
    path('food_delete/<int:pk>/', views.FoodDeleteView.as_view(), name='food_delete'),
    path('food_update/<int:pk>', views.UpdateFoodView.as_view(), name='food_update'),
]
