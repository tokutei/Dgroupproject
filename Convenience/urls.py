from django.urls import path
from . import views

app_name = 'Convenience'
urlpatterns = [
    path('register/', views.product_register, name='product_register'),  # 商品登録
    path('pconfirm/', views.product_confirm, name='product_confirm'),  # 確認ページ
    path('products/', views.product_list, name='product_list'),  # 商品一覧
]
