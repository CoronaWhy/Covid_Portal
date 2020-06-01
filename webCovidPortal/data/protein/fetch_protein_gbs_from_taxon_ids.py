import sys, time;
import numpy as np, pandas as pd;
import urllib, requests, xmltodict, pprint;
################################################################################
def fetch_protein_ids_from_taxon_id(taxon_id, protein_name="spike"):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    options = {
        'term'          : "txid"+taxon_id+"[Oraganism:noexp] AND "+protein_name,
        'db'            : "protein",
        'usehistory'    : "n",
    }
    url = base + urllib.parse.urlencode(options);
    r = xmltodict.parse(requests.get(url).text);
    try: returnval = r['eSearchResult']['IdList']['Id'];
    except: return None;
    if type(returnval)==list: return returnval;
    else: return [returnval];

def fetch_protein_gbs_from_taxon_id(taxon_id, protein_name="spike", retmax=500):
    base_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    base_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?";
    search_options = {
        'term'          : "txid"+taxon_id+"[Oraganism:noexp] AND "+protein_name,
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
    return buffer;


################################################################################

taxon_ids = ["230471"];
failed_ids = [];
txidfile = "txid-search-list.csv";
df = pd.read_csv(txidfile);
taxon_ids = df['taxon_id'].astype(str);

fh = open("accumulated_gbs.fna", "w");
for taxon_id in taxon_ids:
    print("Downloading for "+taxon_id+" ... ", end='', flush=True);
    try:
        gbs = fetch_protein_gbs_from_taxon_id(taxon_id);
        print("OK");
        fh.write("".join(gbs));
    except:
        print("Failed "+taxon_id);
        failed_ids.append(taxon_id);
        fh.close();
        sys.exit();
    time.sleep(1);
fh.close();
failed_ids = pd.DataFrame({'taxon_id': failed_ids});
failed_ids.to_csv("gbs_fetch_failed_taxon_ids.csv");


sys.exit();

taxon_ids = ["31631"];
outfile = "protein_gbs.fna";
fail_file = "failed_taxon_ids.csv";
# get taxon ids from file
txidfile = "txid-search-list.csv";
df = pd.read_csv(txidfile);
taxon_ids = df['taxon_id'].astype(str);
failed_ids = [];

protein_ids = pd.DataFrame(columns=['protein_id','taxon_id']);
for taxon_id in taxon_ids:
    print("Searching "+taxon_id+" ...", end='', flush=True);
    local = fetch_protein_ids_from_taxon_id(taxon_id);
    if local==None:
        print(" FAILED");
        failed_ids.append(taxon_id);
    else:
        print(" OK ["+str(len(local))+"]");
        newrows = pd.DataFrame({'protein_id': local});
        newrows['taxon_id'] = taxon_id;
        protein_ids = pd.concat([newrows, protein_ids], ignore_index=True);
#    if taxon_id=="702701": break;
    time.sleep(1);
print("writing "+outfile);
protein_ids.to_csv(outfile);
print("Writing "+fail_file);
failed_ids = pd.DataFrame({'taxon_id': failed_ids});
failed_ids.to_csv(fail_file);
print("Done");
