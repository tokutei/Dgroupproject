from django.forms import ModelForm
from .models import CartPost


class CartPostForm(ModelForm):
    class Meta:
        model = CartPost
        fields = ['stockminus']

    def __init__(self, *args, **kwargs):
        super(CartPostForm, self).__init__(*args, **kwargs)
        maxvalue = kwargs['instance'].stock
        self.fields['stockminus'].widget.attrs.update({
            'class': 'form-control text-center me-3',
            'id': 'inputQuantity',
            'style': 'max-width: 3rem',
            'type': 'number',
            'min': 1,
            'max': maxvalue
        })
