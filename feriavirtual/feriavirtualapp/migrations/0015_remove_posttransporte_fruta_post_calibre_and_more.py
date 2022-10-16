# Generated by Django 4.1 on 2022-10-16 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0014_delete_estadopr_rename_fruta_post_producto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttransporte',
            name='fruta',
        ),
        migrations.AddField(
            model_name='post',
            name='calibre',
            field=models.CharField(choices=[('1', 'Segunda'), ('2', 'Primera'), ('3', 'Extra ')], default='1', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='posttransporte',
            name='producto',
            field=models.CharField(choices=[('1', 'Cerezas '), ('2', 'Uvas'), ('3', 'Arándanos '), ('4', 'Nueces'), ('5', 'Manzana'), ('6', 'Ciruela'), ('7', 'Peras'), ('9', 'Durazno'), ('11', 'Frutilla'), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Naranja'), ('16', 'Sandia '), ('17', 'Melón'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='calibre',
            field=models.CharField(choices=[('1', 'Cerezas '), ('2', 'Uvas'), ('3', 'Arándanos '), ('4', 'Nueces'), ('5', 'Manzana'), ('6', 'Ciruela'), ('7', 'Peras'), ('9', 'Durazno'), ('11', 'Frutilla'), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Naranja'), ('16', 'Sandia '), ('17', 'Melón'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='producto',
            field=models.CharField(choices=[('1', 'Cerezas '), ('2', 'Uvas'), ('3', 'Arándanos '), ('4', 'Nueces'), ('5', 'Manzana'), ('6', 'Ciruela'), ('7', 'Peras'), ('9', 'Durazno'), ('11', 'Frutilla'), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Naranja'), ('16', 'Sandia '), ('17', 'Melón'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='producto',
            field=models.CharField(choices=[('1', 'Cerezas '), ('2', 'Uvas'), ('3', 'Arándanos '), ('4', 'Nueces'), ('5', 'Manzana'), ('6', 'Ciruela'), ('7', 'Peras'), ('9', 'Durazno'), ('11', 'Frutilla'), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Naranja'), ('16', 'Sandia '), ('17', 'Melón'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana')], max_length=50, null=True),
        ),
    ]