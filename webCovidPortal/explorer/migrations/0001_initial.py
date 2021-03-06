# Generated by Django 3.0.5 on 2020-05-28 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('alignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Alignment')),
            ],
        ),
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isolate', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mesh_id', models.CharField(max_length=200)),
                ('organism_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Organism')),
            ],
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gb_taxon_id', models.CharField(max_length=20)),
                ('leaf', models.BooleanField()),
                ('path', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProteinSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=50)),
                ('collection_date', models.DateTimeField(null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('host', models.CharField(max_length=100, null=True)),
                ('isolation_source', models.CharField(max_length=100, null=True)),
                ('coded_by', models.CharField(max_length=50, null=True)),
                ('sequence', models.TextField()),
                ('offset', models.IntegerField()),
                ('alignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Alignment')),
                ('protein_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Protein')),
            ],
        ),
        migrations.AddField(
            model_name='organism',
            name='taxon_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Taxon'),
        ),
        migrations.CreateModel(
            name='NomenClaturePositions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('major', models.IntegerField()),
                ('minor', models.IntegerField()),
                ('nomenclature_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorer.Nomenclature')),
            ],
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='reference_proteinSequence_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='explorer.ProteinSequence'),
        ),
    ]
