from django.shortcuts import render;
# from django.http import HttpResponse;
from django.core import serializers;
from django.db.models import Q;
import json;
from explorer.models import Taxon, SequenceRecord, Sequence, EpitopeExperiment, Epitope, Protein, Alignment, Structure, StructureChain, StructureChainSequence, StructureChainResidue, StructureAtom, StructureChainResidueAlignment, StructureChainSequence;
from django.db.models import Value as V, CharField, F;
from django.db.models.functions import Concat, Cast;
import pprint as pp;
import numpy as np, pandas as pd;

# def error_response(msg):
#     response = HttpResponse(
#         json.dumps({'message': msg}),
#         content_type="application/json");
#     response.status_code=400;
#     return response;

# def index(request):
#     context = { };
#     return render(request, 'explorer/index.html', context);
################################################################################
# def taxa(request):
#     if request.method=="GET":
#         return HttpResponse(
#             serializers.serialize("json", Taxon.objects.all()),
#             content_type="application/json");

################################################################################
# SEQUENCE RECORDS, ALIGNMENTS AND NOMENCLATURES
################################################################################
# def sequencerecords(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def sequencerecords(params):
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    criteria = {
        # 'taxon_id':str,  # see below
        'accession':str,
        'organism':str,
        'country':str,
        'host':str,
        'isolation_source':str,
        'isolate':str,
    };

    # build query
    qs = [ Q(protein__mesh_id=params['mesh_id']) ];
    for k in criteria:
        if k in params:
            qs.append(Q(**{k+"__in":params[k].split(',')}));
    # do taxon separately b/c it's a foreign key
    if 'taxon_id' in params:
        qs.append(Q(taxon__gb_taxon_id__in=(params['taxon_id'].split(','))));

    recs = [];
    for r in SequenceRecord.objects.filter(
        protein__mesh_id=params['mesh_id'],
        *qs
    ):
        if Sequence.objects.filter(sequence_record = r).exists():
            recs.append({
                'accession':r.accession,
                'organism':r.organism,
                'collection_date':str(r.collection_date),
                'country':r.country,
                'host':r.host,
                'isolation_source':r.isolation_source,
                'isolate':r.isolate,
                'taxon_id':r.taxon.gb_taxon_id,
                'coded_by':r.coded_by,
            });

    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;
        # URL ENCODED FOR SPIKE
        # 127.0.0.1:8000/explorer/sequencerecords?mesh_id=D064370
        # http://127.0.0.1:8000/explorer/sequencerecords?mesh_id=D064370&host=Homo%20sapiens&country=USA%2CChina

################################################################################
# def sequences(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def sequences(params):

    # all by accession
    if not 'accession' in params:
        return error_response("No valid criteria");
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    # retreive
    accessions = params['accession'].split(',');
    if len(accessions)<1:
        return error_response("No criteria specified");

    recs = [];
    for r in Sequence.objects.filter(
        alignment__name=params['alignment'],
        sequence_record__protein__mesh_id=params['mesh_id'],
        sequence_record__accession__in=accessions
    ):
        recs.append({
            'accession': r.sequence_record.accession,
            'seq': r.sequence,
            'offset': r.offset,
        });

    return recs;
    # if len(recs)<1:
    #     return error_response("No records");
    # else:
    #     response = HttpResponse(
    #         json.dumps(recs),
    #         content_type="application/json");
    #     return response;

    # sample accessions
    # ADB10848.1,ADB10845.1,ADB10846.1,ABV74054.1,ABG89288.1,ACT10995.1, ABP38243.1,ACT10983.1,ABI93999.2,Q9QAR5.1,P25192.1,P15777.1,ABP38295.1, ABP38267.1,P25190.1,P25191.1,Q9QAQ8.1,P25193.2,P25194.1,Q91A26.1,

    # URL encoded
    # 127.0.0.1:8000/explorer/sequences?mesh_id=D064370&alignment=20200505&accession=ADB10848.1%2CADB10845.1%2CADB10846.1%2CABV74054.1%2CABG89288.1%2CACT10995.1%2C%20ABP38243.1%2CACT10983.1%2CABI93999.2%2CQ9QAR5.1%2CP25192.1%2CP15777.1%2CABP38295.1%2C%20ABP38267.1%2CP25190.1%2CP25191.1%2CQ9QAQ8.1%2CP25193.2%2CP25194.1%2CQ91A26.1
################################################################################
# def nomenclature(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def nomenclature(params):
    if not 'accession' in params:
        return error_response("No valid criteria");
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    # retreive
    try:
        seq = Sequence.objects.get(
            alignment__name=str(params['alignment']),
            sequence_record__protein__mesh_id=str(params['mesh_id']),
            sequence_record__accession=str(params['accession']),
        );
    except Exception as e:
        return error_response(str(e));

    # nomenclature format
    nomenclature_format = "minor_alphabet";


    # build and send
    nom = [];
    minor = 0;
    major = 0;
    # nomenclature format generators -------------------------------------------
    def minor_alphabet(major,minor,delimeter='.'):
        def minor_gen(minor):
            if minor==0: return "";
            if minor<=26:
                return chr(ord('a')+minor);
        if minor==0:
            return str(major);
        else:
            return str(major)+str(delimeter)+minor_gen(minor);
    # --------------------------------------------------------------------------
    nomenclature_generators = {
        'minor_alphabet'        : minor_alphabet,
    };
    # generate nomenclature ----------------------------------------------------
    try:
        for i,r in enumerate(seq.sequence):
            if r=='-':
                minor+=1;
            else:
                minor = 0;
                major+=1;
            nom.append(
                nomenclature_generators[nomenclature_format](
                    major,
                    minor,
                    delimeter=''
                )
            );
    except Exception as e:
        return error_response("Reference does not conform to the nomenclature format requested: "+str(e));
    # send results -------------------------------------------------------------
    return recs;
    # response = HttpResponse(
    #     json.dumps(nom),
    #     content_type="application/json");
    # return response;

    # 127.0.0.1:8000/explorer/nomenclature?mesh_id=D064370&alignment=20200505&accession=ABG78748.1
################################################################################
# EPITOPES
################################################################################
# def epitopeexperimentclasses(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def epitopeexperimentclasses(params):
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    # get list of distinct values for the following EpitopeExperiments:
    distinct_fieldvalues = {
        'host'              : [],
        'assay_type'        : [],
        'assay_result'      : [],
        'mhc_allele'        : [],
        'mhc_class'         : [],
        'exp_method'        : [],
        'measurement_type'  : [],
    };
    for k in distinct_fieldvalues.keys():
        distinct_fieldvalues[k] = list(
            EpitopeExperiment.objects.filter(
                epitope__protein__mesh_id=params['mesh_id'],
                epitope__alignment__name=params['alignment'],
            ).values_list(
                k,
                flat=True
            ).distinct()
        );
    # get distinct IEDB IDs
    distinct_fieldvalues['iedb_id'] = list(
        Epitope.objects.filter(
            protein__mesh_id=params['mesh_id'],
            alignment__name=params['alignment'],
        ).values_list(
            'IEDB_ID',
            flat=True
        ).distinct()
    );
    return recs;
    # response = HttpResponse(
    #     json.dumps(distinct_fieldvalues),
    #     content_type="application/json");
    # return response;

    # http://127.0.0.1:8000/explorer/epitopeexperimentclasses?mesh_id=D064370&alignment=20200505
################################################################################
# def epitopeexperimentsfilter(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def epitopeexperimentsfilter(params):
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    criteria = {
        # 'iedb_id': str, # see below
        'host': str,
        'assay_type': str,
        'assay_result': str,
        'mhc_allele': str,
        'mhc_class': str,
        'exp_method': str,
        'measurement_type': str,
    };

    # build queryset
    qs = [
        Q(epitope__alignment__name=params['alignment']),
        Q(epitope__protein__mesh_id=params['mesh_id']),
    ];
    for k in criteria.keys():
        if k in params:
            qs.append(Q(**{k+"__in":params[k].split(',')}));
    # iedb_id is done separately since it's a foreign key
    if 'iedb_id' in params:
        qs.append(Q(epitope__IEDB_ID__in=params['iedb_id'].split(',')));

    # if len(qs)<=2:
    #     return error_message("At least one criterion must be specified");

    # fetch
    recs = [];
    for r in EpitopeExperiment.objects.filter( *qs ):
        recs.append({
            'host'              : r.host,
            'assay_type'        : r.assay_type,
            'assay_result'      : r.assay_result,
            'mhc_allele'        : r.mhc_allele,
            'mhc_class'         : r.mhc_class,
            'exp_method'        : r.exp_method,
            'measurement_type'  : r.measurement_type,
            'iedb_id'           : r.epitope.IEDB_ID
        });

    # return
    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;

    # localhost:8000/explorer/epitopeexperimentsfilter?alignment=20200505&mesh_id=D064370&host=Human&mhc_class=I&assay_result=Positive-High&iedb_id=73883
################################################################################
# def epitopesequence(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def epitopesequence(params):
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'iedb_id' in params:
        return error_response("No IEDB IDs specified");

    # separate ids
    iedb_ids = params['iedb_id'].split(',');

    # fetch
    recs = [];
    for r in Epitope.objects.filter(
        alignment__name=params['alignment'],
        protein__mesh_id=params['mesh_id'],
        IEDB_ID__in=(iedb_ids)
    ):
        recs.append({
            'iedb_id': r.IEDB_ID,
            'offset': r.offset,
            'seq': r.sequence
        });

    # return
    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;

    # localhost:8000/explorer/epitopesequence?alignment=20200505&mesh_id=D064370&iedb_id=73883%2C1220%2C2770
################################################################################
# CRYSTAL STRUCTURES
################################################################################
# def structurechains(request):
#
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def structurechains(params):

    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'alignment' in params:
        return error_response("No alignment specified");
    # fetch
    recs = [];
    for r in StructureChainSequence.objects.filter(
        chain__protein__mesh_id=params['mesh_id'],
        alignment__name=params['alignment'],
    ):
        recs.append({
            'taxon'             : r.chain.structure.taxon.name,
            'taxon_id'          : r.chain.structure.taxon.gb_taxon_id,
            'pdb_id'            : r.chain.structure.pdb_id,
            'chain'             : r.chain.name
        });

    # return
    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;

    # http://localhost:8000/explorer/structurechains?mesh_id=D064370
################################################################################
# def structuresequence(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");

def structuresequence(params):
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'pdbchains' in params:
        return error_response("No PDB/Chains specified");

    pdbchains = params['pdbchains'].split(',');
    pdb_ids, chains = zip(*[v.split('.') for v in pdbchains]);

    recs = [];
    for r in StructureChainSequence.objects.filter(
        chain__structure__pdb_id__in=(pdb_ids),
        chain__protein__mesh_id=params['mesh_id'],
        alignment__name=params['alignment']
    ).annotate(
        pdb_chain=Concat("chain__structure__pdb_id", V("."), "chain__name")
    ).filter(
        pdb_chain__in=(pdbchains)
    ):
        recs.append({
            'pdbchain'  : r.chain.structure.pdb_id + "." + r.chain.name,
            'pdb_id'    : r.chain.structure.pdb_id,
            'chain'     : r.chain.name,
            'sequence'  : r.sequence,
            'offset'    : r.offset,
        });

    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;

    # http://localhost:8000/explorer/structuresequence?mesh_id=D064370&alignment=20200505&pdbchains=5X5B.A%2C5X5B.C
################################################################################
# def structureresidueatoms(request):
#     if request.method=="GET":
#         params = request.GET;
#     elif request.method=="POST":
#         params = request.POST;
#     else:
#         return error_respone("Invalid request");
def structureresidueatoms(params):
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'atom' in params:
        return error_response("No atom specified");
    if not 'pdbchains' in params:
        return error_response("No PDB/Chains specified");
    if not 'alignment' in params:
        return error_response("No alignment specified");

    pdbchains = params['pdbchains'].split(',');
    pdb_ids, chains = zip(*[v.split('.') for v in pdbchains]);
    atom_names = params['atom'].split(',');

    # Currently using nested queries, join will probably be more efficient? How to do joins with Django?

    # desired sql:
    # localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&atom=CA&pdbchains=5X5B.A
    recs = [];

    for sc in StructureChain.objects.annotate(
        pdb_chain=Concat(
            'structure__pdb_id',
            V("."),
            'name'
        )
    ).filter(
        pdb_chain__in=(pdbchains),
        protein__mesh_id=params['mesh_id'],
    ):
        # get alignment
        resalns = pd.DataFrame(
            sc.structurechainsequence_set.get(
                alignment__name=params['alignment']
            ).structurechainresiduealignment_set.values(
                'id','residue_id','resaln'
            )
        );

        # get atoms
        atoms = pd.DataFrame(
            StructureAtom.objects.annotate(
                pdb_chain=Concat(
                    'residue__chain__structure__pdb_id',
                    V("."),
                    'residue__chain__name'
                )
            ).filter(
                atom__in=(atom_names),
                pdb_chain=sc.pdb_chain,
            ).values(
                'residue_id',
                'atom',
                'element',
                'charge',
                'occupancy',
                'x',
                'y',
                'z',
                'residue__resix',
                'residue__resid',
                'residue__resn',
            )
        );
        atoms.index = atoms['residue_id'];

        resalns.index = resalns['residue_id'];

        # merge on residueid
        result = pd.concat([atoms,resalns],axis=1);

        # drop duplicate column names
        result = result.loc[:,~result.columns.duplicated()];

        # rename and trim
        result = result.rename(
            columns={
                'residue__resix':'resix',
                'residue__resid':'resid',
                'residue__resn':'resn',
            })[[
                'atom',
                'element',
                'charge',
                'occupancy',
                'x',
                'y',
                'z',
                'resaln',
                'resix',
                'resid',
                'resn',
        ]];

        # store
        recs.append({
            'pdb_id': sc.structure.pdb_id,
            'chain': sc.name,
            'pdb_chain': sc.structure.pdb_id+"."+sc.name,
            'alignment': params['alignment'],
            'atoms': result.to_dict(orient='records')
        });

    # return
    return recs;
    # response = HttpResponse(
    #     json.dumps(recs),
    #     content_type="application/json");
    # return response;
    # localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&atom=CA&pdbchains=5X5B.A

    # http://localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&alignment=20200505&atom=CA&pdbchains=5X5B.A%2C5X5B.C
################################################################################






# Updated strcutre-alignment API functions
################################################################################
# def structuresequencecoords(request):
def structuresequencecoords(params):
# localhost:8000/explorer/structuresequencecoords?mesh_id=D064370&alignment=20200505&pdb_id=5X5B&chain=A
    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'alignment' in params:
        return error_response("No alignment specified");
    if not 'pdb_id' in params:
        return error_response("No PDB ID specified");
    if not 'chain' in params:
        return error_response("No chain specified");

    sequence_record = getstructurechainsequence(
        params['mesh_id'],
        params['alignment'],
        params['pdb_id'],
        params['chain']
    );

    atoms = getstructureatoms(
        params['mesh_id'],
        params['alignment'],
        params['pdb_id'],
        params['chain'],
        'CA',
    );
    print(sequence_record);
    # confirm matching offsets
    try:
        if len(''.join(atoms[0:sequence_record['offset']-1]))>0:
            return error_response("Sequence and residue coordinate offsets do not match.");
    except:
        return error_response("An error occurred comparing offsets.");
    # trim offset from atoms
    atoms = atoms[sequence_record['offset']-1:];
    print(atoms);
    print("number atoms: "+str(len(atoms)));
    print("Sequence length: "+str(len(sequence_record['sequence'])));

    data = {
            'pdb_id': sequence_record['pdb_id'],
            'sequence': sequence_record['sequence'],
            'chain': sequence_record['chain'],
            'offset': sequence_record['offset'],
            'coords': ";".join(atoms),
        }

    # response = HttpResponse(
    #     json.dumps({
    #         'pdb_id': sequence_record['pdb_id'],
    #         'sequence': sequence_record['sequence'],
    #         'chain': sequence_record['chain'],
    #         'offset': sequence_record['offset'],
    #         'coords': ";".join(atoms),
    #     }),
    #     # conform to (react) explorerDataModels.StructureSequenceModel
    #     # json.dumps([
    #     #     sequence_record['pdb_id'],     # label
    #     #     sequence_record['sequence'],   # sequence
    #     #     sequence_record['chain'],      # value
    #     #     [],                         # styles
    #     #     sequence_record['offset'],     # offset
    #     #     ";".join(atoms),                      # coords
    #     # ]),
    #     content_type="application/json");
    return data
################################################################################
def getstructurechainsequence(mesh_id, alignment, pdb_id, chain):
    r = StructureChainSequence.objects.get(
        chain__structure__pdb_id=pdb_id,
        chain__name=chain,
        chain__protein__mesh_id=mesh_id,
        alignment__name=alignment,
    );
    return {
        'pdbchain'  : r.chain.structure.pdb_id + "." + r.chain.name,
        'pdb_id'    : r.chain.structure.pdb_id,
        'chain'     : r.chain.name,
        'sequence'  : r.sequence,
        'offset'    : r.offset,
    };
################################################################################
def getstructureatoms(mesh_id, alignment, pdb_id, chain, atom):
    recs = [];

    sc = StructureChain.objects.get(
            structure__pdb_id=pdb_id,
            protein__mesh_id=mesh_id,
            name=chain
        );

    # alignment
    resalns = pd.DataFrame(
        sc.structurechainsequence_set.get(
            alignment__name=alignment
        ).structurechainresiduealignment_set.values(
            'id','residue_id','resaln'
        )
    );

    # get atoms
    atoms = pd.DataFrame(
        StructureAtom.objects.filter(
            atom=atom,
            residue__chain__structure__pdb_id=pdb_id,
            residue__chain__name=chain,
        ).values(
            'residue_id',
            # 'atom',
            # 'element',
            # 'charge',
            # 'occupancy',
            'x',
            'y',
            'z',
            'residue__resix',
            'residue__resid',
            'residue__resn',
        )
    );

    atoms['x'] = atoms['x'].astype(float).round(decimals=3);
    atoms['y'] = atoms['y'].astype(float).round(decimals=3);
    atoms['z'] = atoms['z'].astype(float).round(decimals=3);
    atoms.index = atoms['residue_id'];
    resalns.index = resalns['residue_id'];

    # merge on residueid
    result = pd.concat([atoms,resalns],axis=1);

    # drop duplicate column names
    result = result.loc[:,~result.columns.duplicated()];
    result['resaln'] = result['resaln'].astype(int);
    result['coords'] = \
        result['x'].astype(str)+","+ \
        result['y'].astype(str)+","+ \
        result['z'].astype(str);

    # get max length of coord string for numpy full
    result['coordlength'] = result['coords'].str.len();
    dtype = "U"+str(result['coordlength'].max());

    aligned_coords = np.full(result['resaln'].max(),'',dtype=dtype);
    for i,r in result.iterrows():
        aligned_coords[(r['resaln']-1)] = r['coords'];
    return aligned_coords;

# fin.
