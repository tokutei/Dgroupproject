from django import forms
from .models import CustomUser


# 電話番号フォーム
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
        labels = {
            'username': 'ユーザー名',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'address': '住所',
            'password': 'パスワード',
        }
        help_texts = {
            'username': '半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。',
            'nickname': 'ニックネームを入力してください。',
            'email': '有効なメールアドレスを入力してください。',
            'address': '住所を入力してください。',
            'password': 'パスワードを設定してください。',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('パスワードとパスワード確認が一致しません。')
        return cleaned_data
