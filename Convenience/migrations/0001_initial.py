# Generated by Django 4.0 on 2024-11-21 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('expiration_date', models.DateField()),
                ('allergies', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
            ],
        ),
    ]
