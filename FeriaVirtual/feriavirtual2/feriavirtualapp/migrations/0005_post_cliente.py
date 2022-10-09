# Generated by Django 3.1.2 on 2021-07-04 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0004_notificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Cliente', to='feriavirtualapp.user'),
            preserve_default=False,
        ),
    ]
