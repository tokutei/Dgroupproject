from django.urls import path
from . import views

app_name = 'dgroupapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('input/', views.CreateFoodView.as_view(), name='input'),
    path('input_done/', views.InputDoneView.as_view(), name='input_done'),
]
