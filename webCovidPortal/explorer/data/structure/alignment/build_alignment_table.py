import numpy as np, pandas as pd;
import re, sys;
################################################################################
infile = "./conformed_alignments.csv";
out_alignment_table = "./conformed_alignment_table.csv";
################################################################################
rx_pdbchain = r'PDB\.(?P<pdb_id>.+)?\:(?P<chain>[A-Z])$';
seqs = pd.read_csv(infile);
# extract pdb/chain info where available in accession, for trimming and identity
seqs = pd.concat(
    [
        seqs,
        seqs['accession'].str.extract(rx_pdbchain)
    ], axis=1, sort=False);
# trim to only pdb sequences
seqs = seqs[seqs['pdb_id'].notnull()];
# split and index gapped sequence residues
sp_seqs = pd.DataFrame(
    [ list(s) for s in seqs['sequence'] ],
    index=seqs['accession']
);
# normalize empties to nan
sp_seqs = sp_seqs.fillna(np.nan);
sp_seqs = sp_seqs.replace('-', np.nan);

# build lookup table for each sequence
table = [];
for accession,seq in sp_seqs.iterrows():
    print("Processing "+accession);
    # get sequence record
    seq_record = seqs[seqs['accession']==accession].iloc[0];
    # trim gaps while preserving resaln indices
    ungapped = seq[seq.notnull()].copy();
    # enumerating gap-trimmed index gives resix and resaln
    for resix, resaln in enumerate(ungapped.index):
        table.append({
            'alignment': seq_record['alignment'],
            'pdb_id': seq_record['pdb_id'],
            'chain': seq_record['chain'],
            'resix': resix,
            'resaln': resaln,
        });
        
# dataframe and store
table = pd.DataFrame(table);
print("Writing "+out_alignment_table);
table.to_csv(out_alignment_table);
