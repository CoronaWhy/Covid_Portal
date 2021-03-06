# Generated by Django 3.0.5 on 2020-05-30 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0008_auto_20200529_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epitope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IEDB_ID', models.CharField(max_length=50)),
                ('sequence', models.TextField()),
                ('offset', models.IntegerField()),
                ('alignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Alignment')),
                ('protein_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Protein')),
            ],
        ),
    ]
