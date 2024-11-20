import json
import stripe
import datetime
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from .models import CartPost, OrderPost, OrderAitemPost, Product, Price
from foods.models import Food
from .forms import CartPostForm
from urllib.parse import urlencode, urljoin

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartView(ListView):
    template_name = 'cart.html'
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        return user_list


class PurchaseDeleteView(UpdateView):
    model = CartPost
    template_name = 'delete.html'
    form_class = CartPostForm

    def get_success_url(self):
        return reverse_lazy('purchaseapp:cart', kwargs={'user': self.request.user.id})

    def form_valid(self, form):
        value = self.object.stock
        input = form.cleaned_data['stockminus']
        self.object.stock = value - input
        if self.object.stock == 0:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.stockminus = 1
            self.object.save()
            return super().form_valid(form)


class PurchaseView(ListView):
    template_name = 'purchase.html'
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        return user_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = self.get_queryset()
        totalprice = sum(item.price * item.stock for item in user_list)
        totalstock = sum(item.stock for item in user_list)
        context['totalprice'] = totalprice
        context['totalstock'] = totalstock
        return context


class DetailView(DetailView):
    template_name = 'detail.html'
    model = CartPost


class CancelPageView(TemplateView):
    template_name = 'cancel.html'


class ProductTopPageView(ListView):
    model = Product
    template_name = "product-top.html"
    context_object_name = "product_list"


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request):
        request.session['address'] = request.POST.get('address')
        request.session['delivery'] = request.POST.get('delivery')
        if 'credit' in request.POST:
            request.session['payment'] = 'credit'
            user_list = CartPost.objects.filter(user=request.user.id)
            YOUR_DOMAIN = "http://127.0.0.1:8000/stripe"
            user_email = request.user.email
            line_items_list = []
            for i in user_list:
                product = Product.objects.get(stripe_product_id=i.stripe_product_id)
                price = Price.objects.get(product=product)
                line_items_list.append({
                    'price': price.stripe_price_id,
                    'quantity': i.stock,
                },)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items_list,
                customer_email = user_email,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return redirect(checkout_session.url)
        else:
            request.session['payment'] = 'cod'
            return redirect('purchasecheck')


def PurchaseCheck(request):
    address = request.session['address']
    delivery = request.session['delivery']
    match delivery:
        case 'standard':
            delivery = '通常配送'
        case 'express':
            delivery = '速達配送'
    object_list = CartPost.objects.filter(user=request.user.id)
    totalprice = sum(item.price * item.stock for item in object_list)
    totalstock = sum(item.stock for item in object_list)
    dictionary = {
        'address': address,
        'delivery': delivery,
        'object_list': object_list,
        'totalprice': totalprice,
        'totalstock': totalstock,
    }
    return render(request, 'purchasecheck.html', dictionary)


def SuccessPage(request):
    if OrderPost.objects.exists():
        input = OrderPost.objects.aggregate(Max('ordernumber'))['ordernumber__max']
        inputordernumber = input + 1
    else:
        inputordernumber = 1
    user_list = CartPost.objects.filter(user=request.user.id)
    address = request.session['address']
    payment = request.session['payment']
    delivery = request.session['delivery']
    totalprice = 0
    totalaitem = 0
    entries = []
    for i in user_list:
        entries.append(OrderAitemPost(
            ordernumber=inputordernumber,
            aitemname=i.aitemname,
            aitemprice=i.price,
            quantity=i.stock)
        )
        totalprice = totalprice + i.price * i.stock
        totalaitem += i.stock
    OrderAitemPost.objects.bulk_create(entries)
    entries = OrderPost(
        ordernumber=inputordernumber,
        aitem=totalaitem,
        price=totalprice,
        payment=payment,
        user=request.user.username,
        address=address,
        delivery_method=delivery)
    entries.save()
    CartPost.objects.filter(user=request.user.id).delete()
    return render(request, ('success.html'))


class BuyView(DetailView):
    template_name = 'buy.html'
    model = Food
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productid = self.object.stripe_product_id
        mystock = CartPost.objects.filter(stripe_product_id=productid)
        if len(mystock) == 0:
            context['maxvalue'] = self.object.stock
        else:
            value = CartPost.objects.get(stripe_product_id=productid)
            context['maxvalue'] = self.object.stock - value.stock
        return context

def BuySuccess(request, stripe_product_id):
    select_list = CartPost.objects.filter(stripe_product_id=stripe_product_id)
    addstock = request.POST.get('addstock')
    if len(select_list) == 0:
        print_list = Food.objects.get(stripe_product_id=stripe_product_id)
        cartadd = CartPost(
            user=request.user,
            stripe_product_id=stripe_product_id,
            aitemimage=print_list.image,
            category=print_list.category,
            aitemname=print_list.name,
            price=print_list.price,
            stock=addstock,
            shelf=print_list.shelf_life,
            allergy=print_list.allergy,
        )
        cartadd.save()
    else:
        update_object = CartPost.objects.get(stripe_product_id=stripe_product_id)
        update_object.stock = update_object.stock + int(addstock)
        update_object.save()
    return redirect('index')
