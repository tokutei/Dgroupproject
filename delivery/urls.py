from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),

    path('ship_order/<int:order_id>/', views.ship_order, name='ship_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
