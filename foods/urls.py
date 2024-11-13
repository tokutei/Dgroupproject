from django.urls import path
from .import views

app_name = 'foods'

urlpatterns = [
    path('food_input/', views.CreateFoodView.as_view(), name='food_input'),
    path('input_done/', views.InputDoneView.as_view(), name='input_done'),
]
