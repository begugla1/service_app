# Generated by Django 3.2.16 on 2023-07-05 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_subscription_full_price_with_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='full_price_with_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13, verbose_name='Full_price_with_discount'),
        ),
    ]
