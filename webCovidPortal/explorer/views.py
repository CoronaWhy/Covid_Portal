from django.shortcuts import render;
from django.http import HttpResponse;
from django.core import serializers;
from django.db.models import Q;
import json;
from explorer.models import Taxon, SequenceRecord, Sequence, EpitopeExperiment, Epitope, Protein, Alignment, Structure, StructureChain, StructureChainSequence, StructureChainResidue, StructureAtom;
from django.db.models import Value as V, CharField, F;
from django.db.models.functions import Concat, Cast;
import pprint as pp;

def error_response(msg):
    response = HttpResponse(
        json.dumps({'message': msg}),
        content_type="application/json");
    response.status_code=400;
    return response;

def index(request):
    context = { };
    return render(request, 'explorer/index.html', context);
################################################################################
def taxa(request):
    if request.method=="GET":
        return HttpResponse(
            serializers.serialize("json", Taxon.objects.all()),
            content_type="application/json");

################################################################################
# SEQUENCE RECORDS, ALIGNMENTS AND NOMENCLATURES
################################################################################
def sequencerecords(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;
        # URL ENCODED FOR SPIKE
        # 127.0.0.1:8000/explorer/sequencerecords?mesh_id=D064370
        # http://127.0.0.1:8000/explorer/sequencerecords?mesh_id=D064370&host=Homo%20sapiens&country=USA%2CChina

################################################################################
def sequences(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    if len(recs)<1:
        return error_response("No records");
    else:
        response = HttpResponse(
            json.dumps(recs),
            content_type="application/json");
        return response;

    # sample accessions
    # ADB10848.1,ADB10845.1,ADB10846.1,ABV74054.1,ABG89288.1,ACT10995.1, ABP38243.1,ACT10983.1,ABI93999.2,Q9QAR5.1,P25192.1,P15777.1,ABP38295.1, ABP38267.1,P25190.1,P25191.1,Q9QAQ8.1,P25193.2,P25194.1,Q91A26.1,

    # URL encoded
    # 127.0.0.1:8000/explorer/sequences?mesh_id=D064370&alignment=20200505&accession=ADB10848.1%2CADB10845.1%2CADB10846.1%2CABV74054.1%2CABG89288.1%2CACT10995.1%2C%20ABP38243.1%2CACT10983.1%2CABI93999.2%2CQ9QAR5.1%2CP25192.1%2CP15777.1%2CABP38295.1%2C%20ABP38267.1%2CP25190.1%2CP25191.1%2CQ9QAQ8.1%2CP25193.2%2CP25194.1%2CQ91A26.1
################################################################################
def nomenclature(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    # build and send
    nom = [];
    minor = 0;
    major = 0;
    for i,r in enumerate(seq.sequence):
        if r=='-':
            minor+=1;
        else:
            minor = 0;
            major+=1;
        nom.append([major,minor]);
    response = HttpResponse(
        json.dumps(nom),
        content_type="application/json");
    return response;

    # 127.0.0.1:8000/explorer/nomenclature?mesh_id=D064370&alignment=20200505&accession=ABG78748.1
################################################################################
# EPITOPES
################################################################################
def epitopeexperimentclasses(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    response = HttpResponse(
        json.dumps(distinct_fieldvalues),
        content_type="application/json");
    return response;

    # http://127.0.0.1:8000/explorer/epitopeexperimentclasses?mesh_id=D064370&alignment=20200505
################################################################################
def epitopeexperimentsfilter(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    if len(qs)<=2:
        return error_message("At least one criterion must be specified");
        # other than MeSH and alignment.

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
    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;

    # localhost:8000/explorer/epitopeexperimentsfilter?alignment=20200505&mesh_id=D064370&host=Human&mhc_class=I&assay_result=Positive-High&iedb_id=73883
################################################################################
def epitopesequence(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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
    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;

    # localhost:8000/explorer/epitopesequence?alignment=20200505&mesh_id=D064370&iedb_id=73883%2C1220%2C2770
################################################################################
# CRYSTAL STRUCTURES
################################################################################
def structurechains(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");

    # fetch
    recs = [];
    for r in StructureChain.objects.filter(
        protein__mesh_id=params['mesh_id'],
    ):
        recs.append({
            'taxon'             : r.structure.taxon.name,
            'taxon_id'          : r.structure.taxon.gb_taxon_id,
            'pdb_id'            : r.structure.pdb_id,
            'chain'             : r.name
        });

    # return
    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;

    # http://localhost:8000/explorer/structurechains?mesh_id=D064370
################################################################################
def structuresequence(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

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

    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;

    # http://localhost:8000/explorer/structuresequence?mesh_id=D064370&alignment=20200505&pdbchains=5X5B.A%2C5X5B.C
################################################################################
def structureresidueatoms(request):
    if request.method=="GET":
        params = request.GET;
    elif request.method=="POST":
        params = request.POST;
    else:
        return error_respone("Invalid request");

    if not 'mesh_id' in params:
        return error_response("No MeSH ID specified");
    if not 'atom' in params:
        return error_response("No atom specified");
    if not 'pdbchains' in params:
        return error_response("No PDB/Chains specified");

    pdbchains = params['pdbchains'].split(',');
    pdb_ids, chains = zip(*[v.split('.') for v in pdbchains]);

    # Currently using nested queries, join will probably be more efficient? How to do joins with Django?

    recs = [];
    for pc in StructureChain.objects.annotate(
        pdb_chain=Concat("structure__pdb_id", V("."), "name")
    ).filter(
        pdb_chain__in=(pdbchains)
    ):
        residues = [];
        for r in StructureAtom.objects.filter(
            residue__chain=pc,
            atom=params['atom'],
        ):
            residues.append({
                'resid'     : r.residue.resid,
                'resix'     : r.residue.resix,
                'resn'      : r.residue.resn,
                'atom'      : r.atom,
                'atom_x'    : round(r.x,2),
                'atom_y'    : round(r.y),
                'atom_z'    : round(r.z),
                'element'   : r.element,
                'charge'    : r.charge,
            });

        recs.append({
            'pdbchain'  : pc.structure.pdb_id + "." + r.residue.chain.name,
            'pdb_id'    : pc.structure.pdb_id,
            'chain'     : pc.name,
            'residues'  : residues,
        });

    response = HttpResponse(
        json.dumps(recs),
        content_type="application/json");
    return response;

    # http://localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&atom=CA&pdbchains=5X5B.A%2C5X5B.C
################################################################################
# fin.
