# Generated by Django 4.0.4 on 2022-09-03 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_alter_products_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='related_products',
        ),
        migrations.RemoveField(
            model_name='products',
            name='reveiw',
        ),
        migrations.AlterField(
            model_name='products',
            name='vender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.vender'),
        ),
    ]
