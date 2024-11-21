# Generated by Django 4.0 on 2024-11-21 06:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='カテゴリ')),
                ('image', models.ImageField(default='images/default.jpg', upload_to='images', verbose_name='写真')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_product_id', models.CharField(max_length=100, verbose_name='商品ID')),
                ('stripe_price_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200, verbose_name='商品名')),
                ('price', models.IntegerField(verbose_name='価格')),
                ('stock', models.IntegerField(verbose_name='在庫')),
                ('shelf_life', models.DateField(default=django.utils.timezone.now, verbose_name='賞味期限')),
                ('allergy', models.CharField(max_length=150, verbose_name='アレルギー')),
                ('image', models.ImageField(upload_to='images', verbose_name='写真')),
                ('inputed_at', models.DateField(auto_now_add=True, verbose_name='入力日時')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='foods.category', verbose_name='カテゴリ')),
            ],
        ),
    ]
