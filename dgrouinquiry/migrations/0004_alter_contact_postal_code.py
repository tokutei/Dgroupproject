# Generated by Django 4.0 on 2025-01-24 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgrouinquiry', '0003_alter_contact_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='postal_code',
            field=models.CharField(default='000-0000', max_length=10),
        ),
    ]
