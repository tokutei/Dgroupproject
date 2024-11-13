from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.product_register, name='product_register'),  # 商品登録
    path('list/', views.product_list, name='product_list'),  # 商品一覧
]
