# Generated by Django 4.0.4 on 2022-07-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vender',
            name='products',
            field=models.CharField(default='none', max_length=500),
        ),
    ]
