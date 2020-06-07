import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Nomenclature, NomenclaturePosition;
from explorer.models import Protein, Sequence;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):

        # field list
        fields = {
            'major':int,
            'minor':int,
            'protein':str,
            'reference':str,
            'alignment_name':str,
            'name':str,
        };

        records = []; # list of taxon dataframes to concatenate
        for ffn in options['file']:
            # load file into dataframe
            if not os.path.isfile(ffn):
                self.stdout.write(ffn+" not found...");
                continue;
            df = pd.read_csv(ffn);
            cols = df.columns.tolist();

            # check fields
            for field in fields:
                if not field in cols:
                    raise Exception(ffn+" has no '"+field+"' column");

            records.append( df[fields] );
            self.stdout.write("Added "+str(len(df))+" records from "+ffn);
        records = pd.concat(records);
        records['alignment_name'] = records['alignment_name'].astype(str);


        # get protein objects
        pros = {};
        for p in Protein.objects.filter(
            mesh_id__in=(records['protein'].unique())
        ):
            pros[p.mesh_id] = p;

        # get sequence reference using alignment and reference accession
        sep = "~`_`~";
        records['_pra_key'] =           \
            records['protein']+sep+     \
            records['reference']+sep+   \
            records['alignment_name'];

        seqs_by_nn = {};
        # validate nomenclature multiplicity by name and get references
        for nomname in records['name'].unique():
            ss = records[records['name']==nomname];
            if len(ss['protein'].unique())!=1:
                raise Exception(str(nomname)+
                    " can only have one protein.");
            if len(ss['reference'].unique())!=1:
                raise Exception(str(nomname)+
                    " can only have one reference.");
            if len(ss['alignment_name'].unique())!=1:
                raise Exception(str(nomname)+
                    " can only have one alignment name.");
            if len(ss['_pra_key'].unique())!=1:
                raise Exception(str(nomname)+
                    " can only have one combination of alignment,"+
                    " protein and reference.");
            # get reference sequence object
            pra = ss.loc[0,'_pra_key'].split(sep);
            seq = Sequence.objects.get(
                sequence_record__protein__mesh_id=(pra[0]),
                sequence_record__accession=(pra[1]),
                alignment__name=(pra[2])
            );
            seqs_by_nn[nomname] = seq;

        # create nomenclature and nomenclatureposition objects
        try:
            with transaction.atomic():
                for nn in records['name'].unique():
                    # create nomenclature object
                    nom, created = Nomenclature.objects.get_or_create(
                        name = nn,
                        # date_created = AUTOGENERATED
                        reference = seqs_by_nn[nn]
                    );
                    if created==False:
                        raise Exception(str(nom)+" exists");

                    # create nomenclature positions
                    ss = records[records['name']==nn];
                    pix = 0;
                    for i,r in ss.iterrows():
                        npos, created = \
                            NomenclaturePosition.objects.get_or_create(
                                index = pix,
                                nomenclature = nom,
                                major = int(r['major']),
                                minor = int(r['minor']),
                            );
                        if created==False:
                            raise Exception(str(nom)+
                                " position "+str(int(r['major']))+
                                "."+str(int(r['minor']))+" exists.");
                        else:
                            self.stdout.write(str(nom)+
                                " position "+str(int(r['major']))+
                                "."+str(int(r['minor']))+" OK.");
                        pix += 1;
        except: raise;