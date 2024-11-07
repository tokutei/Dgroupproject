# dgroupinquiry/urls.py

from django.urls import path
from . import views

app_name = 'dgrouinquiry'

urlpatterns = [
    path('', views.contact_view, name='contact'),  # お問い合わせフォームのビューを設定
    path('confirm/', views.contact_confirm_view, name='contact_confirm'),
]
