from django.urls import path
from . import views
from .views import TermsAndPrivacyView

app_name = 'dgroupLogin'

urlpatterns = [
    path('terms-and-privacy/', TermsAndPrivacyView.as_view(), name='terms_and_privacy'),  # アンダースコアに修正
    path('phone_number/', views.phone_number_view, name='phone_number'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
]
