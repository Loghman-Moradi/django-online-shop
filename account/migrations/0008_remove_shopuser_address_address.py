# Generated by Django 5.1.4 on 2025-01-10 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_shopuser_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='address',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=11)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('plate', models.CharField(max_length=10)),
                ('unit', models.CharField(max_length=10)),
                ('postal_code', models.CharField(max_length=10)),
                ('address_line', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
    ]
