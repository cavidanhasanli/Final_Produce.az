# Generated by Django 3.0.2 on 2020-01-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodsApp', '0002_auto_20200109_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='email',
            field=models.EmailField(max_length=60, null=True),
        ),
    ]
