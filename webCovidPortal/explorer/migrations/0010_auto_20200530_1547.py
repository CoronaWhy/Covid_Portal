# Generated by Django 3.0.5 on 2020-05-30 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0009_epitope'),
    ]

    operations = [
        migrations.RenameField(
            model_name='epitope',
            old_name='protein_id',
            new_name='protein',
        ),
    ]
