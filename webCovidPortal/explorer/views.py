from django.shortcuts import render;
from django.http import HttpResponse;
from django.core import serializers;
import json;
from explorer.models import Taxon, SequenceRecord, Sequence;
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
def sequencerecords(request):
    if request.method=="GET":
        # get by protein mesh_id
        if not 'mesh_id' in request.GET:
            return error_response("No valid criteria");
        # retreive
        recs = SequenceRecord.objects.filter(
            protein__mesh_id=request.GET['mesh_id']
        );
        # return records or empty
        if len(recs)<1:
            return error_response("No records");
        else:
            response = HttpResponse(
                serializers.serialize("json", recs),
                content_type="application/json");
            return response;
        # URL ENCODED FOR SPIKE
        # 127.0.0.1:8000/explorer/sequencerecords?mesh_id=D064370
################################################################################
def sequences(request):
    if request.method=="GET":
        # all by accession
        if not 'accession' in request.GET:
            return error_response("No valid criteria");
        if not 'alignment' in request.GET:
            return error_response("No alignment specified");
        if not 'mesh_id' in request.GET:
            return error_response("No MeSH ID specified");

        # retreive
        accessions = request.GET['accession'].split(',');
        if len(accessions)<1:
            return error_response("No criteria specified");

        recs = [];
        for r in Sequence.objects.filter(
            alignment__name=request.GET['alignment'],
            sequence_record__protein__mesh_id=request.GET['mesh_id'],
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
        if not 'accession' in request.GET:
            return error_response("No valid criteria");
        if not 'alignment' in request.GET:
            return error_response("No alignment specified");
        if not 'mesh_id' in request.GET:
            return error_response("No MeSH ID specified");

        # retreive
        try:
            seq = Sequence.objects.get(
                alignment__name=str(request.GET['alignment']),
                sequence_record__protein__mesh_id=str(request.GET['mesh_id']),
                sequence_record__accession=str(request.GET['accession']),
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
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
# fin.
