# Generated by Django 3.2 on 2022-10-04 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudcompra',
            name='cantidad_actual',
            field=models.IntegerField(default=0),
        ),
    ]
