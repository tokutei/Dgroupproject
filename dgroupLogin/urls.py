from django.urls import path
from . import views
from .views import TermsAndPrivacyView

app_name = 'dgroupLogin'

urlpatterns = [
    path('terms-and-privacy/', TermsAndPrivacyView.as_view(), name='terms_and_privacy'),
    path('termsofservice', views.terms_of_service_view, name='termsofservice'),
    path('privacyconfirmation/', views.privacy_confirmation_view, name='privacy_confirmation'),  # 追加
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('singnup_success/', views.singnup_success_view, name='singnup_success'),
    
]