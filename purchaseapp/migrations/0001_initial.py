# Generated by Django 4.0 on 2024-11-21 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dgroupLogin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyJudge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_product_id', models.CharField(max_length=100, verbose_name='商品ID')),
                ('stock', models.IntegerField(verbose_name='購入数')),
            ],
        ),
        migrations.CreateModel(
            name='OrderAitemPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField(verbose_name='注文番号')),
                ('aitemname', models.CharField(max_length=100, verbose_name='商品名')),
                ('aitemprice', models.IntegerField(verbose_name='価格')),
                ('quantity', models.PositiveIntegerField(verbose_name='数量')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField(verbose_name='注文番号')),
                ('aitem', models.IntegerField(verbose_name='商品数')),
                ('price', models.IntegerField(verbose_name='支払額')),
                ('payment', models.CharField(choices=[('credit', 'クレジットカード決済'), ('cod', '代金引換')], max_length=100, verbose_name='支払方法')),
                ('user', models.CharField(max_length=100, verbose_name='ユーザー')),
                ('address', models.CharField(max_length=100, verbose_name='住所')),
                ('delivery_method', models.CharField(choices=[('standard', '通常配送'), ('express', '速達配送')], default='standard', max_length=10)),
                ('shipped', models.BooleanField(default=False, verbose_name='配送済み')),
                ('shipped_date', models.DateTimeField(blank=True, null=True, verbose_name='配送日時')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_product_id', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='photos')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_price_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prices', to='purchaseapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_product_id', models.CharField(max_length=100, verbose_name='商品ID')),
                ('aitemimage', models.ImageField(upload_to='photos', verbose_name='商品の写真')),
                ('category', models.CharField(max_length=100, verbose_name='カテゴリー')),
                ('aitemname', models.CharField(max_length=200, verbose_name='商品名')),
                ('price', models.IntegerField(verbose_name='価格')),
                ('stock', models.IntegerField(verbose_name='数量')),
                ('stockminus', models.IntegerField(default=1, verbose_name='削除数量')),
                ('shelf', models.DateField(verbose_name='賞味期限')),
                ('allergy', models.CharField(max_length=150, verbose_name='アレルギー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgroupLogin.customuser', verbose_name='ユーザー')),
            ],
        ),
    ]
