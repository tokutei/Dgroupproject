import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from purchaseapp.models import Product, Price
from .forms import FoodInputForm
from django.views.generic import ListView, DeleteView 
from .models import Food  


stripe.api_key = settings.STRIPE_SECRET_KEY


# 商品情報入力ページのビュー
class FoodCreateView(CreateView):
    form_class = FoodInputForm
    template_name = "food_input.html"
    success_url = reverse_lazy('foods:food_input')

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


# 登録食品の一覧ページ
class FoodDeleteListView(ListView):
    model = Food
    template_name = 'food_delete_list.html'
    context_object_name = 'foods'


# 個別削除ページ
class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'food_delete_confirm.html'
    success_url = reverse_lazy('foods:food_delete_list')


# 変更ページのビュー
class FoodUpdateView(UpdateView):
    template_name = 'food_update.html'
    form_class = FoodInputForm
    model = Food
    success_url = reverse_lazy('foods:food_delete_list')

    # 既存のアレルギーデータを取得して変更画面の初期値に設定
    def get_initial(self):
        initial = super().get_initial()
        food = self.get_object()
        initial['allergy'] = food.allergy.split('、') if food.allergy else []
        return initial

    def form_valid(self, form):
        adddata = form.save(commit=False)
        allergy = form.cleaned_data.get("allergy")
        if allergy:
            adddata.allergy = '、'.join(allergy)
        else:
            adddata.allergy = 'なし'
        productname = adddata.name
        price = int(adddata.price)
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
        adddata.stripe_product_id = product.id
        adddata.stripe_price_id = price_data.id
        price.save()
        adddata.save()
        return super().form_valid(form)
