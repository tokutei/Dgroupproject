from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)  # 商品名
    quantity = models.IntegerField()  # 個数
    expiration_date = models.DateField()  # 消費期限
    allergies = models.TextField(blank=True)  # アレルギー情報（カンマ区切りのテキスト形式）
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 商品画像

    def __str__(self):
        return self.name
