RESIDUE_COLOR_MAP = {
    'D':'rgba(230,10,10, 0.5)',
    'E':'rgba(230,10,10, 0.5)',
    'C':'rgba(230,230,0, 0.5)',
    'M':'rgba(230,230,0, 0.5)',
    'R':'rgba(20,90,255, 0.5)',
    'K':'rgba(20,90,255, 0.5)',
    'S':'rgba(250,150,0, 0.5)',
    'T':'rgba(250,150,0, 0.5)',
    'F':'rgba(50,50,170, 0.5)',
    'Y':'rgba(50,50,170, 0.5)',
    'N':'rgba(0,220,220, 0.5)',
    'Q':'rgba(0,220,220, 0.5)',
    'G':'rgba(235,235,235, 0.5)',
    'L':'rgba(15,130,15, 0.5)',
    'V':'rgba(15,130,15, 0.5)',
    'I':'rgba(15,130,15, 0.5)',
    'A':'rgba(200,200,200, 0.5)',
    'W':'rgba(180,90,180, 0.5)',
    'H':'rgba(130,130,210, 0.5)',
    'P':'rgba(220,150,130, 0.5)',
    '-':'rgba(255,255,255, 1)',
    'X':'rgba(255,255,255, 1)',
    }

# 1. Request sequence alignments for accession IDs  YP_009724390.1 (early SARS-CoV-2 isolate Wuhan-Hu-1), QIS61410.1 (late SARS-CoV-2 isolate SARS-CoV-2/human/USA/WA-UW376/2020) from API.
# 2. Request alignment nomenclature for accession YP_009724390.1 from API.

ALIGNMENT_NAME = '20200505'
MESH_ID='D064370'

SELECTED_ACCESSIONS = [
    'YP_009724390.1','QIS61410.1','AHN64783.1'
]

SELECTED_EPITOPES = [
    12967, 100347, 64085, 74367
]

# SELECTED_STRUCTURES = [
#     'YP_009724390.1','QIS61410.1','AHN64783.1'
# ]

# 4. PDB ID 5WRG, chain A, taxon “Severe acute respiratory syndrome-related coronavirus” should be selected.
