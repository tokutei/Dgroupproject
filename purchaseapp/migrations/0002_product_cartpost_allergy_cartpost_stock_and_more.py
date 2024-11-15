# Generated by Django 4.0 on 2024-11-15 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchaseapp', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='cartpost',
            name='allergy',
            field=models.CharField(default=1, max_length=150, verbose_name='アレルギー'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartpost',
            name='stock',
            field=models.IntegerField(default=1, verbose_name='数量'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartpost',
            name='stockminus',
            field=models.IntegerField(default=1, verbose_name='削除数量'),
        ),
        migrations.AddField(
            model_name='cartpost',
            name='stripe_product_id',
            field=models.CharField(default=1, max_length=100, verbose_name='商品ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderaitempost',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='数量'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderpost',
            name='delivery_method',
            field=models.CharField(choices=[('standard', '通常配送'), ('express', '速達配送')], default='standard', max_length=10),
        ),
        migrations.AlterField(
            model_name='cartpost',
            name='aitemname',
            field=models.CharField(max_length=200, verbose_name='商品名'),
        ),
        migrations.AlterField(
            model_name='orderpost',
            name='payment',
            field=models.CharField(choices=[('credit', 'クレジットカード決済'), ('cod', '代金引換')], max_length=100, verbose_name='支払方法'),
        ),
        migrations.AlterField(
            model_name='orderpost',
            name='user',
            field=models.CharField(max_length=100, verbose_name='ユーザー'),
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
    ]