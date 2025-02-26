from django.db import models
from dgroupLogin.models import CustomUser
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta


class CartPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    stripe_product_id = models.CharField(verbose_name="商品ID", max_length=100)
    aitemimage = models.ImageField(verbose_name='商品の写真', upload_to='photos')
    category = models.CharField(verbose_name='カテゴリー', max_length=100)
    aitemname = models.CharField(verbose_name='商品名', max_length=200)
    price = models.IntegerField(verbose_name='価格')
    stock = models.IntegerField(verbose_name='数量')
    stockminus = models.IntegerField(verbose_name='削除数量', default=1)
    shelf = models.DateField(verbose_name='賞味期限')
    allergy = models.CharField(verbose_name='アレルギー', max_length=150)
    added_at = models.DateTimeField(verbose_name='追加日時', auto_now_add=True)

    def __str__(self):
        return self.aitemname

    def is_expired(self):
        expiration_time = self.added_at + timedelta(minutes=30)
        return timezone.now() > expiration_time


class OrderPost(models.Model):
    DELIVERY_CHOICES = [
        ('standard', '通常配送'),
        ('express', '速達配送'),
    ]

    PAYMENT_METHOD = [
        ('credit', 'クレジットカード決済'),
        ('cod', '代金引換'),
    ]

    ordernumber = models.IntegerField(verbose_name='注文番号')
    aitem = models.IntegerField(verbose_name='商品数')
    price = models.IntegerField(verbose_name='支払額')
    payment = models.CharField(verbose_name='支払方法', max_length=100, choices=PAYMENT_METHOD)
    user = models.CharField(verbose_name='ユーザー', max_length=100)
    address = models.CharField(verbose_name='住所', max_length=100)
    postal_code = models.CharField(verbose_name='郵便番号', max_length=7, blank=True, null=True)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='standard')
    ordertime = models.DateTimeField(verbose_name='注文日時', auto_now_add=True)
    
    shipped = models.BooleanField(default=False, verbose_name='配送済み')  # 配送完了フラグ
    shipped_date = models.DateTimeField(null=True, blank=True, verbose_name='配送日時')  # 配送日時
    def __str__(self):
        return self.user


class OrderAitemPost(models.Model):
    ordernumber = models.IntegerField(verbose_name='注文番号')
    aitemname = models.CharField(verbose_name='商品名', max_length=100)
    aitemprice = models.IntegerField(verbose_name='価格')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    def __str__(self):
        return self.aitemname


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=100)
    file = models.FileField(upload_to="photos", blank=True, null=True)
    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product, related_name='Prices', on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    def get_display_price(self):
        return self.price


class BuyJudge(models.Model):
    stripe_product_id = models.CharField(verbose_name='商品ID', max_length=100)
    stock = models.IntegerField(verbose_name='購入数')
    def __str__(self):
        return self.stripe_product_id


class Payment_intent(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    payment_intent = models.CharField(max_length=9999)
    def __str__(self):
        return self.payment_intent

# Create your models here.
