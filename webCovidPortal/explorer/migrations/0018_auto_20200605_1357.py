# Generated by Django 3.0.5 on 2020-06-05 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0017_auto_20200605_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureAtom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atom', models.CharField(max_length=5)),
                ('element', models.CharField(max_length=5)),
                ('charge', models.IntegerField()),
                ('occupancy', models.FloatField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='StructureChainResidue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resix', models.IntegerField()),
                ('resid', models.IntegerField()),
                ('resn', models.CharField(max_length=1)),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.StructureChain')),
            ],
        ),
        migrations.DeleteModel(
            name='StructureChainAtom',
        ),
        migrations.AddField(
            model_name='structureatom',
            name='residue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.StructureChainResidue'),
        ),
    ]
