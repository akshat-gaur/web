# Generated by Django 4.0.4 on 2022-08-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_comments_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='date_time',
            field=models.DateTimeField(default='none'),
        ),
    ]
