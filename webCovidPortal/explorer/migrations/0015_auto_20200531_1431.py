# Generated by Django 3.0.5 on 2020-05-31 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0014_auto_20200531_1354'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NomenClaturePositions',
            new_name='NomenclaturePosition',
        ),
        migrations.RemoveField(
            model_name='nomenclature',
            name='protein',
        ),
    ]
