from django import forms
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