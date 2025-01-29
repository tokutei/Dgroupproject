from django import forms
from django.core.exceptions import ValidationError

class AddressEditForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'お届け先住所を入力してください'}
    )
    postal_code = forms.CharField(
        max_length=7,
        min_length=7,
        required=True,
        error_messages={
            'required': '※郵便番号を入力してください',
            'min_length': '※郵便番号は7桁で入力してください',
            'max_length': '※郵便番号は7桁で入力してください',
        }
    )
    
    # 郵便番号のバリデーション（数字だけ）
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isdigit():
            raise ValidationError('郵便番号は数字だけで入力してください')
        return postal_code
