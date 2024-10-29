from django.urls import path
from .views import SignUpView, SignUpSuccessView, SignUpConfirmView
app_name = 'dgroupLogin'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),  # signupへのパス
    path('signup/confirm/', SignUpConfirmView.as_view(), name='signup_confirm'),  # 確認画面へのパス
    path('signup_success/', SignUpSuccessView.as_view(), name='signup_success'),   # サインアップ成功へのパス   
]
