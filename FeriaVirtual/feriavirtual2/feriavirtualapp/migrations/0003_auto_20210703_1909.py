# Generated by Django 3.1.2 on 2021-07-03 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0002_post_cantidad_ingresada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='cantidad_ingresada',
        ),
        migrations.AddField(
            model_name='relacion',
            name='cantidad_ingresada',
            field=models.IntegerField(default=0),
        ),
    ]
