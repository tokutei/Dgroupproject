from django import forms
from django.core.validators import RegexValidator
from .models import CustomUser


# ユーザー情報フォーム
class CustomUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='パスワード確認')

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email', 'phone_number', 'address', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名（半角英数字、記号）'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'ニックネームを入力してください'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@domain.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '電話番号（10～11桁）'}),
            'address': forms.Textarea(attrs={'placeholder': '住所を入力してください', 'rows': 3}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワードを入力してください'}),
        }
        labels = {
            'username': 'ユーザー名',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'phone_number': '電話番号',
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

    # `username`フィールドに半角英数字と特定記号のみを許可するバリデーション
    username = forms.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[a-zA-Z0-9@.+/-_]+$', '半角英数字と一部の記号のみを使用できます。')],
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名（半角英数字、記号）'})
    )

    # `phone_number`フィールドに10桁または11桁の半角数字のみを許可するバリデーション
    phone_number = forms.CharField(
        max_length=11,
        min_length=10,
        validators=[RegexValidator(r'^[0-9]{10,11}$', '10桁または11桁の半角数字を入力してください')],
        widget=forms.TextInput(attrs={'placeholder': '電話番号（10～11桁）'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('パスワードとパスワード確認が一致しません。')
        return cleaned_data
    
    def save(self, commit=True):
        # パスワードをハッシュ化して保存
        user = super().save(commit=False)
        if user.password:
            user.set_password(user.password)  # ここでパスワードをハッシュ化
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email', 'phone_number', 'address']  # 必要なフィールドを指定
        labels = {
            'username': 'ユーザー名',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'phone_number': '電話番号',
            'address': '住所',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
