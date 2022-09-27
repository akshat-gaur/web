# Generated by Django 4.0.4 on 2022-09-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0027_alter_product_class_class_img_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='history',
        ),
        migrations.RemoveField(
            model_name='users',
            name='preference',
        ),
        migrations.AddField(
            model_name='users',
            name='b_history',
            field=models.ManyToManyField(blank=True, null=True, related_name='brouser_h', to='main_app.products'),
        ),
        migrations.AddField(
            model_name='users',
            name='order_history',
            field=models.ManyToManyField(blank=True, null=True, related_name='orders_h', to='main_app.products'),
        ),
    ]