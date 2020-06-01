import numpy as np, pandas as pd;
infile = "Taxonomy_parsed.csv";
outfile = "txid-search-list.csv";
df = pd.read_csv(infile);
df['pcount'] = df['pcount'].astype(int);
df = df[
    (df['leafnode']=="leaf") &
    (df['pcount']>0)
];
df = df[['taxon_id','name']];
df.to_csv(outfile);
