from django import forms
from .models import CustomUser


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='電話番号')


# ユーザー情報フォーム
class CustomUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='パスワード確認')

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email', 'address', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('パスワードとパスワード確認が一致しません。')
        return cleaned_data
