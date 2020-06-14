import numpy as np, pandas as pd;
import os, sys, re;
from Bio import SeqIO;
################################################################################
genbank_files_path = os.path.join('.','genbank_files');
triage_file="triage_genbank_files_output.csv";
################################################################################
def triage_genbank_files(
    path=os.path.join('.','genbank_files'),
    verbose=False
):
    """Short summary.

    Parameters
    ----------
    path : type
        Description of parameter `path`.
    verbose : type
        Description of parameter `verbose`.

    Returns
    -------
    type
        Description of returned object.

    """

    records = [];
    rx_filters = {
        # synonyms for spike in sentence context for description field
        'spike'     : re.compile('^spike | spike |\=spike ', re.IGNORECASE),
        'e2'        : re.compile('^e2 | e2 |\=e2 ', re.IGNORECASE),
        's'         : re.compile('^s | s |\=s ', re.IGNORECASE),
        'surface'   : re.compile('surface glycoprotein', re.IGNORECASE),
        # reject records with these words in description
        'exclude'   : re.compile('putative|hypothetical|chain', re.IGNORECASE),
    };

    for fn in os.listdir(genbank_files_path):
        if os.path.isfile( os.path.join(genbank_files_path, fn) ):
            base, ext = os.path.splitext(fn);
            if ext==".fna":
                if verbose:
                    print(fn.ljust(15)+" ... ", end='', flush=True);
                file_records = [];
                for record in SeqIO.parse(os.path.join(genbank_files_path, fn),"genbank"):
                        valid = False;
                        # filter keeps
                        if re.search(rx_filters['spike'], record.description):
                            valid=True;
                        elif re.search(rx_filters['e2'], record.description):
                            valid=True;
                        elif re.search(rx_filters['s'], record.description):
                            valid=True;
                        elif re.search(rx_filters['surface'], record.description):
                            valid=True;
                        # filter excludes
                        if re.search(rx_filters['exclude'], record.description):
                            valid=False;
                        # store
                        file_records.append({
                            'description': record.description,
                            'accession': record.annotations['accessions'][0],
                            'organism': record.annotations['organism'],
                            'taxon_id': base,
                            'valid': valid,
                            'ffn': os.path.join(genbank_files_path, fn),
                        });
                if verbose:
                    print(str(len(file_records))+" records.");
                records = records+file_records;
    if verbose:
        print("dataframing...");
    records = pd.DataFrame(records);
    return records;
################################################################################
if __name__ == '__main__':
    triaged = triage_genbank_files(path=genbank_files_path, verbose=True);
    print("Writing "+triage_file);
    triaged.to_csv(triage_file);
