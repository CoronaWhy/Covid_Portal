# Generated by Django 2.2.13 on 2020-06-22 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covidPortalApp', '0003_auto_20200605_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epitope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IEDB_ID', models.CharField(max_length=50)),
                ('sequence', models.TextField()),
                ('offset', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EpitopeExperiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=75)),
                ('assay_type', models.CharField(max_length=50)),
                ('assay_result', models.CharField(max_length=50)),
                ('mhc_allele', models.CharField(max_length=30)),
                ('mhc_class', models.CharField(max_length=30)),
                ('exp_method', models.CharField(max_length=100)),
                ('measurement_type', models.CharField(max_length=100)),
                ('epitope', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Epitope')),
            ],
        ),
        migrations.CreateModel(
            name='SequenceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=50, unique=True)),
                ('organism', models.CharField(max_length=200)),
                ('collection_date', models.DateTimeField(null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('host', models.CharField(max_length=100, null=True)),
                ('isolation_source', models.CharField(max_length=100, null=True)),
                ('isolate', models.CharField(max_length=100, null=True)),
                ('coded_by', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdb_id', models.CharField(max_length=10, unique=True)),
                ('taxon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Taxon')),
            ],
        ),
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
            name='StructureChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StructureChainResidue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resix', models.IntegerField()),
                ('resid', models.IntegerField()),
                ('resn', models.CharField(max_length=1)),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.StructureChain')),
            ],
        ),
        migrations.CreateModel(
            name='StructureChainSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField()),
                ('sequence', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='NomenClaturePositions',
            new_name='NomenclaturePosition',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='commentType',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='uploadFolder',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='coviduser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='gene',
            name='strain',
        ),
        migrations.RemoveField(
            model_name='logfile',
            name='uploadFolder',
        ),
        migrations.DeleteModel(
            name='Mutation',
        ),
        migrations.RemoveField(
            model_name='processstep',
            name='process',
        ),
        migrations.RemoveField(
            model_name='proteinsequence',
            name='alignment',
        ),
        migrations.RemoveField(
            model_name='proteinsequence',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='proteinsequence',
            name='taxon',
        ),
        migrations.RemoveField(
            model_name='strain',
            name='species',
        ),
        migrations.RemoveField(
            model_name='submittedjob',
            name='jobStatusCode',
        ),
        migrations.RemoveField(
            model_name='submittedjob',
            name='process',
        ),
        migrations.RemoveField(
            model_name='submittedjob',
            name='submittedBy',
        ),
        migrations.RemoveField(
            model_name='submittedjob',
            name='uploadeFolder',
        ),
        migrations.RemoveField(
            model_name='uploadfolder',
            name='user',
        ),
        migrations.RenameField(
            model_name='sequence',
            old_name='sequenceString',
            new_name='sequence',
        ),
        migrations.RemoveField(
            model_name='nomenclature',
            name='alignment',
        ),
        migrations.RemoveField(
            model_name='nomenclature',
            name='reference_proteinSequence',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='extrez_id',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='uniprot_id',
        ),
        migrations.RemoveField(
            model_name='sequence',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sequence',
            name='strain',
        ),
        migrations.AddField(
            model_name='alignment',
            name='protein',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Protein'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='reference',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Sequence'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='alignment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Alignment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='offset',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='protein',
            name='mesh_id',
            field=models.CharField(default=None, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentType',
        ),
        migrations.DeleteModel(
            name='CovidUser',
        ),
        migrations.DeleteModel(
            name='Gene',
        ),
        migrations.DeleteModel(
            name='JobStatusCode',
        ),
        migrations.DeleteModel(
            name='LogFile',
        ),
        migrations.DeleteModel(
            name='Process',
        ),
        migrations.DeleteModel(
            name='ProcessStep',
        ),
        migrations.DeleteModel(
            name='ProteinSequence',
        ),
        migrations.DeleteModel(
            name='Species',
        ),
        migrations.DeleteModel(
            name='Strain',
        ),
        migrations.DeleteModel(
            name='SubmittedJob',
        ),
        migrations.DeleteModel(
            name='UploadFolder',
        ),
        migrations.AddField(
            model_name='structurechainsequence',
            name='alignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Alignment'),
        ),
        migrations.AddField(
            model_name='structurechainsequence',
            name='chain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.StructureChain'),
        ),
        migrations.AddField(
            model_name='structurechain',
            name='protein',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Protein'),
        ),
        migrations.AddField(
            model_name='structurechain',
            name='structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Structure'),
        ),
        migrations.AddField(
            model_name='structureatom',
            name='residue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.StructureChainResidue'),
        ),
        migrations.AddField(
            model_name='sequencerecord',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Protein'),
        ),
        migrations.AddField(
            model_name='sequencerecord',
            name='taxon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Taxon'),
        ),
        migrations.AddField(
            model_name='epitope',
            name='alignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Alignment'),
        ),
        migrations.AddField(
            model_name='epitope',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.Protein'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='sequence_record',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='covidPortalApp.SequenceRecord'),
            preserve_default=False,
        ),
    ]