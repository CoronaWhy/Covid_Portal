The explorer API serves sequence alignemnts etc. to the front end.

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








fin.
