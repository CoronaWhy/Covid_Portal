import sys, time, os, re;
import numpy as np, pandas as pd;
import urllib, requests, xmltodict, pprint;
################################################################################
txidfile = os.path.join('..','taxon','taxonomy_parsed.csv');
genbank_file_path = os.path.join('.','genbank_files');
overwrite = False;
################################################################################
# def fetch_protein_ids_from_taxon_id(taxon_id, protein_name="spike"):
#     base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
#     options = {
#         'term'          : "txid"+taxon_id+"[Organism:noexp] AND "+protein_name,
#         'db'            : "protein",
#         'usehistory'    : "n",
#     }
#     url = base + urllib.parse.urlencode(options);
#     r = xmltodict.parse(requests.get(url).text);
#     try: returnval = r['eSearchResult']['IdList']['Id'];
#     except: return None;
#     if type(returnval)==list: return returnval;
#     else: return [returnval];

def fetch_protein_gbs_from_taxon_id(taxon_id, protein_name="spike", retmax=500):
    base_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    base_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?";
    search_options = {
        'term'          : "txid"+taxon_id+"[Organism:noexp] AND "+protein_name,
        'db'            : "protein",
        'usehistory'    : "y",
    };

    url = base_search + urllib.parse.urlencode(search_options);
    r = xmltodict.parse(requests.get(url).text)['eSearchResult'];

    buffer = [];
    if int(r['Count'])>0:
        for restart in range(0,int(r['Count']),retmax):
            fetch_options = {
                'db'        : 'protein',
                'WebEnv'    : r['WebEnv'],
                'query_key' : r['QueryKey'],
                'retmax'    : str(retmax),
                'rettype'   : 'gb',
                'retmode'   : 'text',
            }
            fetch_url = base_fetch + urllib.parse.urlencode(fetch_options);
            gbs = requests.get(fetch_url).text;
            buffer.append(gbs);
            print('.', end='', flush=True);
    return buffer;
################################################################################
failed_ids = [];
taxa = pd.read_csv(txidfile);
taxa['gb_taxon_id'] = taxa['gb_taxon_id'].astype(str);
leafs = taxa[(taxa['leaf']==True) & (taxa['pcount']>0)];
rx_count_gbs = re.compile('[\n]?LOCUS       ');
# fh = open(outfile, "w");
for i,leaf in leafs.iterrows():
    # print("Downloading for "+taxon_id+" ... ", end='', flush=True);
    taxon_id = leaf['gb_taxon_id'];
    filename = os.path.join('genbank_files',taxon_id+'.fna');
    if os.path.isfile(filename):
        if overwrite:
            os.remove(filename);
        else:
            print(
                taxon_id.ljust(10)+" "+
                leaf['name'].ljust(20)+" exists");
            continue;

    print(
        taxon_id.ljust(10)+" "+
        leaf['name'].ljust(20)+" ...");
    gbs = fetch_protein_gbs_from_taxon_id(str(taxon_id));
    record_count = len(re.findall(rx_count_gbs, "".join(gbs)));
    with open(filename,'w') as fh:
        fh.write("".join(gbs));
    print(("--> ").rjust(14)+filename+" ("+str(record_count)+")");
    time.sleep(1);
# fh.close();
# print("Wrote to "+outfile);
# failed_ids = pd.DataFrame({'taxon_id': failed_ids});
# print("Writing "+failfile);
# failed_ids.to_csv(failfile);
