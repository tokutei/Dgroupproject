# models.py
from django.db import models

class Order(models.Model):
    PRODUCT_CHOICES = [
        ('A', '商品A'),
        ('B', '商品B'),
        ('C', '商品C'),
    ]
    
    DELIVERY_CHOICES = [
        ('standard', '通常配送'),
        ('express', '速達配送'),
    ]

    order_number = models.CharField(max_length=10, unique=True)
    product_name = models.CharField(max_length=1, choices=PRODUCT_CHOICES)
    quantity = models.PositiveIntegerField()
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='standard')
    shipped = models.BooleanField(default=False)  # 配送ステータスを追加
    shipped_date = models.DateTimeField(null=True, blank=True)  # 配送日時を追加

    def __str__(self):
        return f"注文 {self.order_number} - {self.product_name}"
