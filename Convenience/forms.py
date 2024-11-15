from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    ALLERGY_CHOICES = [
        ('egg', '卵'),
        ('milk', '乳'),
        ('wheat', '小麦'),
        ('peanut', 'ピーナッツ'),
        ('soy', '大豆'),
        ('fish', '魚'),
        ('crustacean', '甲殻類'),
    ]
    
    allergies = forms.MultipleChoiceField(
        choices=ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,  # アレルギー選択なしでもOK
    )

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'expiration_date', 'allergies', 'image']
