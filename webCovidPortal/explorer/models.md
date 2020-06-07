# Explorer models

- [Explorer models](#explorer-models)
  * [Global Identifiers and Classifiers](#global-identifiers-and-classifiers)
    + [explorer.models.Taxon](#explorermodelstaxon)
    + [explorer.models.Protein](#explorermodelsprotein)
  * [Sequence Associated Models](#sequence-associated-models)
    + [explorer.models.Alignment](#explorermodelsalignment)
    + [explorer.models.SequenceRecord](#explorermodelssequencerecord)
    + [explorer.models.Sequence](#explorermodelssequence)
    + [explorer.models.Nomenclature](#explorermodelsnomenclature)
    + [explorer.models.NomenclaturePosition](#explorermodelsnomenclatureposition)
  * [Immunological Epitope Models](#immunological-epitope-models)
    + [explorer.models.Epitope](#explorermodelsepitope)
    + [explorer.models.EpitopeExperiment](#explorermodelsepitopeexperiment)
  * [Crystal Structure Models](#crystal-structure-models)

## Global Identifiers and Classifiers

### explorer.models.Taxon

| Property | Type | Description |
|----------|------|-------------|
| gb_taxon_id   | str       | GenBank Taxon ID, unique. |
| leaf          | boolean   | Leaf node (True) or not (False). |
| path          | str       | period-separated list of ancestral taxon IDs starting with the farthest ancestor (left) to closest (right). |
| name          | str       | Name of the taxon. |
| level         | str       | Taxonomic level (Genus, Family, etc...). |

### explorer.models.Protein

| Property | Type | Description |
|----------|------|-------------|
| name      | str   | Name of the protein (common). |
| mesh_id   | str   | MeSH ID for the protein (unique). |

## Sequence Associated Models

### explorer.models.Alignment

| Property | Type | Description |
|----------|------|-------------|
| name      | str   | Name of the alignment (unique). |
| protein   | explorer.models.Protein | Protein the alignment is for. |
| date_created | str | Date the alignment was stored (auto). |

### explorer.models.SequenceRecord

| Property | Type | Description |
|----------|------|-------------|
| protein   | explorer.models.Protein   | Protein the sequence record is for. |
| taxon     | explorer.models.Taxon     | Taxon that this sequence record is for. |
| accession | str   | NCBI Protein accession number (With version, unique). |
| organism | str | Organism name (required). |
| collection_date | str | Sequence collection date (null). |
| country | str | Country, country:region the sequence was obtained from (null). |
| host | str | Name of organism host (null). |
| isolation_source | str | Name of tissue sequence was isolated from (null). |
| isolate | str | Name of isolate (null). |
| coded_by | str | NCBI nucleotide accession and region that codes this protein sequence. |

### explorer.models.Sequence

| Property | Type | Description |
|----------|------|-------------|
| sequence_record | explorer.models.SequenceRecord | Record for this sequence. |
| alignment | explorer.models.Alignment | Alignment for this sequence. |
| sequence | str | Sequence alignment with leading gaps trimemd. |
| offset | int | Number of leading gaps that were trimmed. |

### explorer.models.Nomenclature

| Property | Type | Description |
|----------|------|-------------|
| name | str | Name of the nomenclature. |
| date_created | date | Date the nomenclature was stored (auto). |
| reference | explorer.models.Sequence | Sequence alignment that this nomenclature is based on. |

### explorer.models.NomenclaturePosition

| Property | Type | Description |
|----------|------|-------------|
| nomenclature | explorer.models.Nomenclature | Nomenclature the position is for. |
| index | int | Index of position in aligned sequence. |
| major | int | Major nomenclature position. |
| minor | int | Minor nomenclature position. |

## Immunological Epitope Models

### explorer.models.Epitope

| Property | Type | Description |
|----------|------|-------------|
| IEDB_ID | str | IEDB ID for epitope. |
| protein | explorer.models.Protein | Protein the epitope is described for. |
| alignment | explorer.models.Alignment | Alignment this epitope sequence was aligned to. |
| sequence | str | Aligned epitope sequence with leading gaps trimmed. }
| offset | int | Number of leading gaps that were trimemd. |

### explorer.models.EpitopeExperiment

| Property | Type | Description |
|----------|------|-------------|
| epitope | explorer.models.Epitope | Epitope sequence this experiment is for. |
| host | str | Name of the host organism used in experiment where applicable. |
| assay_type | str | Name of the assay type (e.g. "ELISA"). |
| assay_result | str | Result of the assay (single-word categorical description). |
| mhc_allele | str | Four-digit resolved HLA recognizing the epitope. |
| mhc_class | str | MHC class tested (I is T cell, II is B cell). |
| exp_method | str | Experimental method used (subclass of assay type). |
| measurement_type | str | Type of measurement (binding, lysis activity etc...). |

## Crystal Structure Models
