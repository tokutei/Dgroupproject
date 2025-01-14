import json
import stripe
import datetime
from django.db.models import Max
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from .models import CartPost, OrderPost, OrderAitemPost, Product, Price, BuyJudge, Payment_intent
from foods.models import Food
from dgroupLogin.models import CustomUser
from .forms import CartPostForm
from urllib.parse import urlencode, urljoin

stripe.api_key = settings.STRIPE_SECRET_KEY

endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

class CartView(ListView):
    template_name = 'cart.html'

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        return user_list


class PurchaseDeleteView(DetailView):
    model = CartPost
    template_name = 'delete.html'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            max_number = self.object.stock
            count = 1
            number = []
            for i in range(max_number):
                number.append(count)
                count = count + 1
            context['deletenumber'] = number
        return context


class OverView(DetailView):
    model = CartPost
    template_name = 'over.html'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            max_number = self.object.stock
            count = 1
            number = []
            for i in range(max_number):
                number.append(count)
                count = count + 1
            context['deletenumber'] = number
            food_list = Food.objects.filter(stripe_product_id=self.object.stripe_product_id)
            if len(food_list) > 0:
                food_list = Food.objects.get(stripe_product_id=self.object.stripe_product_id)
                context['food_stock'] = food_list.stock
            else:
                context['food_stock'] = 0
        return context


class PurchaseView(ListView):
    template_name = 'purchase.html'

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        if len(user_list) > 0:
            user_list.update(added_at=now())
            return user_list
        else:
            return None

    def get_user_id(self):
        user_id = self.kwargs['user']
        return user_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = self.get_queryset()
        if user_list:
            totalprice = sum(item.price * item.stock for item in user_list)
            totalstock = sum(item.stock for item in user_list)
            context['totalprice'] = totalprice + 150
            context['totalstock'] = totalstock
        return context


class DetailView(DetailView):
    template_name = 'detail.html'
    model = CartPost

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


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
        user_list = CartPost.objects.filter(user=request.user.id)
        judgement = 0
        if len(user_list) == 0:
            judgement = 2
        for i in user_list:
            food_list = Food.objects.filter(stripe_product_id=i.stripe_product_id)
            if len(food_list) > 0:
                food_list = Food.objects.get(stripe_product_id=i.stripe_product_id)
                if food_list.stock < i.stock:
                    judgement = 1
            else:
                judgement = 1
        if judgement == 0:
            if 'credit' in request.POST:
                request.session['payment'] = 'credit'
                user_list = CartPost.objects.filter(user=request.user.id)
                YOUR_DOMAIN = "http://127.0.0.1:8000/stripe"
                user_email = request.user.email
                line_items_list = []
                metalist = []
                for i in user_list:
                    product = Product.objects.get(stripe_product_id=i.stripe_product_id)
                    price = Price.objects.get(product=product)
                    line_items_list.append({
                        'price': price.stripe_price_id,
                        'quantity': i.stock,
                    },)
                    metalist.append(i.stripe_product_id)
                line_items_list.append({
                    'price': 'price_1Qh09ML8vAMNBiqUkFzXCIqT',
                    'quantity': 1,
                },)
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items_list,
                    customer_email = user_email,
                    metadata = {
                        "user": request.user.id
                    },
                    mode='payment',
                    payment_intent_data={
                        "capture_method": "manual"
                    },
                    success_url=YOUR_DOMAIN + '/success/',
                    cancel_url=YOUR_DOMAIN + '/cancel/',
                )
                return redirect(checkout_session.url)
            else:
                request.session['payment'] = 'cod'
                return redirect('purchasecheck')
        elif judgement == 1:
            errorname_list = []
            error_list = []
            for i in user_list:
                food_list = Food.objects.filter(stripe_product_id=i.stripe_product_id)
                if len(food_list) > 0:
                    food_list = Food.objects.get(stripe_product_id=i.stripe_product_id)
                    if food_list.stock < i.stock:
                        over = i.stock - food_list.stock
                        errorname_list.append(i.stripe_product_id)
                        error_list.append([i.stripe_product_id, over])
            dictionary = {
                'errorname_list': errorname_list,
                'error_list': error_list,
                'object_list': user_list,
            }
            return render(request, 'cart.html', dictionary)
        else:
            return render(request, ('timeout.html'))



@csrf_exempt
def stripe_webhook(request):
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_name = session["customer_details"]["name"]
        customer_email = session["customer_details"]["email"]
        user = session["metadata"]["user"]
        productlist = []

        amount = session["amount_total"]

        payment_intent = session["payment_intent"]
        customuser = CustomUser.objects.get(id=user)
        intent = Payment_intent(
            user=customuser,
            payment_intent=payment_intent
        )
        intent.save()
        # stripe.PaymentIntent.capture(payment_intent)
        # send_mail(
        #     subject = '商品購入完了！',
        #     message = '{}様\n商品購入ありがとうございます。購入された商品情報'.format(customer_name),
        #     recipient_list = [customer_email],
        #     from_email = 'test@test.com'
        # )
        print(session)
    return HttpResponse(status=200)



def cancel_checkout(request):
    payment_intent = request.POST.get('payment_intent')
    if payment_intent:
        stripe.PaymentIntent.cancel(payment_intent)
    return redirect('canceltemplate')


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
        'totalprice': totalprice + 150,
        'totalstock': totalstock,
    }
    return render(request, 'purchasecheck.html', dictionary)


def SuccessPage(request):
    judge = 0
    user_list = CartPost.objects.filter(user=request.user.id)
    if len(user_list) == 0:
        intent = Payment_intent.objects.filter(user=request.user.id)
        if len(intent) > 0:
            payment = Payment_intent.objects.get(user=request.user.id)
            payment_intent = payment.payment_intent
            stripe.PaymentIntent.cancel(payment_intent)
            payment.delete()
        return render(request, ('timeout.html'))
    else:
        errorname_list = []
        error_list = []
        for i in user_list:
            food_list = Food.objects.filter(stripe_product_id=i.stripe_product_id)
            if len(food_list) > 0:
                food_list = Food.objects.get(stripe_product_id=i.stripe_product_id)
                if food_list.stock < i.stock:
                    over = i.stock - food_list.stock
                    errorname_list.append(i.stripe_product_id)
                    error_list.append([i.stripe_product_id, over])
        dictionary = {
            'errorname_list': errorname_list,
            'error_list': error_list,
            'object_list': user_list,
        }
        intent = Payment_intent.objects.filter(user=request.user.id)
        if len(intent) > 0:
            payment = Payment_intent.objects.get(user=request.user.id)
            payment_intent = payment.payment_intent
            if len(error_list) > 0:
                stripe.PaymentIntent.cancel(payment_intent)
                judge = 1
                payment.delete()
                return render(request, 'cart.html', dictionary)
            else:
                stripe.PaymentIntent.capture(payment_intent)
                payment.delete()
        else:
            if len(error_list) > 0:
                judge = 1
                return render(request, 'cart.html', dictionary)
        if judge == 0:
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
            messagetext = ''+request.user.username+'様\n商品購入ありがとうございます。購入された商品情報\n'

            payment_intent = request.POST.get('payment_intent')
            if payment_intent:
                stripe.PaymentIntent.capture(payment_intent)

            for i in user_list:
                entries.append(OrderAitemPost(
                    ordernumber=inputordernumber,
                    aitemname=i.aitemname,
                    aitemprice=i.price,
                    quantity=i.stock)
                )
                messagetext = messagetext + '　・商品名:'+i.aitemname+'　　個数:'+str(i.stock)+'\n'
                totalprice = totalprice + i.price * i.stock
                totalaitem += i.stock
            OrderAitemPost.objects.bulk_create(entries)
            entries = OrderPost(
                ordernumber=inputordernumber,
                aitem=totalaitem,
                price=totalprice + 150,
                payment=payment,
                user=request.user.username,
                address=address,
                delivery_method=delivery)
            entries.save()
            for i in user_list:
                item_list = Food.objects.filter(stripe_product_id=i.stripe_product_id)
                if len(item_list) > 0:
                    item_list = Food.objects.get(stripe_product_id=i.stripe_product_id)
                    item_list.stock -= i.stock
                    if item_list.stock < 1:
                        item_list.delete()
                    else:
                        item_list.save()
                judge_list = BuyJudge.objects.filter(stripe_product_id=i.stripe_product_id)
                if len(judge_list) > 0:
                    judge_list = BuyJudge.objects.get(stripe_product_id=i.stripe_product_id)
                    judge_list.stock -= i.stock
                    if judge_list.stock < 1:
                        judge_list.delete()
                    else:
                        judge_list.save()
            CartPost.objects.filter(user=request.user.id).delete()
            send_mail(
                subject = '商品購入完了！',
                message = messagetext,
                recipient_list = [request.user.email],
                from_email = 'test@test.com'
            )
            return render(request, ('success.html'))


class BuyView(DetailView):
    template_name = 'buy.html'
    model = Food
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        judge = BuyJudge.objects.filter(stripe_product_id=self.object.stripe_product_id)
        maxnum = self.object.stock
        if len(judge) > 0:
            judge = BuyJudge.objects.get(stripe_product_id=self.object.stripe_product_id)
            maxnum = self.object.stock - judge.stock
        number = 1
        numlist = []
        for i in range(maxnum):
            numlist.append(number)
            number = number + 1
        context['numlist'] = numlist
        return context

def BuySuccess(request, stripe_product_id):
    select_list = CartPost.objects.filter(stripe_product_id=stripe_product_id, user=request.user.id)
    addstock = request.POST.get('addstock')
    target = BuyJudge.objects.filter(stripe_product_id=stripe_product_id)
    if len(target) > 0:
        target = BuyJudge.objects.get(stripe_product_id=stripe_product_id)
        target.stock += int(addstock)
        target.save()
    else:
        target = BuyJudge(
            stripe_product_id=stripe_product_id,
            stock=int(addstock)
        )
        target.save()
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


def DeleteSuccess(request, stripe_product_id):
    delete_object = CartPost.objects.filter(stripe_product_id=stripe_product_id)
    if len(delete_object) > 0:
        delete_object = CartPost.objects.get(stripe_product_id=stripe_product_id)
        deletestock = request.POST.get('deletestock')
        if delete_object.stock - int(deletestock) > 0:
            delete_object.stock = delete_object.stock - int(deletestock)
            delete_object.save()
        else:
            delete_object.delete()
        deletejudge = BuyJudge.objects.filter(stripe_product_id=stripe_product_id)
        if len(deletejudge) > 0:
            deletejudge = BuyJudge.objects.get(stripe_product_id=stripe_product_id)
            deletejudge.stock -= int(deletestock)
            deletejudge.save()
    return redirect('purchaseapp:cart', request.user.id)


def OverDelete(request, stripe_product_id):
    delete_object = CartPost.objects.filter(stripe_product_id=stripe_product_id)
    if len(delete_object) > 0:
        delete_object = CartPost.objects.get(stripe_product_id=stripe_product_id)
        deletestock = request.POST.get('deletestock')
        if delete_object.stock - int(deletestock) > 0:
            delete_object.stock = delete_object.stock - int(deletestock)
            delete_object.save()
        else:
            delete_object.delete()
        deletejudge = BuyJudge.objects.filter(stripe_product_id=stripe_product_id)
        if len(deletejudge) > 0:
            deletejudge = BuyJudge.objects.get(stripe_product_id=stripe_product_id)
            deletejudge.stock -= int(deletestock)
            deletejudge.save()
    errorname_list = []
    error_list = []
    user_list = CartPost.objects.filter(user=request.user.id)
    for i in user_list:
        food_list = Food.objects.filter(stripe_product_id=i.stripe_product_id)
        if len(food_list) > 0:
            food_list = Food.objects.get(stripe_product_id=i.stripe_product_id)
            if food_list.stock < i.stock:
                over = i.stock - food_list.stock
                errorname_list.append(i.stripe_product_id)
                error_list.append([i.stripe_product_id, over])
    dictionary = {
        'errorname_list': errorname_list,
        'error_list': error_list,
        'object_list': user_list,
    }
    return render(request, 'cart.html', dictionary)
