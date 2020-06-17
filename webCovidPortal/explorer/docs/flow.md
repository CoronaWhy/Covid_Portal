# Protien Explorer: Logical Flow


## Definitions

| Name | Description |
|------|-------------|
| `sequence viewer` | Visual panel that contains horizontally synchronized sequence alignments labeled by accession number and with one additional column of sortable data, with a select dropdown to choose the sort criteria field. |
| `sequence browser` | Sortable, filterable table popup display that allows users to add/remove sequences from the `sequence viewer`. |
| `epitope viewer` | Visual panel that contains horizontally synchronized epitope sequence alignment. |
| `epitope browser` | Sortable, filterable table opup that allows users to add/remove epitopes from the `epitope viewer`. |
| `structure viewer` | Visual panel that contains horizontally synchronized structure-chain sequences colored according to a the distance between each residue and a `reference residue`.  |
| `structure browser` | Sortable, filterable table popup that allows users to add/remove strucure chain sequences from the `structure viewer`. |
| `alignemnt bar` | A horizontally synchronized list of names for each amino acid position. |
| `structure reference picker` | A horizontally synchronized alignment bar that has a marker that marks the `reference residue` for the `structure viewer`. The marker may be moved by clicking on the desired position in the `structure reference picker`. |

## Initialization

### Sequence Browser

1. The `sequence browser` requests all sequence record information for the coronavirus spike protein by MeSH ID:
    * http://localhost:8000/explorer/sequencerecords?mesh_id=D064370
2. These data populate the sortable, filterable `sequence browser` table with the following columns:

| Column | Type | Description |
| taxon_name   | str    | Name of taxon. |
| accession    | str    | NCBI Protein accession number (With version). |
| organism     | str    | Organism name. |
| country      | str    | Country, country:region the sequence was obtained from. |
| host         | str    | Name of organism host. |
| isolation_source | str | Name of tissue sequence was isolated from. |
| isolate | str | Name of isolate. |

3. Accession IDs YP_009724390.1 (early SARS-CoV-2 isolate Wuhan-Hu-1), QIS61410.1 (late SARS-CoV-2 isolate SARS-CoV-2/human/USA/WA-UW376/2020) and XX should be indicated as sequences currently being displayed by the `sequence viewer`.

### Sequence Viewer

1. The `sequence viewer` requests sequence alignments for the coronavirus spike, alignment 20200505, and accessions XX, XX and XX:
    * LINK
2. Available sortable criteria should be:

| Name | Type | Description |
|------|------|-------------|
| taxon_name   | str    | Name of taxon. |
| accession    | str    | NCBI Protein accession number (With version). |
| organism     | str    | Organism name. |
| country      | str    | Country, country:region the sequence was obtained from. |
| host         | str    | Name of organism host. |
| isolation_source | str | Name of tissue sequence was isolated from. |
| isolate | str | Name of isolate. |

3. Sortable crtierion selected should be host and sequences should be vertically sorted alphabetically by accession.








fin.
