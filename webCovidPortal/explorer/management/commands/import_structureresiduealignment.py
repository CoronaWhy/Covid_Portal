import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from django.db.models import Value as V;
from django.db.models.functions import Concat;
from explorer.models import Alignment, Structure, StructureChain, StructureChainSequence, StructureChainResidue, StructureChainResidueAlignment;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):

        # field list
        fields = {
            'pdb_id'        : str,
            'chain'         : str,
            'alignment'     : str,
            'resix'         : int,
            'resaln'        : int,
        };

        records = [];
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
        records['_pdb_chain'] = records['pdb_id']+"."+records['chain'];

        # get alignments
        aligns = {};
        for a in Alignment.objects.filter(
            name__in=(records['alignment'].unique())
        ):
            aligns[a.name] = a;

        # get foreign id's and store at the same time.
        try:
            with transaction.atomic():

                for pdbchain in records['_pdb_chain'].unique():
                    ss = records[records['_pdb_chain']==pdbchain];
                    # only permit one alignment per sequence/chain for now
                    if len(ss['alignment'].unique())!=1:
                        raise Exception("Alignment "+alignment+" is either "+
                            "missing or multiple alignments are specified for "+
                            pdbchain);
                    ref = ss.iloc[0];

                    # get sequence from database with alignment
                    seq = StructureChainSequence.objects.get(
                        chain__structure__pdb_id=ref['pdb_id'],
                        chain__name=ref['chain'],
                        alignment=aligns[str(ref['alignment'])],
                    );

                    # dict of resix's
                    resaln_by_resix = dict(zip(ss['resix'],ss['resaln']));

                    # get residues
                    for res in StructureChainResidue.objects.filter(
                        chain__structure__pdb_id=ref['pdb_id'],
                        chain__name=ref['chain'],
                    ):
                        resaln, created = \
                        StructureChainResidueAlignment.objects.get_or_create(
                            structure_chain_sequence = seq,
                            residue = res,
                            resaln = resaln_by_resix[res.resix]
                        );
                        if created==False:
                            raise Exception(ref['_pdb_chain']+" already exists");
        except: raise;
        return;

# fin.
