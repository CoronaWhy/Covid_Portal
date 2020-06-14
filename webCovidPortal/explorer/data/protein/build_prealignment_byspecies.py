import sys, os;
import numpy as np, pandas as pd;
import logging;
################################################################################
infile = "extract_protein_sequences_output.csv";
batch_size = 2000; # sequence batch size per fasta file
taxon_file = os.path.join('..','taxon','taxonomy_parsed.csv');
logfile = os.path.join('.','build_prealignment_byspecies.log');
lw = 80;
alignment = "20200613"; # name of the alignment
prealign_folder = os.path.join('alignments',str(alignment),'prealign');
################################################################################
if not os.path.isdir(prealign_folder):
    os.makedirs(prealign_folder);
################################################################################
with open(logfile, 'w') as fh:
    pass;
logging.basicConfig(
    filename=logfile,
    level=logging.DEBUG,
    format='%(asctime)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%s'
);
################################################################################
# get sequences
seqs = pd.read_csv(infile);
# group leaf taxon ids by species
taxa = pd.read_csv(taxon_file);
taxa['gb_taxon_id'] = taxa['gb_taxon_id'].astype(str);
#------------------------------------------------------------------------------#
# An attempt to isolate distinct species from taxon list, work on this later.
# get species, squares are teminal species endpoints
species = taxa[
    (taxa['level']=='species') &
    (taxa['type']=='circle')];
#------------------------------------------------------------------------------#
# this is being done manually because NCBI tree has multiple levels labeled as
# species, resulting in massive duplication of sequences.
groupby_taxon = [
    'Betacoronavirus 1',
    'China Rattus coronavirus HKU24',
    'Human coronavirus HKU1',
    'Murine coronavirus',
    'unclassified Embecovirus',
    'Bat Hp-betacoronavirus Zhejiang2013',
    'unclassified Hibecovirus',
    'Hedgehog coronavirus 1',
    'Middle East respiratory syndrome-related coronavirus',
    'Pipistrellus bat coronavirus HKU5',
    'Tylonycteris bat coronavirus HKU4',
    'unclassified Merbecovirus',
    'Rousettus bat coronavirus GCCDC1',
    'Rousettus bat coronavirus HKU9',
    'unclassified Nobecovirus',
    'Severe acute respiratory syndrome-related coronavirus',
    'unclassified Sarbecovirus',
    'unclassified Betacoronavirus'
];
species = taxa[taxa['name'].isin(groupby_taxon)];
# print("\n".join(list(species['path']+"."+species['gb_taxon_id'].astype(str))));
# print(species);
# sys.exit();
#------------------------------------------------------------------------------#
# get paths to the species, these will be roots to the leafs
sp_paths = species['path'];
sp_taxon_ids = {}; # list of taxon ids for each species by taxon id
total_seqs = 0;
# this is being done manually because NCBI tree has multiple levels defined as "species", resulting in massive duplication of sequences.

accs = []; # to ensure each accession is processed only once
for i,sp in species.iterrows():
    spp = sp['path']+"."+str(sp['gb_taxon_id']);
    sp_leafs = taxa[
        (taxa['path'].str.contains(spp)) &
        (taxa['leaf']==True)];
    logging.info(sp['gb_taxon_id']+" "+sp['name']);
    logging.info(str(len(sp_leafs))+" leafs.");
    # if there are no leafs there are no sequences
    if len(sp_leafs)<=0: continue;
    # get matching sequences
    leaf_seqs = seqs[seqs['taxon_id'].isin(sp_leafs['gb_taxon_id'])];
    total_seqs += len(leaf_seqs);
    logging.info(str(len(leaf_seqs))+" sequences.");
    # generate output file basename
    outfile_base = sp['gb_taxon_id']+"_";
    # batch
    batch_size = 200; #batch size, in number of sequences
    for i in range(0, len(sp_leafs), batch_size):
        seq_batch = leaf_seqs.iloc[i:i+batch_size];
        if len(seq_batch)<=0: break;
        outfile = outfile_base+str(int(i/batch_size)+1)+".fasta";
        # process sequences into fasta format
        fasta = [];
        for i,r in seq_batch.iterrows():
            name = r['version'];
            seq = r['seq'];
            if name in accs:
                raise Exception("Duplicate accession: "+str(name));
            accs.append(name);
            if len(seq)<500: continue; # skip short sequences
            fasta.append(">"+name);
            fasta = fasta + [
                seq[i:i+(lw-1)] for i in range(0, len(seq), (lw-1))
            ];
        outffn = os.path.join(prealign_folder, outfile);
        with open(outffn,'w') as fh:
            fh.write("\n".join(fasta));
        logging.info("Wrote "+outffn);
logging.info("Processed a total of "+str(total_seqs)+" sequences.");
