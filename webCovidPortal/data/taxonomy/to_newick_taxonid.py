import csv;
import sys;
import numpy as np, pandas as pd;
from collections import defaultdict;
from pprint import pprint;
################################################################################
infile = "Taxonomy_parsed.csv";
outfile = "Taxonomy_newick_taxid.newick";
################################################################################
# FROM https://stackoverflow.com/questions/26146623/convert-csv-to-newick-tree
# USER Mark Watson
def tree(): return defaultdict(tree)

def tree_add(t, path):
  for node in path:
    t = t[node];

def pprint_tree(tree_instance):
    def dicts(t): return {k: dicts(t[k]) for k in t};
    pprint(dicts(tree_instance));

def csv_to_tree(input):
    t = tree();
    for row in csv.reader(input):
        tree_add(t, row);
    return t;

def tree_to_newick(root):
    items = [];
    for k,v in root.items():
        s = '';
        if len(root[k].keys()) > 0:
            sub_tree = tree_to_newick(root[k]);
            if sub_tree != '':
                s += '(' + sub_tree + ')';
        s += k;
        items.append(s);
    return ','.join(items);

def csv_to_weightless_newick(input):
    t = csv_to_tree(input);
    #pprint_tree(t)
    return tree_to_newick(t);
################################################################################
# Parse paths from taxon extract into format amenible to Mark's script
# Labels and names are the taxonomy ID, the resulting tree can be loaded into
# http://etetoolkit.org/treeview/, which will resolve the names for each leaf
# using the NCBI taxon id's.
df = pd.read_csv(infile);
df['name'] = df['name'].replace('(','[').replace(')',']');
recs = [
        r['path'].replace('.',',')+',"'+str(r['taxon_id'])+'"'
        for i,r in df.iterrows() ];
# Build
newick = csv_to_weightless_newick(recs);
# Output
with open(outfile,'w') as fh:
    fh.write(newick);
# fin.
