# Generated by Django 4.0.4 on 2022-08-25 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_remove_orders_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='vender_id',
            field=models.IntegerField(null=True),
        ),
    ]