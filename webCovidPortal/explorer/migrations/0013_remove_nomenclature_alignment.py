# Generated by Django 3.0.5 on 2020-05-31 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0012_auto_20200531_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomenclature',
            name='alignment',
        ),
    ]
