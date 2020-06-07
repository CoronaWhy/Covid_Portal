The explorer API serves sequence alignemnts etc. to the front end.

- [Global Classifiers](#global-classifiers)
  * [Taxa](#taxa)
- [Protein Sequence Records and Alignments](#protein-sequence-records-and-alignments)
  * [Sequence Records](#sequence-records)
  * [Sequence](#sequence)
  * [Nomenclature](#nomenclature)
- [Immunological Epitopes and Experiments](#immunological-epitopes-and-experiments)
  * [Epitope Experiment Classes](#epitope-experiment-classes)
  * [Epitope Experiments](#epitope-experiments)
  * [Epitope Sequences](#epitope-sequences)
- [Crystal Structures](#crystal-structures)
  * [Crystal Structure Names and Chains](#crystal-structure-names-and-chains)
  * [Crystal Structure Sequence Alignments](#crystal-structure-sequence-alignments)
  * [Crystal Structure Residue Info and Coordinates](#crystal-structure-residue-info-and-coordinates)


## Global Classifiers

### Taxa

**URL**: explorer/taxa

**Example**: http://localhost:8000/explorer/taxa

**Returns**: an array of all `explorer.Taxon` objects from database.

**Return Format**: Django-serialized.

**Example**:
```
[{
    "model": "explorer.taxon",
    "pk": 1, "fields": {
        "gb_taxon_id": "2509481",
        "leaf": false,
        "path": "0",
        "name": "Embecovirus",
        "level": "subgenus"
    }
}, {
    "model": "explorer.taxon",
    "pk": 2,
    "fields": {
        "gb_taxon_id": "694003",
        "leaf": false,
        "path": "0.2509481",
        "name": "Betacoronavirus 1",
        "level": "species"
    }
}]
```

## Protein Sequence Records and Alignments

### Sequence Records

A sequence record contains metadata about a sequence (what organism it's from, when it was obtained, it's accession number, etc...). The sequence records API provides all sequences records associated with a protein identified by it's MeSH ID.

**URL**: explorer/sequencerecord?mesh_id=[MESH ID]

**URL Example**: http://localhost:8000/explorer/sequencerecords?mesh_id=D064370

**Returns**: an array of all `explorer.SequenceRecord` objects belonging to the protein specified by mesh_id.

**Return Format**: Django-serialized.

**Example**:
```
[{
    "model": "explorer.sequencerecord",
    "pk": 1,
    "fields": {
        "protein": 1,
        "taxon": 4,
        "accession": "ADB10847.1",
        "organism": "Bovine coronavirus Bubalus/153/ITA/2008",
        "collection_date": "2008-04-01T00:00:00Z",
        "country": "Italy",
        "host": "Bubalus bubalis",
        "isolation_source": "intestinal content",
        "isolate": "153/08-B",
        "coded_by": "GU001946.1:132..>817"
    }
}, {
    "model": "explorer.sequencerecord",
    "pk": 2,
    "fields": {
        "protein": 1,
        "taxon": 5,
        "accession": "ADB10848.1",
        "organism": "Bovine coronavirus Bubalus/155/ITA/2008",
        "collection_date": "2008-04-01T00:00:00Z",
        "country": "Italy",
        "host": "Bubalus bubalis",
        "isolation_source": "intestinal content",
        "isolate": "155/08",
        "coded_by": "GU001947.1:132..>817"
    }
}]
```

### Sequence

A sequence is the single-letter amino acid code of a protein that has been aligned and represented with gaps (`-`). Sequences are identified by a protein MeSH ID, an alignment name and a comma-separated list of NCBI accession numbers (with versions).

**URL**: explorer/sequencerecord?mesh_id=[MESH ID]&alignment=[ALIGNMENT NAME]&accession=[COMMA-SEPARATED ACCESSION NUMBERS]

**URL Example**: http://localhost:8000/explorer/sequences?mesh_id=D064370&alignment=20200505&accession=P15777.1%2CABP38295.1%2CABP38267.1%2CP25190.1%2CP25191.1%2CQ9QAQ8.1%2C

**Returns**: an JSON-formatted list of objects contianing sequence alignment information for the provided accession numbers.

**Return Format**: `[ { accession:str, offset:int, seq:str}, ... ]`

**Example**:
```
[{
    "accession": "ABP38295.1",
    "seq": "MFLILLISLPTAFAV---------IGDLKCTT-----LSINDVD-TGV---PSISTDTVDVTNGLGTYYVLDRVYLNTTLLLNGYYPTSGSTYRNMALKGTLLLSTLWF---------------KPPFLSDFTNGIFAKVKNTKVI-----------KDGVMYSEFPAITIGSTFVNTSYSVVV---QPHTTIL----GNKLQG-------FLEISVCQ---------YTMCEYPNTICNPNLG-NQRVELWHWD-TG-VVSCLYKR---NFTYDVNA----DY-----LYFHFYQEGGTFYAYFTDTGVVTK--------------FLF---NVYLGTVLSHYYVM-PLTCNS-------------ALTLEYWVTPLTSKQYLLAFNQDGVIFNAVDCKSDFMSEIKCKTLSIAPSTGVYELNGYTVQPIADVYRRIPNLPDCN--IEAWL--NDKSVPSPLNWERKTFSNCNFNMSSLMSF-IQADSFTCNNIDAAKIYGMCFSSITIDKFAIPNGRKVDLQLGNLGYLQSFNYRIDTTATSCQLYYNLPAANVSVSRFNPSTWNRRFGFTEQSVFKPQPAGVFTDHDVVYAQHCFKAPTNFCPCKLDGSLCVGNGPGIDAGYKTSGIGTCPAGTN-----YLTCHN----------------AAQCDCLCTPDPITSKATGPY---KCPQTKYLVGIGEHCSGLAIKSDYCGGNP-------CSCQPQ------------AFLGWSVD-SCLQGDRCNIFANFILHDVNSGTTCSTDLQ---KSNTDIILGVCVNYDLYGITGQGIFVEVNATYYNSWQNLLYDSNGNLYGFRDYLTNRTFMIRSCYSGRVSAAFHA--NSSEPALLFRNIKCNYVFNNTL---SRQL---------QPINY-FDSYLGCVVNADNSTSIVVQ--TCDLTVGNGYCVDYST-----KRRSRRSITTGYRFTNFEPFTVNSVNDSLEPVGGLYEIQIPSEFTIGNMEEFIQTSSPKVTIDCSAFVCGDYAACKSQLVEYGSFCDNINAILTEVNELLDTTQLQVANSLMNGVTLSTKLKDGVNFNVDDINFSPVLGCLGSDCNKV-------SSRSAIEDLLFSKVKLSDVGFVEAYNNCTG---GAEIRDLICVQSYNGIKVLPPLLSENQISGYTLAATSASLFPPWSA----AAGVPFYLNVQYRINGIGVTMDVLSQNQKLIANAFNNALGAIQEGFDATNSALVKIQAVVNANAEALNNLLQQLSNRFGAISSSLQEILSRLDALEAQAQIDRLINGRLTALNAYVSQQLSDSTLVKFSAAQAMEKVNECVKSQSSRINFCGNGNHIISLVQNAPYGLYFIHFSYVPTKYVTAKVSPGLCIAG--GRGIAPKSGYFVNVNN----------SWMFTGSGYYYPEPIT-GNNVVVMSTCAVNYTKAPDVMLNIST--PNLPDFKEELDQWFKNQTSVAPDLSL----D--YINVTFLDLQDEMNRLQEAIKVLNQSYINLKDIGTYEYYVKWPWYVWLLIGFAGVAMLVLLFFICCCTGCGTSCFKK--CGGCCDDYTGHQELVIK---TSHED",
    "offset": 7
}, {
    "accession": "ABP38267.1",
    "seq": "MFLILLISLPTAFAV---------IGDLKCTT-----VSINDVD-TGV---PSISTDTVDVTNGLGTYYVLDRVYLNTTLLLNGYYPTSGSTYRNMALKGTLLLSTLWF---------------KPPFLSDFTNGIFAKVKNTKVV-----------KDGVMYSEFPAITIGSTFVNTSYSVVV---QPHTTIL----GNKLQG-------FLEISVCQ---------YTMCEYPNTICNPNLG-NQRVELWHWD-TG-VVSCLYKR---NFTYDVNA----DY-----LYFHFYQEGGTFYAYFTDTGVVTK--------------FLF---NVYLGTVLSHYYVM-PLTCNS-------------ALTLEYWVTPLTSKQYLLAFNQDGVIFNAVDCKSDFMSEIKCKTLSIAPSTGVYELNGYTVQPIADVYRRIPNLPDCN--IEAWL--NDKSVPSPLNWERKTFSNCNFNMSSLMSF-IQADSFTCNNIDAAKIYGMCFSSITIDKFAIPNGRKVDLQLGNLGYLQSFNYRIDTTATSCQLYYNLPAANVSVSRFNPSTWNRRFGFTEQSVFKPQPAGVFTDHDVVYAQHCFKAPTNFCPCKLDGSLCVGSGSGIDAGYKNTGIGTCPAGTN-----YLTCHN----------------AAQCNCLCTPDPITSKATGPY---KCPQTKYLVGIGEHCSGLAIKSDHCGGNP-------CSCQPQ------------AFLGWSVD-SCLQGDRCNIFANFILHDVNSGTTCSTDLQ---KSNTDIILGVCVNYDLYGITGQGIFVEVNATYYNSWQNLLYDSNGNLYGFRDYLTNRTFMIRSCYSGRVSAAFHA--NSSEPALLFRNIKCNYVFNNTL---SRQL---------QPINY-FDSYLGCVVNADNSTSSVVQ--TCDLTVGSGYCVDYST-----KRRSRRSITTGYRFTNFEPFTVNSVNDSLEPVGGLYEIQIPSEFTIGNMEEFIQTSSPKVTIDCSAFVCGDYAACKSQLVEYGSFCDNINAILTEVNELLDTTQLQVANSLMNGVTLSTKLKDGVNFNVDDINFSPVLGCLGSDCNKV-------SSRSAIEDLLFSKVKLSDVGFVEAYNNCTG---GAEIRDLICVQSYNGIKVLPPLLSENQISGYTLAATSASLFPPWSA----AAGVPFYLNVQYRINGIGVTMDVLSQNQKLIANAFNNALGAIQEGFDATNSALVKIQAVVNANAEALNNLLQQLSNRFGAISSSLQEILSRLDALEAQAQIDRLINGRLTALNAYVSQQLSDSTLVKFSAAQAMEKVNECVKSQSSRINFCGNGNHIISLVQNAPYGLYFIHFSYVPTKYVTAKVSPGLCIAG--GRGIAPKSGYFVNVNN----------TWMFTGSGYYYPEPIT-GNNVVVMSTCAVNYTKAPDVMLNIST--PNLPDFKEELDQWFKNQTSVAPDLSL----D--YINVTFLDLQDEMNRLQEAIKVLNQSYINLKDIGTYEYYVKWPWYVWLLIGFAGVAMLVLLFFICCCTGCGTSCFKK--CGGCCDDYTGHQELVIK---TSHED",
    "offset": 7
}]
```

### Nomenclature

A nomenclature names the positions of sequence alignment in the context of a reference sequence from that alignment. This allows one to say "I want residue *X* of the SARS-CoV-2 Spike", which a different position than residue *X* of the SARS-CoV or MERS-CoV spike.

Nomenclatures are generated for by the nomenclature API for an aligned reference sequence that is identified by its protein MeSH ID, accession number and alignemnt name. **Note** that only one accession number may be given here.

**URL**: explorer/nomenclature?mesh_id=[MESH ID]&alignment=[ALIGNMENT NAME]&accession=[ACCESSION]

**URL Example**: http://localhost:8000/explorer/nomenclature?mesh_id=D064370&alignment=20200505&accession=P25193.2

**Returns**: one two-element array contianing the major and minor position of the nomenclature, for every position in the reference sequence alignment, there the *n* th element gives the major and minor integer positions of the *n* th character in the aligned sequence.

**Return Format**: `[ [maj, min], [maj, min], ... ]`

**Example**:
```
[
    [0, 0],     # major, minor position for first character in aligned string
    [1, 0],     # major, minor position for second character in aligned string
    [2, 0],     # ...
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 0],
    [7, 0],
    [8, 0],
    [9, 0],
    [10, 0],
    [11, 0],
    [12, 0],
    [13, 0],
    [14, 0],
    [15, 0],
    [15, 1],    # first insert at position 15, sequence is a gap (-), minor=1
    [15, 2],    # second insert at position 15, sequence is a gap (-), minor=2
    [15, 3],    # third insert at position 15, sequence is a gap (-), minor=3
    [15, 4],
    [15, 5],
    [15, 6],
    [15, 7],
    [15, 8],
    [15, 9],
    [16, 0],    # now we're at position 16 in reference, past all the gaps
    [17, 0],
    [18, 0]],
```

## Immunological Epitopes and Experiments

### Epitope Experiment Classes

This URL returns distinct values for each field in the `explorer.models.EpitopeExperiments` given a protein MeSH ID and an alignment name. The fields are as follows:

| Name | Type | Description |
| host          | str | Host organism for the epitope experiment. |
| assay_type    | str | Type of assay. |
| assay_result  | str | Categorical string value describing assay result. |
| mhc_allele    | str | MHC allele if specified. |
| mhc_class     | str | MHC class if specified. |
| exp_method    | str | Experimental method used. |
| measurement_type | str | Description of the measurement meaning. |
| iedb_id       | str | IEDB IDs for epitopes (e.g. for all epitopes having the MeSH and alignment). |

**URL**: explorer/epitopeexperimentclasses?mesh_id=[MESH ID]&alignment=[ALIGNMENT NAME]

**URL Example**: http://localhost:8000/explorer/epitopeexperimentclasses?mesh_id=D064370&alignment=20200505

**Returns**: a list of distinct values for each field in the epitope experiments table.

**Return Format**: `{ [FIELD]: [VAL1, VAL2, VAL3...], ...`

**Example**:
```
{
    "host": ["Human", "Mouse", "Rabbit", "Chicken", "Chimpanzee", "Guinea pig", "Monkey", "Humanized (transgene)"], "assay_type": ["B Cell", "MHC Binding", "T Cell"],
    "assay_result": ["Positive", "Negative", "Positive-Low", "Positive-High", "Positive-Intermediate"],
    "mhc_allele": ["", "HLA-A*33:01", "HLA-A*03:01", "HLA-A*11:01", "HLA-A*68:01", "HLA-A*31:01", "HLA-DRB1*01:01", "HLA-B*18:01", "HLA-B*40:01", "HLA-B*40:02", "HLA-B*44:03", "HLA-B*44:02", "HLA-B*45:01", "Patr-B*24:01", "HLA-A*23:01", "HLA-A*24:02", "HLA-A*26:01", "HLA-A*29:02", "HLA-A*01:01", "HLA-A*30:02", "HLA-A*02:01", "HLA-A*68:02", "HLA-A*02:02", "HLA-A*02:03", "HLA-A*02:06", "HLA-B*35:01", "HLA-B*51:01", "HLA-B*53:01", "HLA-B*07:02", "HLA-B*54:01", "HLA-DRB1*04:01", "H2-d class II", "Patr-A*01:01", "H2-Db", "H2-Kb", "H2-b class I", "Patr-B*01:01", "H2-d class I", "Patr-A*07:01", "Patr-A*09:01", "Mamu-B*001:01", "HLA-B*08:01", "HLA-B*15:01", "HLA-B*27:05", "HLA-B*58:01", "HLA-A*68:23", "HLA-A*32:15", "HLA-A*69:01", "HLA-B*15:42", "HLA-B*45:06", "HLA-C*04:01", "HLA-A2", "H2 class I", "H2-b class II", "Patr-B*13:01", "HLA-C*07:02", "Mamu-B*017:04", "HLA-DRA*01:01/DRB1*07:01", "H2-Kd", "HLA-C*15:02", "HLA class II", "HLA-DR8", "HLA-C*14:02", "H2-k class I", "H2-k class II", "H2-IEk", "H2-IAb"],
    "mhc_class": ["", "I", "II"],
    ...
}
```

### Epitope Experiments

Data from epitope experimences is retreived using the `epitopeexperimentsfilter` URL, which requires at least one of the following criteria to be specified:

| Name | Type | Description |
|------|------|-------------|
| host          | str | Host organism for the epitope experiment. |
| assay_type    | str | Type of assay. |
| assay_result  | str | Categorical string value describing assay result. |
| mhc_allele    | str | MHC allele if specified. |
| mhc_class     | str | MHC class if specified. |
| exp_method    | str | Experimental method used. |
| measurement_type | str | Description of the measurement meaning. |
| iedb_id       | str | Filter experiments to those involving epitope with this IEDB ID. |

**URL**: localhost:8000/explorer/epitopeexperimentsfilter?alignment=[ALIGNMENT NAME]&mesh_id=[MESH ID]&[ADDITIONAL CRITERIA]

**URL Example**: http://localhost:8000/explorer/epitopeexperimentsfilter?alignment=20200505&mesh_id=D064370&host=Human&mhc_class=I&assay_result=Positive-High&iedb_id=73883

**Returns**: an array of experiment result hashes.

**Return Format**: `[{ [KEY]: [VALUE] }, ...]`

**Example**:
```
[
    {
        "host": "Human",
        "assay_type": "MHC Binding",
        "assay_result": "Positive-High",
        "mhc_allele": "HLA-A*23:01",
        "mhc_class": "I",
        "exp_method": "purified MHC/competitive/radioactivity",
        "measurement_type": "dissociation constant KD (~IC50)",
        "iedb_id": "73883"
    }, {
        "host": "Human",
        "assay_type": "MHC Binding",
        "assay_result": "Positive-High",
        "mhc_allele": "HLA-A*24:02",
        "mhc_class": "I",
        "exp_method": "purified MHC/competitive/radioactivity",
        "measurement_type": "dissociation constant KD (~IC50)",
        "iedb_id": "73883"
    }, {
        "host": "Human",
        "assay_type": "MHC Binding",
        "assay_result": "Positive-High",
        "mhc_allele": "HLA-A*29:02",
        "mhc_class": "I",
        "exp_method": "purified MHC/competitive/radioactivity",
        "measurement_type": "dissociation constant KD (~IC50)",
        "iedb_id": "73883"
    },
    ...
]
```

### Epitope Sequences

Epitope sequences are obtained through the `epitopesequence` URL and are specified with a MeSH ID, an alignment name and a comma-separated list of IEDB IDs.

**URL**: explorer/epitopesequence?alignment=[ALIGNMENT NAME]&mesh_id=[MESH ID]&iedb_id=[LIST OF IEDB IDS]

**URL Example**: http://localhost:8000/explorer/epitopesequence?alignment=20200505&mesh_id=D064370&iedb_id=73883%2C1220%2C2770

**Returns**: a list of epitope sequence objects.

**Return Format**: `[ { [KEY]: [VALUE] }, ...]`

**Example**:
```
[
    {
        "iedb_id": "2770",
        "offset": 470,
        "seq": "ALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFEL"
    }, {
        "iedb_id": "1220",
        "offset": 988,
        "seq": "AEVQIDRLI"
    }, {
        "iedb_id": "73883",
        "offset": 1055,
        "seq": "YFPREGVFVF"
    },
    ...
]
```

## Crystal Structures

### Crystal Structure Names and Chains
A collection of structures and their chains for a given protein are retreived through the `structurechains` URL and are identified by protein MeSH ID.

**URL**: explorer/structurechains?mesh_id=[MESH ID]

**URL Example**: http://localhost:8000/explorer/structurechains?mesh_id=D064370

**Returns**: A list of structure/chain objects

**Return Format**: `[ { [KEY]: [VALUE] }, ...]`

**Example**:
```
[
    {
        "taxon": "Severe acute respiratory syndrome-related coronavirus",
        "taxon_id": "694009",
        "pdb_id": "5WRG",
        "chain": "A"
    }, {
        "taxon": "Severe acute respiratory syndrome-related coronavirus",
        "taxon_id": "694009",
        "pdb_id": "5WRG",
        "chain": "B"
    }, {
        "taxon": "Severe acute respiratory syndrome-related coronavirus",
        "taxon_id": "694009",
        "pdb_id": "5WRG",
        "chain": "C"
    }, {
        "taxon": "Human coronavirus HKU1 (isolate N1)",
        "taxon_id": "443239",
        "pdb_id": "5GNB",
        "chain": "A"
    }, {
        "taxon": "Middle East respiratory syndrome-related coronavirus",
        "taxon_id": "1335626",
        "pdb_id": "5X5F",
        "chain": "A"
    },
    ...
]
```

### Crystal Structure Sequence Alignments
Multiple structure chain sequence alignments can be acccessed through the `structuresequence` URL and are identified by protein MeSH ID, alignment name and a comma-separated list of [PDB_ID].[CHAIN] identifiers.

**URL**: explorer/structuresequence?mesh_id=[MESH ID]&alignment=[ALIGNMENT]&pdbchains=[PDB.CHAIN LIST]

**URL Example**: http://localhost:8000/explorer/structuresequence?mesh_id=D064370&alignment=20200505&pdbchains=5X5B.A%2C5X5B.C

**Returns**: A list of structure sequence objects.

**Return Format**: `[ { [KEY]: [VALUE] }, ...]`

**Example**:
```
[
    {
        "pdbchain": "5X5B.A",
        "pdb_id": "5X5B",
        "chain": "A",
        "sequence": "RCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFDNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFS--------------TWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVR--------LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFE---------------------DLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHT-------------------KSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKV-----------------------TDLICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------SWFITQRNFFSPQIIT-TDNTFV---------------------------------------------------------------------------------------------------------------------------------------------------------------",
        "offset": 35
    }, {
        "pdbchain": "5X5B.C",
        "pdb_id": "5X5B",
        "chain": "C",
        "sequence": "RCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFDNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFS--------------TWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVRF-PNITN-LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFELLNAPATVCGPK-L-----STDLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHT-------------------KSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKV-----------------------T-LICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------SWFITQRNFFSPQIIT-TDNTFV---------------------------------------------------------------------------------------------------------------------------------------------------------------",
        "offset": 35
    },
    ...
]
```

### Crystal Structure Residue Info and Coordinates

To get residue information and the coordinates of an atom (across all residues), use the `structureresidueatoms` URL. You need to specify a protein MeSH ID, an atom name and a comma-separated list of [PDB ID].[CHAIN].

**Note** that this URL uses nested queries and should be optimized to use a more efficient and faster method.

**URL**: explorer/structureresidueatoms?mesh_id=D064370&atom=CA&pdbchains=5X5B.A%2C5X5B.C

**URL Example**: http://localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&atom=CA&pdbchains=5X5B.A%2C5X5B.C

**Returns**: A list of pdb/chain objects with residue/atom data.

**Return Format**: `[ { [PDB.CHAIN]: { [KEY]: [VALUE] } }, ...]`

**Example**:
```
[
    {
        "pdbchain": "5X5B.A",
        "pdb_id": "5X5B",
        "chain": "A",
        "residues": [
            {
                "resid": 18,
                "resix": 0,
                "resn": "R",
                "atom": "CA",
                "atom_x": 46.76,
                "atom_y": -31,
                "atom_z": 43,
                "element": "C",
                "charge": 0
            }, {
                "resid": 19,
                "resix": 1,
                "resn": "C",
                "atom": "CA",
                "atom_x": 49.18,
                "atom_y": -28,
                "atom_z": 42,
                "element": "C",
                "charge": 0
            },
            ...
    },
    ...
]
```








fin.
