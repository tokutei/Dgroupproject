from django.urls import path
from .views import IndexView, LoginView, LogoutView, InputDoneView,SuperuserOnlyView
from .views import CreateFoodView
app_name = 'dgroupapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('superuser-only/', SuperuserOnlyView.as_view(), name='superuser_only'),
    path('input_food/', CreateFoodView.as_view(), name='input_food'),
    path('input_done/', InputDoneView.as_view(), name='input_done'),
]
