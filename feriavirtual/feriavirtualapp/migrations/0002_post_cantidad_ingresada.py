# Generated by Django 3.1.2 on 2021-07-03 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cantidad_ingresada',
            field=models.IntegerField(default=0),
        ),
    ]