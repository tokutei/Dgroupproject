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
    path('profile/', views.profile, name='profile'),
    path('edit_address/', views.edit_address, name='edit_address'),
    path('address_update_complete/', views.address_update_complete, name='address_update_complete'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('new-arrivals/', views.NewArrivalsView.as_view(), name='new_arrivals'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
#http://127.0.0.1:8000/convenience/register/