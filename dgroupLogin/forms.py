from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:  # ここを追加
        model = CustomUser  # この行はこのまま
        fields = ('username', 'email', 'address', 'password1', 'password2') 
