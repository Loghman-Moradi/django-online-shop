# Generated by Django 5.1.4 on 2025-01-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_returnedproducts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnedproducts',
            name='additional_info',
        ),
        migrations.AlterField(
            model_name='returnedproducts',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
