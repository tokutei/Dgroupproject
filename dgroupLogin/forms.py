from django import forms
from django.core.validators import RegexValidator
from .models import CustomUser
from django.core.validators import MaxLengthValidator, MinLengthValidator

# ユーザー情報フォーム
class CustomUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='パスワード確認')

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email', 'phone_number', 'address', 'postal_code', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名（半角英数字、記号）'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'ニックネームを入力してください'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@domain.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '電話番号（10～11桁　‐無し）（入力例）　0262295577'}),
            'address': forms.Textarea(attrs={'placeholder': '住所を入力してください（入力例）長野県長野市栗田 2288', 'rows': 3}),
            'postal_code': forms.TextInput(attrs={'placeholder': '郵便番号（7桁の半角数字）'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワードを入力してください'}),
        }
        labels = {
            'username': 'ユーザー名',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'phone_number': '電話番号',
            'postal_code': '郵便番号',
            'address': '住所',
        }
        help_texts = {
            'username': '半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。',
            'nickname': 'ニックネームを入力してください。',
            'email': '有効なメールアドレスを入力してください。',
            'postal_code': '郵便番号は7桁の半角数字で入力してください。',
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

    # `postal_code`フィールドに7桁の半角数字のみを許可するバリデーション
    postal_code = forms.CharField(
        max_length=7,
        min_length=7,
        validators=[RegexValidator(r'^[0-9]{7}$', '郵便番号は7桁の半角数字で入力してください')],
        widget=forms.TextInput(attrs={'placeholder': '郵便番号（7桁の半角数字）'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        address = cleaned_data.get('address')
        postal_code = cleaned_data.get('postal_code')

        # パスワードと確認用パスワードの一致チェック
        if password != confirm_password:
            raise forms.ValidationError('パスワードとパスワード確認が一致しません。')

        # 住所と郵便番号が両方とも入力されていない場合にエラーを発生
        if not address or not postal_code:
            raise forms.ValidationError('住所と郵便番号は両方とも必須です。')

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
        fields = ['nickname', 'email', 'phone_number', 'postal_code', 'address']
        labels = {
            'username': 'ユーザー名',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'phone_number': '電話番号',
            'postal_code': '郵便番号',
            'address': '住所',
        }

    nickname = forms.CharField(
        max_length=30,
        required=True,
        label="ニックネーム",
        widget=forms.TextInput(attrs={
            'placeholder': '例: 山田太郎',
            'size': '20',
            'style': 'margin-left: 15px;',
        })
    )

    email = forms.EmailField(
        required=True,
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            'placeholder': '例: example@example.com',
            'size': '30',
            'style': 'margin-left: 5px;',
        })
    )

    phone_number = forms.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11, "電話番号は11桁で入力してください"),
        ],
        required=True,
        label="電話番号",
        widget=forms.TextInput(attrs={
            'placeholder': '例: 09012345678',
            'pattern': '\d{11}',
            'size': '13',
            'style': 'margin-left: 22px;',
        })
    )

    postal_code = forms.CharField(
        max_length=7,
        validators=[
            MinLengthValidator(7, "郵便番号は7桁で入力してください"),
        ],
        required=True,
        label="郵便番号",
        widget=forms.TextInput(attrs={
            'placeholder': '例: 1234567',
            'pattern': '\d{7}',
            'size': '12',
            'style': 'margin-left: 22px;',
        })
    )

    address = forms.CharField(
        max_length=100,
        required=True,
        label="住所",
        widget=forms.TextInput(attrs={
            'placeholder': '例: 長野市篠ノ井1-2-3',
            'size': '30',
            'style': 'margin-left: 53px;',
        })
    )