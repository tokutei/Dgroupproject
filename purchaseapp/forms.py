from django.forms import ModelForm
from .models import CartPost


class CartPostForm(ModelForm):
    class Meta:
        model = CartPost
        fields = ['category', 'title', 'comment', 'image1', 'image2']