import os, sys, numpy as np, pandas as pd;
from covidPortalApp.models import *
from covidPortalApp.models import Taxon

def loadTaxa():
    taxa = []

    df = pd.read_csv("data/db_inserts/Taxonomy_parsed.csv");
    cols = df.columns.tolist();

    for field in Taxon._meta.fields:
        print(field)
        if type(field) != type(models.AutoField()):
            if not field.name in cols:
                raise Exception(
                    ffn+" has no '"+field.name+"' column");

    for i,r in df.iterrows():
        try:
            taxa.append(
                Taxon(
                    gb_taxon_id=r['gb_taxon_id'],
                    leaf=r['leaf'],
                    path=r['path'],
                    name=r['name'],
                    level=r['level']
                )
            )

        except Exception as e:
            print(e+" "+r);
            sys.exit();

    print("Added "+str(len(df))+" taxa from data/db_inserts/Taxonomy_parsed.csv");

    # currently overwrite mode always
    for t in taxa:
        try:
            try:
                dbt = Taxon.objects.get(gb_taxon_id=t.gb_taxon_id)
                dbt.leaf = t.leaf
                dbt.path = t.path
                dbt.name = t.name
                dbt.level = t.level
                dbt.save()
            except:
                t.save();
            print(str(t.gb_taxon_id)+" "+str(t.name)+" OK");
        except Exception as e:
            print(str(e)+" "+str(t)+" "+str(t.gb_taxon_id));
            raise;
loadTaxa()
