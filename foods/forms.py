from django.forms import ModelForm
from .models import Food


from django import forms


class FoodInputForm(ModelForm):

    CHOICE = [('えび', 'えび'), ('かに', 'かに'), ('小麦', '小麦'),
              ('そば', 'そば'), ('卵', '卵'), ('乳', '乳'), ('落花生', '落花生'),
              ('あわび', 'あわび'), ('いか', 'いか'), ('いくら', 'いくら'),
              ('さけ', 'さけ'), ('さば', 'さば'), ('牛肉', '牛肉'),
              ('豚肉', '豚肉'), ('鶏肉', '鶏肉'), ('オレンジ', 'オレンジ'),
              ('キウイフルーツ', 'キウイフルーツ'), ('もも', 'もも'),
              ('りんご', 'りんご'), ('バナナ', 'バナナ'), ('やまいも', 'やまいも'),
              ('大豆', '大豆'), ('くるみ', 'くるみ'), ('アーモンド', 'アーモンド'),
              ('カシューナッツ', 'カシューナッツ'), ('ごま', 'ごま'),
              ('まつたけ', 'まつたけ'), ('ゼラチン', 'ゼラチン')]

    allergy = forms.MultipleChoiceField(
        label='アレルギー',
        choices=CHOICE,
        required=False,
        disabled=False,
        initial=[],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Food
        fields = ['category', 'name', 'price', 'stock', 'shelf_life', 'allergy', 'image']
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "商品名を入力"}),
            'shelf_life': forms.NumberInput(attrs={"type": "date"})
        }
