import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from purchaseapp.models import Product, Price
from .forms import FoodInputForm

stripe.api_key = settings.STRIPE_SECRET_KEY


# 商品情報入力ページのビュー
class CreateFoodView(CreateView):
    form_class = FoodInputForm
    template_name = "food_input.html"
    success_url = reverse_lazy('foods:input_done')

    def form_valid(self, form):
        inputdata = form.save(commit=False)
        allergy = form.cleaned_data.get("allergy")
        if allergy:
            inputdata.allergy = '、'.join(allergy)
        else:
            inputdata.allergy = 'なし'
        productname = inputdata.name
        price = int(inputdata.price)
        product = stripe.Product.create(
            name=productname,
        )
        price_data = stripe.Price.create(
            product=product.id,
            unit_amount=price,
            currency='jpy'
        )
        productdb = Product(
            name=productname,
            stripe_product_id=product.id,
        )
        productdb.save()
        price = Price(
            product=productdb,
            stripe_price_id=price_data.id,
            price=price,
        )
        inputdata.stripe_product_id = product.id
        inputdata.stripe_price_id = price_data.id
        price.save()
        inputdata.save()
        return super().form_valid(form)


# 入力完了ページのビュー
class InputSuccessView(TemplateView):
    template_name = 'input_success.html'
