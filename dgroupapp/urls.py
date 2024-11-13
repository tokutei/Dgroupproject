from django.urls import path,include
from .views import IndexView, LoginView, LogoutView, SuperuserOnlyView
from .import views

app_name = 'dgroupapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('superuser-only/', SuperuserOnlyView.as_view(), name='superuser_only'),
    path('contact/', include('dgrouinquiry.urls')),
    path('switch_account/', views.switch_account, name='switch_account'),
    path('teams/', views.TeamsView.as_view(), name='teams'),  
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('convenience/', include('Convenience.urls')),
]
