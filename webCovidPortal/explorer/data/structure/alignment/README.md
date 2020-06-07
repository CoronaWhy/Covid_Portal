# Structure Sequence Alignment
The general idea here is to align the PDB structure sequences with closely realted sequences that have already been aligned, in the explorer database. Once these related sequences are aligned to the PDB sequences, a comparison between the newly aligned databse sequences and their original alignment will allow the new alignment to be translated to the original alignment for all sequences, including the PDB sequences. Confirmation is obtained by comparing the corrected database sequences with their original alignments.

Related sequences are obtained from the PDB file `taxon_id`s, which are extracted by `../extract_chains.py` and stored in `../chains.csv`. All aligned sequences from the explorer database that belong to these taxa are merged with the PDB sequences and stored in unique FASTA files for each taxon. The FASTA files are aligned, individually, so that the PDB sequences are aligned with closely related sequences that we have alignments for.

These alignments are conformed to the original database alignment by padding in missing gaps. This requires that **at least one of the database sequences has no gaps in the taxon alignment.** Where this is true, the missing gaps from the original sequence (from the database alignment) can be filled in to this new alignment, thereby aligning the PDB sequences.

A different strategy is necessary to determine what to do with gaps in taxon alignments that don't produce any gapless reference sequences.

The process requires `../chains.csv`, which is generated by `../extract_chains.py` and must have a `taxon_id` column listing the `taxon_id`s of each PDB structure.

1. Get aligned explorer database sequences that match the `taxon_id`s of each PDB structure in `../chains.csv` using `db_taxon_select.py`.
    * `../chains.csv -< db_taxon_select.py -> select_taxa_seqs.sql`
2. Run and export the SQL results from `select_taxa_seqs.sql` to `db_taxon_sequences.csv` with headers.
3. Build taxon prealigment FASTA files using `build_aligment_fastas.py`, which requires the taxon sequences and PDB sequences as input.
    * `./db_taxon_sequences.csv, ../sequences/csv -< build_alignment_fastas.py -> fasta_prealign_[TAXON_ID].fasta`
4. Run an alignment on each file using [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/) and save resulting aligment/clustal files locally.
5. Build preconformed alignment CSV file using `build_preconformed_alignments.py`, this file contains a list of all the clustal alignment files you want to include and will combine all into a single CSV for bulk processing.
    * `[CLUSTAL FILES] -< build_preconformed_alignments.py -> preconformed_alignments.csv`
6. Conform the alignments using the preconformed alignments CSV file, your original aligned reference sequences and `conform_alignments.py`.
    * `preconformed_alignments.csv, db_taxon_sequences.csv -< conform_aligments -> conformed_alignemnts.csv`
    * **Note** that `conformed_alignments.csv` will only contain the conformed PDB sequence alignments and the conformed reference that was used for each `taxon_id`, the final conformed reference is always checked against it's originally conformed version to ensure correct re-alignment.
    * **Note** leading gaps are not removed from PDB sequences and the offset refers to the reference offset, to which the leading gaps in PDB sequences will eventually be added upon database import.

## Get Taxon-Related Aligned Sequences
This requires `taxon_id`s extracted from the PDB files, which is done by `../extract_chains.py` and will be found in the output `../chains.csv`. A SQL statement is generated by `db_taxon_select.py`, which can be used to select and export all aligned sequences. **Note** that the alignment name is presently hard-coded into `db_taxon_select.py`, since we only have one alignment and one protein. The SQL statement is output to `select_taxa_seqs.sql`.

Export the results to a file called `db_taxon_sequences.csv`.

## Build FASTA Files for Alignment
Sequences from the taxon search (`db_taxon_select.py`) and the PDB files (`../sequences.csv`) are combined, gap-stripped, and converted to FASTA files that group the sequences by `taxon_id`. This is done by `build_alignment_fastas.py`, which produces fasta files in the `./prealign/` folder named by taxon ID as `fasta_prealign_[TAXON ID].fasta`.

**Note** that the FASTA headers for database sequeces (with accession numbers) are different from those of the PDB sequences.

Database sequence headers are
```
>ACCESSION=[ACCESION #];CHAIN=X;TAXID=[TAXON ID]
```

while PDB sequences are
```
>PDB=[PDB ID];CHAIN=[CHAIN ID];TAXID=[TAXON ID]
```

## Run Alignments
Alignments are currently run manually using [Clustal Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/). Resulting clustal alignment files are stored in the `./aligned/` folder and should be named by taxon ID as: `aligned_[TAXON ID].aln`.

## Build Preconformed Alignments File
The alignments are formatted and gathered across multiple taxa so they can be processed in bulk. This is done by `build_preconformed_alignments.py`, which contains a hard-coded list of alignment files to work on, from the `./aligned/` folder (`alignment_files`). The output is `preconformed_alignments.csv` with the following columns:

| column | type | description |
|--------|------|-------------|
| accession         | str   | Accesion number of sequence (if from database). |
| pdb               | str   | PDB ID of sequence (if from structure file). |
| chain             | char  | Chain ID (if from structure file). |
| taxon_id          | str   | NCBI taxon id of taxon alignment. |
| sequence          | str   | Taxon-aligned sequence (not final alignment). |

## Conform Alignments
To convert these new alignments to the final database alignment, gaps need to be filled in where needed. The gap fill-in is defined as follows:

```
ORIGINAL RELATIVE = ABC---DEF---GHI
ORIGINAL STRIPPED = ABCDEFGHI
PDB SEQUENCE =      CDFG

# align sequences
ORIGINAL TAXON ALIGNED =    ABCDEFGHI
PDB TAXON ALIGNED =         --CD-FG--

# add gaps to all TAXON ALIGNED sequences where ORIGINAL RELATIVE has gaps

ORIGINAL RELATIVE =             ABC---DEF---GHI
ORIGINAL TAXON ALIGNED RE-GAP = ABC---DEF---GHI
PDB TAXON ALIGNED RE-GAP =      --C---D-F---G--
```

This is done by `conform_alignments.py`, which requires the pre-conformed aligments in `preconformed_alignments.csv` and the original taxon sequences from the database in `db_taxon_sequences.csv`. The output is `conformed_alignments.csv`, which contains the following columns:

| column | type | description |
|--------|------|-------------|
| sequence  | str   | Corrected/conformed sequence. |
| offset    | int   | Offset of reference sequence that was used to correct the taxon alignment. |
| accession | str   | Either the NCBI Protein accession number (for database sequence) or the PDB ID and chain if sequence is from a structure(1) |
| alignment | str   | Name of the alignment for the reference sequence used. |

*(1) Format is* `PDB.[PDB_ID]:[CHAIN ID]`

**Note** that trimming and offsetting the structure sequences is done later, before import.


fin.