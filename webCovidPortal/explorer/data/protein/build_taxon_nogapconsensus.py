import numpy as np, pandas as pd;
import os, sys, re;
import logging;
################################################################################
alignment_root = os.path.join('.','alignments');
alignment = "20200613";
alignment_path = os.path.join(alignment_root, str(alignment));

prealign_path = os.path.join(alignment_path,'prealign');
tax_aligned_path = os.path.join(alignment_path,'tax_aligned');
ngs_filename = alignment+"_nongapconsensus.fasta";
logfile = os.path.join('.','build_taxon_nogapconsensus.log');
################################################################################
with open(logfile, 'w') as fh:
    pass;
logging.basicConfig(
    filename=logfile,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%s'
);
# logging.info("Begin clustalo alignment run using EMBL server.");
# logging.info("Prealign path: "+prealign_path);
# logging.info("Taxon-aligned path: "+tax_aligned_path);
################################################################################
def loadFASTA(fh):
    seqs = {};
    current = "";
    for l in fh.read().split('\n'):
        if len(l)<=1: continue;
        if l[0]=='>': current = l[1:];
        else:
            if current in seqs.keys():
                seqs[current] += str(l);
            else:
                seqs[current] = str(l);
    return pd.Series(seqs, dtype=str).drop(index=[''], errors='ignore');

def formatFASTA(seqs, sequence_split_length=80):
    buff = [];
    for i in seqs.index:
        buff.append(">" + str(i));
        buff += [
            seqs[i][p:p+sequence_split_length] for p in range(0,len(seqs[i]),sequence_split_length)
        ];
    return '\n'.join(buff);
################################################################################
# load taxon alignment files
nongap_consensus = [];
for name in os.listdir(tax_aligned_path):
    base, ext = os.path.splitext(name);
    if ext=='.fasta':
        tax_batch, fmt = base.split('.');
        taxon_id, batch = tax_batch.split('_');
        with open( os.path.join(tax_aligned_path, name) ) as fh:
            seqs = loadFASTA(fh);
        print(os.path.join(tax_aligned_path),name);

        if len(seqs)>2:
            # split and generate non-gap consensus: most prevalent non-gap residue
            seqs = pd.DataFrame([ list(r) for r in seqs], index=seqs.index);
            seqs = seqs.replace('-',np.nan);
            # mode() ignores NaN which not represent the gaps.
            ngs = pd.Series([ dat.mode().values[0] for c,dat in seqs.iteritems() ]);
            nongap_consensus.append({
                'seq': ''.join(ngs),
                'taxon_id': taxon_id,
                'batch': batch,
                'seqid': 'TAXBATCH:'+taxon_id+"_"+str(batch),
                'taxon_aligned': name,
            });
        else:
            for acc,seq in seqs.iteritems():
                nongap_consensus.append({
                    'seq': seq,
                    'taxon_id': taxon_id,
                    'batch': batch,
                    'seqid': 'ACCESSION:'+acc,
                    'taxon_aligned': name,
                });
nongap_consensus = pd.DataFrame(nongap_consensus).set_index('seqid');
fasta = formatFASTA(nongap_consensus['seq']);
with open( os.path.join(tax_aligned_path, ngs_filename),'w') as fh:
    fh.write(fasta);
print("Wrote to "+os.path.join(tax_aligned_path, ngs_filename));
