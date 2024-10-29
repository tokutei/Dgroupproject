from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/ship/<int:order_id>/', views.ship_order, name='ship_order'),  # 配送済み
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),  # 配送取り消しのURL
]
