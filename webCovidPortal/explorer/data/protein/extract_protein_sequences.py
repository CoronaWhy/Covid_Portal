import sys, re, os;
import numpy as np, pandas as pd;
from Bio import SeqIO;
import logging;
################################################################################
genbank_file_path = os.path.join('.','genbank_files');
triage_file = os.path.join('.','triage_genbank_files_output.csv');
logfile = os.path.join('.','extract_protein_sequences.log');
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
def extract_sequence_data(ffn, ignore_accessions=[], min_seq_length=500):
    """Extract sequence and metadata from genbank file containing >= 1 genbank record. Specifically written to extract from NCBI protein records.

    Parameters
    ----------
    ffn : str
        Full path and file name.
    ignore_accessions : list
        List of non-version accession numbers to skip if found.
    min_seq_length : int
        Minimum length of sequence to keep, otherwise will skip.

    Returns
    -------
    pd.DataFrame
        Extracted meta data and sequences.

    """
    rows = [];
    # for every record in file
    for record in SeqIO.parse(ffn,"genbank"):
        row = {};
        # record basics --------------------------------------------------------
        row['taxon_id'] = ""; # extracted later from dbxref feature
        row['description'] = record.description;
        row['organism'] = record.annotations['organism'];
        row['accession'] = record.annotations['accessions'][0];
        logtitle = str(ffn)+" "+str(row['accession'])+": ";

        if row['accession'] in ignore_accessions:
            logging.info(logtitle+" ignored due to ignore_accessions.");
            continue;

        # build accession.version ----------------------------------------------
        version = (
            row['accession']+"."+
            str(record.annotations.get('sequence_version',"1"))
        );
        row['version'] = version;
        # GET SEQUENCE
        row['seq'] = str(record.seq);
        if len(row['seq']) < min_seq_length:
            logging.info(
                logtitle+"ignored, sequence is <"+str(min_seq_length)+".");
            continue;
        # ----------------------------------------------------------------------
        # get publication references -------------------------------------------
        row['references'] = [];
        for r in record.annotations['references']:
            if r.pubmed_id!="":
                row['references'].append(r.pubmed_id);
        # ----------------------------------------------------------------------
        # extract relevant feature data ----------------------------------------
        def dgf(d, k): # simplify BioPython's arrayifying/OOPing everything
            return d.get(k, [""])[0];
        record_cds = 0;
        for f in record.features:
            # meta-data
            if f.type=="source":
                d = f.qualifiers;
                row['collection_date'] = dgf(d, "collection_date");
                row['country'] = dgf(d, "country");
                row['host'] = dgf(d, "host");
                row['isolation_source'] = dgf(d, "isolation_source");
                if "strain" in d:
                    row['isolate'] = dgf(d, "strain");
                elif "isolate" in d:
                    row['isolate'] = dgf(d, "isolate");
                else:
                    row['isolate'] = row['organism']
                if "db_xref" in d:
                    for ref in d['db_xref']:
                        if ref[0:5]=="taxon":
                            row['taxon_id'] = ref[6:];
            # coding regions, should only one: the spike protein
            elif f.type=="CDS":
                record_cds+=1;
                if record_cds>1:
                    raise Exception("Multiple CDS identified for "+row['organism']);
                d = f.qualifiers;
                row['coded_by'] = dgf(d, "coded_by");
        # ----------------------------------------------------------------------
        # add row
        logging.info(logtitle+" stored.");
        rows.append(row);
    return pd.DataFrame(rows);
################################################################################
def extract_genbank_files(
    # path to genbank protein files by taxon id
    path=os.path.join('.','genbank_files'),
    # triage file
    triage_file=os.path.join('.','triage_genbank_files_output.csv'),
    # output file for sequences and data
    sequence_file=os.path.join('.','extract_protein_sequences_output.csv'),
    # overwrite output file if True
    overwrite=True,
    record_buffer=10000,
):
    """Extracts sequence data and metadata from genbank protein sequence files
    whose accession numbers have been triaged.

    Parameters
    ----------
    path : str
        Path to genbank file repository.
    triage_file : str
        Full file name and path of genbank accession triage output file.
    sequence_file : str
        Full file name and path of file to output to.
    overwrite : bool
        Overwrite output file if True, otherwise will append.
    record_buffer : int
        Number of genbank records to buffer before write.

    Returns
    -------
    None

    """
    # load triage file
    triaged = pd.read_csv(triage_file);
    # delete extract sequence output file if exists
    if os.path.isfile(sequence_file):
        os.remove(sequence_file);
    # initialize rows buffer
    rows = [];
    # go by unique filename
    for ffn in triaged['ffn'].unique():
        # subset traige records
        ss = triaged[triaged['ffn']==ffn];

        # get data from records in file
        # NOTE: accessions here do not include version numbers
        rows.append(
            extract_sequence_data(
                ffn,
                ignore_accessions=ss['accession'][
                    ss['valid']==False
                ].astype(str).to_list()
            )
        );

        # check buffer size and save if needed
        if len(rows)>=record_buffer:
            df = pd.concat(rows);
            if os.path.isfile(sequence_file):
                df.to_csv(sequence_file, mode='a', header=False);
            else:
                df.to_csv(sequence_file, header=True);
            rows = [];

    # final save.
    if len(rows)>0:
            df = pd.concat(rows, ignore_index=True, sort=False);
            if os.path.isfile(sequence_file):
                df.to_csv(sequence_file, mode='a', header=False);
            else:
                df.to_csv(sequence_file, header=True);
################################################################################
if __name__ == '__main__':
    extract_genbank_files(
        path=genbank_file_path,
        # triage file
        triage_file=triage_file,
        # output file for sequences and data
        sequence_file=os.path.join('.','extract_protein_sequences_output.csv'),
        # overwrite output file if True
        overwrite=True,
        record_buffer=10000,
    );
################################################################################
# Issues to be aware of:
#   1. Strain vs. Isolate in record.features type "source", some have neither.
#       Use strain, then isolate, then organism name in that order.
#   2. Make sure every record has only one or no CDS record
