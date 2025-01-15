# Generated by Django 5.1.4 on 2025-01-13 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderaddress',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order'),
        ),
    ]
