# Generated by Django 4.2.6 on 2024-02-29 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='eamil_active',
            field=models.BooleanField(default=False, verbose_name='邮箱激活状态'),
        ),
    ]
