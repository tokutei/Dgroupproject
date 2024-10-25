from django.db import models
from accounts.models import CustomUser


class CartPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    aitemimage = models.ImageField(verbose_name='商品の写真', upload_to='photos')
    category = models.CharField(verbose_name='カテゴリー', max_length=100)
    aitemname = models.CharField(verbose_name='商品名', max_length=100)
    price = models.IntegerField(verbose_name='価格')
    shelf = models.DateField(verbose_name='賞味期限')
    def __str__(self):
        return self.aitemname


class OrderPost(models.Model):
    ordernumber = models.IntegerField(verbose_name='注文番号')
    aitem = models.IntegerField(verbose_name='商品数')
    price = models.IntegerField(verbose_name='支払額')
    payment = models.CharField(verbose_name='支払方法', max_length=100)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='住所', max_length=100)
    def __str__(self):
        return self.ordernumber


class OrderAitemPost(models.Model):
    ordernumber = models.IntegerField(verbose_name='注文番号')
    aitemname = models.CharField(verbose_name='商品名', max_length=100)
    aitemprice = models.IntegerField(verbose_name='価格')
    def __str__(self):
        return self.ordernumber
# Create your models here.
