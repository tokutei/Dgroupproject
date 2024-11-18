from django.forms import ModelForm
from .models import Food, Allergy


from django import forms


class FoodInputForm(ModelForm):

    allergy = forms.MultipleChoiceField(
        label='アレルギー',
        required=False,
        disabled=False,
        initial=[],
        choices=[(i.name, i.name) for i in Allergy.objects.all()],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Food
        fields = ['category', 'name', 'price', 'stock', 'shelf_life', 'allergy', 'image']
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "商品名を入力"}),
            'shelf_life': forms.NumberInput(attrs={"type": "date"})
        }
