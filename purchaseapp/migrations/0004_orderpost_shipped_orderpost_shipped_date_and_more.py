# Generated by Django 4.0 on 2024-12-02 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchaseapp', '0003_remove_orderpost_shipped_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpost',
            name='shipped',
            field=models.BooleanField(default=False, verbose_name='配送済み'),
        ),
        migrations.AddField(
            model_name='orderpost',
            name='shipped_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='配送日時'),
        ),
        migrations.AlterField(
            model_name='buyjudge',
            name='stock',
            field=models.IntegerField(verbose_name='購入数'),
        ),
    ]
