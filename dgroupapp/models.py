from django.db import models


# カテゴリモデル
class Category(models.Model):

    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )

    def __str__(self):
        return self.title


# 食品入力モデル
class FoodInput(models.Model):

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )

    name = models.CharField(
        verbose_name='商品名',
        max_length=200
    )

    price = models.IntegerField(
        verbose_name='価格'
    )

    stock = models.IntegerField(
        verbose_name='数量'
    )

    shelf_life = models.DateField(
        verbose_name='賞味期限',
    )

    allergy = models.CharField(
        verbose_name='アレルギー',
        max_length=150,
    )

    image = models.ImageField(
        verbose_name='写真',
        upload_to='images',
    )

    inputed_at = models.DateField(
        verbose_name='入力日時',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


# アレルギー食材モデル
class Allergy(models.Model):

    name = models.CharField(
        verbose_name='アレルギー食材名',
        max_length=20,
    )

    def __str__(self):
        return self.name
