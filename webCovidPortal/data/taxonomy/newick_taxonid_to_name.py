import numpy as np, pandas as pd;
################################################################################
datafile = "Taxonomy_parsed.csv";
newickfile = "Taxonomy_newick_taxid.tre";
outfile = "Taxonomy_newick_byname.tre";
################################################################################

df = pd.read_csv(datafile);
# index df by taxon id
df['taxon_id'] = df['taxon_id'].astype(str);
df.index = df['taxon_id'];
# load newick string
with open(newickfile,'r') as fh:
    newick = fh.readlines()[0];
# replace
for i,r in df.iterrows():
    name = r['name'];
    name = name.replace('(','-').replace(')','-').replace(' ','-');
    newick = newick.replace(i,name);
# write
with open(outfile,'w') as fh:
    fh.write(newick);
