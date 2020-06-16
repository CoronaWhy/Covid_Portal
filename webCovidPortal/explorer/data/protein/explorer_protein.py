import numpy as np, pandas as pd;
import os, sys, re, logging, time;
import urllib, requests, xmltodict;
from Bio import SeqIO;
from io import StringIO; # for biopython SeqIO.parse on gb strings
import clustaloAPI;
################################################################################
email = 'alkali.blue@gmail.com';
logfile = 'explorer_protein.log';
alignment_batchsize = 2000;
genbank_repository = os.path.join('.','genbank');
alignment_name = "20200616";
alignment_root = os.path.join('.','alignments');
alignment_path = os.path.join(alignment_root, alignment_name);
sequence_record_root = os.path.join('.','sequence_records');
################################################################################
def gbTaxonFile(taxon_id):
    return str(taxon_id)+".fna";
def sequenceRecordFile(taxon_id):
    return str(taxon_id)+"_sequenceRecords.csv";
def clustaloDownloadAlignmentFile(taxon_id, batch):
    return str(taxon_id)+"_"+str(batch+1)+".aln-fasta.fasta";
def clustaloAlignmentFile(taxon_id):
    return str(taxon_id)+".fasta";
################################################################################
def NCBI_fetchGBRecords(taxon_id, protein_name="spike", batchsize=500):
    gbRecords = [];
    base_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    base_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?";
    search_options = {
        'term'     : str(
                        "txid"+
                        str(taxon_id)+
                        "[Organism:noexp] AND "+
                        str(protein_name)),
        'db'        : 'protein',
        'usehistory': 'y',
    };
    url = base_search + urllib.parse.urlencode(search_options);
    r = xmltodict.parse(requests.get(url).text)['eSearchResult'];

    if int(r['Count'])>0:
        for restart in range(0,int(r['Count']),batchsize):
            fetch_options = {
                'db'        : 'protein',
                'WebEnv'    : r['WebEnv'],
                'query_key' : r['QueryKey'],
                'retmax'    : str(batchsize),
                'rettype'   : 'gb',
                'retmode'   : 'text',
            }
            fetch_url = base_fetch + urllib.parse.urlencode(fetch_options);
            gbRecords.append(requests.get(fetch_url).text);
    return "".join(gbRecords);
################################################################################
def load_taxonGBRecords(ffn):
    with open(ffn,'r') as fh:
        records = fh.read();
    return records;
################################################################################
def store_GBRecords_byTaxon(taxon_id, records, path='', overwrite=False):
    ffn = os.path.join(path, gbTaxonFile(taxon_id));
    if os.path.isfile(ffn) and not overwrite:
        raise Exception("GenBank taxon file "+ffn+" already exists.");

    with open(ffn,'w') as fh:
        fh.write("".join(records));

    return ffn;
################################################################################
def parse_GBRecord(record, singular=False):
    data = {};
    # record basics ------------------------------------------------------------
    data['taxon_id'] = ""; # extracted later from dbxref feature
    data['description'] = record.description;
    data['organism'] = record.annotations['organism'];
    data['accession'] = record.annotations['accessions'][0];
    data['version'] = \
        data['accession']+"."+str(
            record.annotations.get('sequence_version',"1"));
    data['sequence'] = str(record.seq);
    # get publication references -----------------------------------------------
    data['references'] = [];
    for r in record.annotations['references']:
        if r.pubmed_id!="":
            data['references'].append(r.pubmed_id);
    # extract relevant feature data --------------------------------------------
    def dgf(d, k): # simplify BioPython's arrayifying/OOPing everything
        return d.get(k, [""])[0];
    record_cds = 0;
    for f in record.features:
        if f.type=="source":
            d = f.qualifiers;
            data['collection_date'] = dgf(d, "collection_date");
            data['country'] = dgf(d, "country");
            data['host'] = dgf(d, "host");
            data['isolation_source'] = dgf(d, "isolation_source");
            if "strain" in d:
                data['isolate'] = dgf(d, "strain");
            elif "isolate" in d:
                data['isolate'] = dgf(d, "isolate");
            else:
                data['isolate'] = data['organism']
            if "db_xref" in d:
                for ref in d['db_xref']:
                    if ref[0:5]=="taxon":
                        data['taxon_id'] = ref[6:];
        # coding regions, should only one, expect protein
        elif f.type=="CDS":
            record_cds+=1;
            if record_cds>1 and singular:
                raise Exception("Multiple CDS for "+data['organism']);
            d = f.qualifiers;
            data['coded_by'] = dgf(d, "coded_by");
    return data;
################################################################################
def extract_GBRecords(gbrecords, singular=False):
    filter_status = [];    # who was kept and who was filtered out
    seqs = {};              # pd.Series of sequences keyed by accession.version
    seqrecords = [];        # pd.DataFrame of sequence records
    rx_filters = {
        # synonyms for spike in sentence context for description field
        'spike'     : re.compile('^spike | spike |\=spike ', re.IGNORECASE),
        'e2'        : re.compile('^e2 | e2 |\=e2 ', re.IGNORECASE),
        's'         : re.compile('^s | s |\=s ', re.IGNORECASE),
        'surface'   : re.compile('surface glycoprotein', re.IGNORECASE),
        # reject records with these words in description
        'exclude'   : re.compile('putative|hypothetical|chain', re.IGNORECASE),
    };
    with StringIO(gbrecords) as gbrecord_handler:
        for record in SeqIO.parse(gbrecord_handler, "genbank"):
            # Apply filters ----------------------------------------------------
            # NOTE: these are very specific to coronavirus spike
            valid = False;
            # matches we want to keep
            if re.search(rx_filters['spike'], record.description):
                valid=True;
            elif re.search(rx_filters['e2'], record.description):
                valid=True;
            elif re.search(rx_filters['s'], record.description):
                valid=True;
            elif re.search(rx_filters['surface'], record.description):
                valid=True;
            # matches to exclude
            if re.search(rx_filters['exclude'], record.description):
                valid=False;
            # parse record data
            row = parse_GBRecord(record, singular=singular);
            # store filter results
            filter_status.append({
                'description': row['description'],
                'version': row['version'],
                'organism': row['organism'],
                'taxon_id': row['taxon_id'],
                'valid': valid,
            });
            # skip to next record if this one isn't valid
            if not valid:
                continue;
            # check unique accession
            if row['version'] in seqs:
                raise Exception(
                    "Duplicate accession/version: "+str(row['version']));
            # add sequence and metadata
            seqs[row['version']] = row['sequence'];
            seqrecords.append(row);
    return {
        'filter_status'    : pd.DataFrame(filter_status),
        'sequences'         : pd.Series(seqs),
        'sequence_records'  : pd.DataFrame(seqrecords),
    };
################################################################################
def store_sequenceRecords_byTaxon(taxon_id, records, path='', overwrite=False):
    ffn = os.path.join(path, taxon_id+"_sequenceRecords.csv");
    if os.path.isfile(ffn) and not overwrite:
        raise Exception("SequenceRecord taxon file "+ffn+" already exists.");

    records.to_csv(ffn, index=False);
    return ffn;
################################################################################
def store_clustaoAlignment_byTaxon(taxon_id, records, path='', overwrite=False):
    ffn = os.path.join(path, clustaloAlignmentFile(taxon_id));
    if os.path.isfile(ffn) and not overwrite:
        raise Exception("SequenceRecord taxon file "+ffn+" already exists.");

    records.to_csv(ffn, index=False);
    return ffn;
################################################################################
def series_toFasta(seqs, linewidth=80):
    fasta = [];
    for n,s in seqs.iteritems():
        fasta.append("\n".join(
            [ ">"+str(n) ] +
            [ s[i:i+(linewidth-1)] for i in range(0,len(s),(linewidth-1)) ]
        ));
    return fasta;
################################################################################
def fasta_toSeries(fasta):
    seqs = {};
    current = "";
    for l in fasta.split('\n'):
        if len(l)<=1: continue;
        if l[0]=='>': current = l[1:];
        else:
            if current in seqs.keys():
                seqs[current] += str(l);
            else:
                seqs[current] = str(l);
    return pd.Series(seqs, dtype=str).drop(index=[''], errors='ignore');
################################################################################
def clustaloAlign(taxon_id, seqs, batchsize=2000, keep_results=True, result_path=''):
    result_file_suffixes = {
        'alignment'         : ".aln-fasta.fasta", #alignment file suffix
        'log'               : ".out.txt",
        'tree'              : ".phylotree.ph",
        'identity_matrix'   : ".pim.pim",
        'input'             : ".sequence.txt",
    };
    aligned_seqs = [];
    fasta_seqs = series_toFasta(seqs);
    # clustalo is multiple alignment, If <=2 seqs then just return
    if len(seqs)<=2:
        return seqs;
    # if >2 sequences then multiple alignment is applicable
    for bix in range(0,len(fasta_seqs),batchsize):
        batch = fasta_seqs[bix:bix+batchsize];
        result_id = taxon_id+"_"+str(bix+1);

        jobId = clustaloAPI.serviceRun(
            email,
            result_id,
            "\n".join(batch),
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
            outfile=result_id,
            # path to store output files in
            path=result_path,
        );
        # load aligned sequences and merge into cumulative structure
        batch_aligned = SeqIO.parse(
            os.path.join(
                result_path,
                result_id+result_file_suffixes['alignment']),
            'fasta').to_dict();
        aligned_seqs = {**aligned_seqs, **batch_aligned};
        # remove files if requested
        if not keep_results:
            for suffix in result_file_suffixes:
                ffn = os.path.join(
                    result_path,
                    result_id+result_file_suffixes['alignment'],
                );
                if os.path.isfile(ffn):
                    os.remove(ffn);
    return pd.Series(aligned_seqs);
################################################################################
def nongapConsensus(sequences, id_column):
    ngs = pd.DataFrame();
    return ngs;
################################################################################
if __name__=="__main__":
    # ARGUMENTS ----------------------------------------------------------------
    # for testing: 11131 is small, 215681 is a little more.
    taxon_id="215681";
    # --------------------------------------------------------------------------
    rx_genbank_record_count = re.compile("[\n]?LOCUS       ");

    # initialize logfile -------------------------------------------------------
    with open(logfile, 'w') as fh:
        pass;
    logging.basicConfig(
        filename=logfile,
        level=logging.DEBUG,
        format='%(asctime)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%s');

    # create folders if needed -------------------------------------------------
    chkpaths = [
        genbank_repository,
        sequence_record_root,
    ];
    for path in chkpaths:
        if not os.path.isdir(path):
            logging.info("Creating "+path);
            os.makedirs(path);

    # fetch GB records from NCBI protein database for taxon id -----------------
    gbtffn = os.path.join(genbank_repository, gbTaxonFile(taxon_id));
    if os.path.isfile(gbtffn):
        gbrecords = load_taxonGBRecords(gbtffn);
        logging.info("Using records from existing taxon file "+gbtffn);
    else:
        logging.info("Fetching GenBank records for taxon "+taxon_id);
        gbrecords = NCBI_fetchGBRecords(taxon_id);
    logging.info(
        "Received "+
        str(len(re.findall(rx_genbank_record_count, gbrecords)))+
        " records"
    );

    # store records in single file named for taxon id --------------------------
    # NOTE: this includes records that will be filtered out, so we can traige
    #       the filtering process.
    gbffn = store_GBRecords_byTaxon(
        taxon_id,
        gbrecords,
        path=genbank_repository,
        overwrite=True,
    );
    logging.info("Stored to "+gbffn);

    # filter and extract good records ------------------------------------------
    filter_results = extract_GBRecords("".join(gbrecords), singular=True);
    seqRecords = filter_results['sequence_records'];
    filterStatus = filter_results['filter_status'];
    sequences = filter_results['sequences'];
    logging.info("Filtered to "+str(len(seqRecords))+" records");

    # save sequence records ----------------------------------------------------
    srffn = store_sequenceRecords_byTaxon(
        taxon_id,
        seqRecords,
        path=sequence_record_root,
        overwrite=True,
    );
    logging.info("Stored sequenceRecords to "+srffn);

    # alignment ----------------------------------------------------------------
    alnffn = os.path.join(
        alignment_path,
        clustaloAlignmentFile(taxon_id),
    );

    # TODO: alignment files need to be store by batch because each batch is a
    #       separate alignment. So how/where to store them and how to allow
    #       load from file if exists, instead of always calling server.

    if os.path.isfile(alnffn):
        # use existing
        with open(alnffn,'r') as fh:
            aligned = fh.read();
        aligned = fast_toSeries(aligned);
    else:
        # run alignment
        logging.info("Aligning in batches of "+str(alignment_batchsize));
        aligned = clustaloAlign(taxon_id, sequences, batchsize=alignment_batchsize);
    print(aligned);



# fin.
