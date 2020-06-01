
# Process

1. Source HTML of taxonomy data from NCBI for betacoronaviruses using the search term "SARS" was downloaded and parsed into taxonomy data records in csv format that include taxon IDs.
2. Protein GI's were obtained using taxon ID searches using NCBI's protein database API (*esearch*).
3. Protein sequences were downloaded from NCBI's protein database API (*efetch*) using GI's.
4. Retreived protein sequences were stored locally.

## API examples
**Get list of protein GI's for taxon ID**

`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=txid591068[Organism:exp]`

**Term criteria for taxon ID spike protein**

`(txid2509481[Organism:exp]) AND spike[Protein Name]`

**Additional term criteria for 'S'**

`(txid2509481[Organism:exp]) AND s[Protein Name]`

**Get merged GenBank file for multiple GI's**

`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=225403291,225403290&rettype=fasta&retmode=text`





# Files

*Taxonomy browser (Betacoronavirus)* is HTML output of search for "SARS" from NCBI taxonomy browser and includes all betacoronavirus entries from various host species. The number of available protein sequences are listed next to each. We can parse this to get a list of all higher-level taxonomic groups and their search criteria (via. the href) in the protein databank. I was not able to restrict protein list to S only. **Note** that SARS-2 is a separate subgroup whose parent but not children are listed here, for these we will want to go to NCBI's COVID-19 page, which has thousands of human sequences.
