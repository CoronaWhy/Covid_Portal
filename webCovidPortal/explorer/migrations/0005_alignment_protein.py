# Generated by Django 3.0.5 on 2020-05-29 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0004_auto_20200529_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='alignment',
            name='protein',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='explorer.Protein'),
            preserve_default=False,
        ),
    ]
