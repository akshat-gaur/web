# Generated by Django 4.0.4 on 2022-09-03 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_alter_products_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='Availability',
            field=models.BooleanField(default=True, verbose_name='Is_avilable'),
        ),
    ]
