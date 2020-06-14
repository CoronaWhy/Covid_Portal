import numpy as np, pandas as pd;
import os, sys, time, re;
import clustaloAPI;
import logging;
################################################################################
alignment_root = os.path.join('.','alignments');
alignment = "20200613";
alignment_path = os.path.join(alignment_root, str(alignment));

prealign_path = os.path.join(alignment_path,'prealign');
tax_aligned_path = os.path.join(alignment_path,'tax_aligned');
logfile = os.path.join('.','run_clustalo_alignment.log');
################################################################################
with open(logfile, 'w') as fh:
    pass;
logging.basicConfig(
    filename=logfile,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%s'
);
logging.info("Begin clustalo alignment run using EMBL server.");
logging.info("Prealign path: "+prealign_path);
logging.info("Taxon-aligned path: "+tax_aligned_path);
################################################################################
if not os.path.isdir(tax_aligned_path):
    os.makedirs(tax_aligned_path);
    logging.info("Created "+tax_aligned_path);
################################################################################
# get all prealign files
prealign_files = [];
for name in os.listdir(prealign_path):
    base, ext = os.path.splitext(name);
    if ext=='.fasta':
        taxon_id, batch = base.split('_');
        prealign_files.append({
            'taxon_id': taxon_id,
            'batch': int(batch),
            'file': name,
            'path': prealign_path,
        });
logging.info("Prealign files:");
for r in prealign_files:
    logging.info("\t"+r['file']);
################################################################################
# load and align
rx_seq_header = re.compile('[\n]?\>.+?\n');
for i,r in enumerate(prealign_files):
    seqs = clustaloAPI.readFile(os.path.join(r['path'],r['file']));
    # how many sequences do we have?
    seq_count = len(re.findall(rx_seq_header, seqs));
    print(os.path.join(r['path'],r['file']));
    logging.info(r['file'].ljust(15)+": "+str(seq_count)+" sequences.");
    if seq_count<=2: # pairwise alignment
        # just put these into the aligned folder as fasta and they will be
        # added to the final alignment
        outfile = r['taxon_id']+'_'+str(r['batch'])+'.aln-fasta.fasta';
        with open(os.path.join(tax_aligned_path,outfile),'w') as fh:
            fh.write(seqs);
        logging.info(r['file'].ljust(15)+": Multiple aligment not needed, copied to "+outfile);
    else:
        jobId = clustaloAPI.serviceRun(
            'alkali.blue@gmail.com',
            'covrun',
            seqs,
            outfmt='fa', # for fasta
            guidetreeout=False,
            dismatout=False,
        );
        logging.info(r['file'].ljust(15)+": JobId "+jobId);
        time.sleep(clustaloAPI.pollFreq);
        clustaloAPI.getResult(
            jobId,
            outfile=r['taxon_id']+'_'+str(r['batch']),
            path=tax_aligned_path,
        );
        logging.info(r['file'].ljust(15)+": Complete.");
    time.sleep(clustaloAPI.pollFreq);
    # print(seqs);
################################################################################
