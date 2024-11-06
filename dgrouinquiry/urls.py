# dgroupinquiry/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),  # お問い合わせフォームのビューを設定
]
