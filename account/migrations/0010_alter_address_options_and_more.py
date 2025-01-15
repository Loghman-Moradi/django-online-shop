# Generated by Django 5.1.4 on 2025-01-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_address_unit_alter_address_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-address_line'], 'verbose_name': 'آدرس', 'verbose_name_plural': 'آدرس ها'},
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['-address_line'], name='account_add_address_58bb7c_idx'),
        ),
    ]
