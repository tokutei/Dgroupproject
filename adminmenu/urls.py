from django.urls import path
from . import views

urlpatterns = [

    path('orders/', views.order_list, name='order_list'),
    path('menu/', views.system_menu, name='system_menu'),  # システムメニュー画面のURL
    path('', views.index, name='index'),
]
