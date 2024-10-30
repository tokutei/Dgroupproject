# Generated by Django 4.0 on 2024-10-30 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dgroupLogin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAitemPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField(verbose_name='注文番号')),
                ('aitemname', models.CharField(max_length=100, verbose_name='商品名')),
                ('aitemprice', models.IntegerField(verbose_name='価格')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField(verbose_name='注文番号')),
                ('aitem', models.IntegerField(verbose_name='商品数')),
                ('price', models.IntegerField(verbose_name='支払額')),
                ('payment', models.CharField(max_length=100, verbose_name='支払方法')),
                ('address', models.CharField(max_length=100, verbose_name='住所')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgroupLogin.customuser', verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='CartPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aitemimage', models.ImageField(upload_to='photos', verbose_name='商品の写真')),
                ('category', models.CharField(max_length=100, verbose_name='カテゴリー')),
                ('aitemname', models.CharField(max_length=100, verbose_name='商品名')),
                ('price', models.IntegerField(verbose_name='価格')),
                ('shelf', models.DateField(verbose_name='賞味期限')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgroupLogin.customuser', verbose_name='ユーザー')),
            ],
        ),
    ]
