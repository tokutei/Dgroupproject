from django.forms import ModelForm
from .models import FoodInput, Allergy
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
        model = FoodInput
        fields = ['category', 'name', 'price', 'stock', 'shelf_life', 'allergy', 'image']
        widgets = {
            'shelf_life': forms.SelectDateWidget()
        }
