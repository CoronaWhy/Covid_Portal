import numpy as np, pandas as pd;
import os, sys, re, logging, time;
import clustaloAPI;
################################################################################
# clustalO settings
clustaloAPI.outputLevel = 0;
# globals
email               = "alkali.blue@gmail.com";
sequence_extract    = "extract_protein_sequences_output.csv";
taxon_extract       = os.path.join('..','taxon','taxonomy_parsed.csv');
fasta_linewidth     = 80;
alignment_batchsize = 2000;
alignment           = '20200613';
alignment_root      = os.path.join('alignments');
alignment_path      = os.path.join(alignment_root, alignment);
taxon_prealign_path = os.path.join(alignment_path, 'taxon_prealign');
taxon_align_path    = os.path.join(alignment_path, 'taxon_aligned');
nongap_cons_path    = os.path.join(alignment_path, 'nongap_consensus');
prealign_nongap_cons_file       = "prealign_nongap_consensus.fasta";
aligned_nongap_cons_filebase    = "nongap_consensus";
logfile             = os.path.join('.','align_sequences.log');
minimum_sequence_length = 500;
rx_fasta_header     = re.compile('[\n]?\>.+?\n');
# functional switches
regen_taxon_prealignments   = False;
realign_taxon_batches       = False;
regen_prealign_nongap_cons  = False;
realign_nongap_cons         = True;
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
# filename constructors
def filename_taxon_prealign(taxon_id, batch, ext=".fasta"):
    return str(taxon_id)+"_"+str(batch)+ext;

def filename_taxon_align(taxon_id, batch, ext=".fasta"):
    return str(taxon_id)+"_"+str(batch)+".aln-fasta"+ext;
################################################################################
# fasta formatting
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

def batchFASTA(seqs, batch_size=2000, linewidth=80):
    all_fastas = [];
    for i in range(0, len(seqs), batch_size):
        seq_batch = seqs.iloc[i:i+batch_size];
        if len(seq_batch)<=0: break;
        fasta = [];
        for six,seq in seq_batch.iteritems():
            fasta.append(">"+str(six));
            fasta = fasta + [
                seq[i:i+(linewidth-1)]
                for i in range(0, len(seq), (linewidth-1))
            ];
        all_fastas.append("\n".join(fasta));
    return all_fastas;
################################################################################
def getTaxonLevel(taxa,level=2):
    z = [ len(p.split('.')) for p in taxa['path'].astype(str) ];
    z = pd.Series(z, index=taxa.index);
    z = z[z==level];
    return taxa.loc[z.index];
################################################################################

################################################################################
if __name__=="__main__":
    # get taxon ids by level
    taxa = pd.read_csv(taxon_extract);
    taxa['gb_taxon_id'] = taxa['gb_taxon_id'].astype(str);
    groupTaxa = getTaxonLevel(taxa,level=2); # species (roughly)
    # FOR DEBUG ----------------------------------------------------------------
    # groupTaxa = taxa[taxa['gb_taxon_id']=="290028"];
    # --------------------------------------------------------------------------
    # get sequences
    seqs = pd.read_csv(sequence_extract);
    seqs = seqs.drop_duplicates('version');
    seqs = seqs.set_index('version');
    seqs['seq_length'] = seqs['seq'].str.len();
    accs = []; # ensure each accession number is processed only once
    # makedirs where needed
    if not os.path.isdir(taxon_prealign_path):
        os.makedirs(taxon_prealign_path);
    if not os.path.isdir(taxon_align_path):
        os.makedirs(taxon_align_path);
    if not os.path.isdir(nongap_cons_path):
        os.makedirs(nongap_cons_path);
    # remove prealign nongap consensus file if needed
    ngc_prealign_ffn = os.path.join(nongap_cons_path,prealign_nongap_cons_file);
    if os.path.isfile(ngc_prealign_ffn):
        if regen_prealign_nongap_cons:
            os.remove(ngc_prealign_ffn);
            with open(ngc_prealign_ffn, 'w') as fh:
                pass;
    ############################################################################
    # Build taxon prealignment files
    ############################################################################
    for i,taxon in groupTaxa.iterrows():
        # BUILD TAXON PREALIGNMENT BATCH FILES AND ALIGN -----------------------
        # get all child leafs
        parent_path = taxon['path']+'.'+taxon['gb_taxon_id'];
        taxon_leafs = taxa[
            (taxa['path'].str.contains(parent_path)) &
            (taxa['leaf']==True)];
        # If no leafs, then no sequences, skip
        if len(taxon_leafs)<=0: continue;
        # get matching sequences and exclude short
        leaf_seqs = seqs[
            (seqs['taxon_id'].isin(taxon_leafs['gb_taxon_id'])) &
            (seqs['seq_length']>=minimum_sequence_length)];
        # build fasta files from these sequences in batches
        fastas = batchFASTA(
            leaf_seqs['seq'],
            batch_size = alignment_batchsize,
            linewidth = fasta_linewidth,
        );
        print(
                taxon['gb_taxon_id'].ljust(10)+
                str(str(len(leaf_seqs))+"/"+str(len(fastas))).ljust(10)+
                taxon['name']);
        # write batches
        for batch,fasta in enumerate(fastas):
            outfile = filename_taxon_prealign(taxon['gb_taxon_id'], batch);
            outffn = os.path.join(taxon_prealign_path, outfile);
            if os.path.isfile(outffn):
                if regen_taxon_prealignments:
                    os.remove(outffn);
                else:
                    print("--> taxon prealignment exists: "+outffn);
                    continue;
            else:
                print("--> taxon prealignment: "+outffn);
                with open(outffn, 'w') as fh:
                    fh.write(fasta);
        # ----------------------------------------------------------------------
        # run taxon alignment(s) using clustalo from EMBL-EBI
        for batch,fasta in enumerate(fastas):
            # filename that should contain the alignment results
            # written by clustaloAPI.getResults()
            expected_aligned_file = filename_taxon_align(
                taxon['gb_taxon_id'],
                batch);
            expected_ffn = os.path.join(
                taxon_align_path,
                expected_aligned_file
            );
            # quick count sequences in batch
            seq_count = len(re.findall(rx_fasta_header, fasta));
            # use prealignment file as name for run
            runname = filename_taxon_prealign(
                        taxon['gb_taxon_id'],
                        batch,
                        ext="");
            # skip or remove expected alignment result file
            if os.path.isfile(expected_ffn):
                if realign_taxon_batches:
                    os.remove(expected_ffn);
                else:
                    print("--> taxon alignment exists: "+expected_ffn);
                    continue;
            if seq_count==0:
                # if not sequences skip
                continue;
            elif seq_count<=2:
                # if one or two sequences, align with nongap consensuses
                with open(expected_ffn,'w') as fh:
                    fh.write(fasta);
            else:
                # if nore than two sequences, do multiple sequence alignment
                print("--> running alignment");
                # send request
                jobId = clustaloAPI.serviceRun(
                    email,
                    runname,
                    fasta,
                    outfmt='fa',
                    guidetreeout=False,
                    dismatout=False,
                );
                # wait
                time.sleep(clustaloAPI.pollFreq);
                # get results
                clustaloAPI.getResult(
                    # id of the job
                    jobId,
                    # oufile is just a base name that clustalo adds to
                    outfile=runname,
                    # path to store output files in
                    path=taxon_align_path,
                );
            if not os.path.isfile(expected_ffn):
                raise Exception(runname+" did not get alignment results.");
            else:
                print("--> taxon alignment: "+expected_ffn);
            # build nongap consensus for this batch ----------------------------
            # fill filename (with path) for nongap consensus
            ngc_prealign_ffn = \
                os.path.join(
                    nongap_cons_path,
                    prealign_nongap_cons_file);
            # skip if requested
            if os.path.isfile(ngc_prealign_ffn) and not regen_prealign_nongap_cons:
                print("--> nongap cons. prealign exists: "+ngc_prealign_ffn);
                continue;
            ng_consensus = {};
            # load taxon-aligned sequences
            with open(expected_ffn,'r') as fh:
                ta_seqs = loadFASTA(fh);
            if len(ta_seqs)<=0:
                print("--> no taxon alignments for nongap consensus");
                continue;
            elif len(ta_seqs)<=2:
                # two or less sequences just append the sequences
                for i,r in ta_seqs.iteritems():
                    ng_consensus['ACC:'+i] = "".join(ngc);
            else:
                # more than two sequences, do nongap consensus
                # split by character
                ngc_seqs = pd.DataFrame(
                    [ list(r) for r in ta_seqs ],
                    index=ta_seqs.index);
                # NaN the gaps
                ngc_seqs = ngc_seqs.replace('-',np.nan);
                # nongap consensus is most prevalent non-gap (non-NAN)
                ngc = pd.Series([
                    residues.mode().values[0]
                    for c,residues in ngc_seqs.iteritems()]);
                # names
                taxbatch = taxon['gb_taxon_id']+"_"+str(batch);
                ng_consensus['TAXBATCH:'+taxbatch]= "".join(ngc);
            # get fasta output
            ngc_fasta = formatFASTA( pd.Series(ng_consensus) );
            with open(ngc_prealign_ffn, 'a') as fh:
                fh.write(ngc_fasta+"\n");
            print("--> nongap consensus appended: "+ngc_prealign_ffn);
            # ------------------------------------------------------------------
        time.sleep(clustaloAPI.pollFreq);
        # ----------------------------------------------------------------------


    ############################################################################
    # Run taxon alignments
    ############################################################################
    # for i,taxon in groupTaxa.iterrows():



    # Align taxon prealignments

    # Build taxon nongap consensuses

    # align nongap consensuses

    # load taxon prealignments and fill in gaps relative to newly aligned nongap consensus

# fin.
