
# Process

`fetch_protein_gbs_from_taxon_ids.py` searched for proteins using individual taxon id's from `txid_search_list.csv` and NCBI's **esearch** and **efetch** APIs, with their protein database. Protein results were downloaded in GenBank format and concatenated into a single large output `accumulated_gbs.fna`. Additional search critera included the MeSH term `spike`.

`extract_protein_sequences.py` used BioPython to load `accumulated_gbs.fna` and extract `taxon_id`, `accession`, `organism`, `version`, `sequence` `references`, `collection_date`, `country`, `host`, `isolation_source`,  `taxon_id` and `coded_by`. An additional column `isolate` was derived from the degenerate features `strain` or `isolate` or otherwise populated with `organism`. The results were output to `gbs_extract_step1.csv`. This script also included a `invalids` list of protein accession numbers (that include versions) that needed to be manually removed. The majority of these were orf1a/b sequences that had not yet been filtered out. In addition, spike proteins listed as "hypothetical" and "putative" were removed as well as sequences from crystal structures, which will be processed separately (protein tags need to be removed). Sequences with these accession numbers were skipped and not added to `gbs_extract_step1.csv`.

Sequences from `gbs_extract_step1.csv` were converted to FASTA format using `build_fasta_for_alignment.py` and identified by accession number. The output is `fbs_foralignment_byaccession.fasta`.

FASTA sequences were aligned using Clustal Omega at the [EMBL-EBI search and sequence analysis tools APIs in 2019](https://www.ebi.ac.uk/Tools/msa/clustalo/) and alignment outputs were stored in the `alignment` folder.
