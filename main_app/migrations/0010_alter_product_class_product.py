# Generated by Django 4.0.4 on 2022-08-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_products_product_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_class',
            name='product',
            field=models.ManyToManyField(blank=True, to='main_app.products'),
        ),
    ]
