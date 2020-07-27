from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import pymongo
import hashlib
import pandas as pd
import shutil
import io
import os
import sys
import json
import traceback
import numpy as np
import seaborn as sns
import gzip
import nibabel as nib
import subprocess
from django import forms
from PIL import Image
import datetime
import base64
from glob import glob
import jwt
import datetime
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import json
import glob
from explorer.models import *
from explorer.explorerapi import *
from covidPortalApp.covidPortalAppObjs import *
from covidPortalApp.covidPortalAppConstants import *
from django.contrib.auth import authenticate
import time
import paramiko
import asyncio, asyncssh, sys
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def monitorJobs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        userName = data["userName"]
        users = User.objects.filter(username = userName)
        if len(users) > 0:
            user = users[0]
            uploadFolders = uploadFolder.objects.filter(user = user)
            uploadFolders = [x for x in uploadFolders if x.status != 'Uploaded' and s.status != 'Analysis Completed']
            uploadFolderJSON = [{'name':x.name,'chksum':x.chksum,'user':str(x.user),
            'description':x.description, 'id':x.id,'status':x.status,
            'fileName':x.fileName,'uploadedDate':x.uploadedDate.strftime('%Y-%m-%d'),
            'analysisProtocol':x.analysisProtocol,
            'fileType':uploadFolder.fileType,
            'analysisSubmittedDate':x.analysisSubmittedDate.strftime('%Y-%m-%d') if x.analysisSubmittedDate else '',
            'rowColor':statusColorMap[x.status], "resultsAvailable":"no"} for x in uploadFolders]
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps(uploadFolderJSON), content_type="application/json")

def getUserProfile(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter (username = username)
        if len(users) > 0:
            user = users[0]
            covidUser = CovidUser.objects.filter(user = user)[0]
            userJSON = {"username":covidUser.user.username, "addressLine1":covidUser.addressLine1, "addressLine2":covidUser.addressLine2, "city":covidUser.city, "state":covidUser.state, "zipCode":covidUser.zipCode, "phoneNumber":covidUser.phoneNumber, "email":covidUser.user.email}
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps(userJSON), content_type="application/json")

def updateUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter (username = username)
        if len(users) > 0:
            user = users[0]
            covidUser = CovidUser.objects.filter(user = user)[0]

            covidUser.addressLine1 = data["addressLine1"]
            covidUser.addressLine2 = data["addressLine1"]
            covidUser.city = data["city"]
            covidUser.state = data["state"]
            covidUser.zipCode = data["zipCode"]
            covidUser.phoneNumber = data["phoneNumber"]

            covidUser.save()

            userJSON = {"username":covidUser.user.username, "addressLine1":covidUser.addressLine1, "addressLine2":covidUser.addressLine2, "city":covidUser.city, "state":covidUser.state, "zipCode":covidUser.zipCode, "phoneNumber":covidUser.phoneNumber, "email":covidUser.user.email}
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed to update profile.", "user":{} } ), content_type="application/json")
    return HttpResponse(json.dumps({"message":"User profile updated.", "user":userJSON}), content_type="application/json")

def signupUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        email = data["email"]

        addressLine1 = data["addressLine1"]
        addressLine2 = data["addressLine2"]
        city = data["city"]
        state = data["state"]
        zipCode = data["zipCode"]
        phoneNumber = data["phoneNumber"]
        print(" username " + username + " password " + password + " email " + email)
        users = User.objects.filter(username = username)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
        else:
            user = User.objects.create_user(username, email, password)

            covidUser = CovidUser ()
            covidUser.user = user
            covidUser.addressLine1 = addressLine1
            covidUser.addressLine2 = addressLine2
            covidUser.city = city
            covidUser.state = state
            covidUser.zipCode = zipCode
            covidUser.phoneNumber = phoneNumber

            covidUser.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def checkUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter(username = username)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def emailPasswordLink(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data["email"]
        print ( " email = " + email )
        account_activation_token = AccountActivationTokenGenerator()
        users = User.objects.filter(email = email)
        if len(users) > 0:
            send_mail(
                'Reset password ' + str(account_activation_token),
                'Please enter password',
                'mitra.siddhartha@gmail.com',
                [email],
                fail_silently=False,
            )
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"An error occured."}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Password resert link emailed."}), content_type="application/json")

def resetPassword(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]

        users = User.objects.filter(username = username)
        if len(users) > 0:
            user = users[0]
            user.set_password(password)
            user.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"An error occured."}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Password resert link emailed."}), content_type="application/json")

def checkEmail(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data["email"]
        users = User.objects.filter(email = email)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def checkLogin(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        print('username='+str(username)+" password="+str(password))
        userString =""
        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponse(json.dumps({"message":"Invalid"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Invalid"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Valid"}), content_type="application/json")

def logoutUser(request):
    try:

        username = request.POST.get("logoutUser","")
        print('username='+str(username))

        logout(request, user)
        userString=json.dumps({"id":"0","firstName":"","lastName":"","email":""})
        print ( "userString =  " + str(userString))

    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(userString), content_type="application/json")

def listSequences(request):
    sequenceObjList = {}
    sequenceResultObj = {}
    try:
        df = pd.read_csv('data/db_inserts/sequencerecord.csv', index_col=None, na_filter=False)
        print(df.columns)
        sequenceObjList = [
        {"id":row["id"], "accession":row["accession"],
         "organism":row["organism"], "collection_date":row["collection_date"], "country":row["country"], "host":row["host"], "isolation_source":row["isolation_source"], "coded_by":row["coded_by"],
         "protein_id":row["protein_id"],"taxon_id":row["taxon_id"],"isolate":row["isolate"] }
          for index, row in df.iterrows()]

        sequenceResultObj = {"sequenceTableColumns":list(df.columns), "sequenceObjList":sequenceObjList}

    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(sequenceResultObj), content_type='application/json')

def showAlignment(request):
    '''
        Initial data load
        Params: None
        Returns: alignmentResultObj (all sequences + selected sequenceRecord)
    '''
    alignmentObjList = []

    alignmentResultObj = {}

    try:

        # print (" alignment ")

         # get params from request
        data = json.loads(request.body.decode('utf-8'))

        sequenceObjList = []
        selectedSequenceRecords = []

        epitopeObjList = []
        structureObjList = []

        sequenceList = sequences({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "accession":SELECTED_ACCESSIONS})
        epitopes = epitopesequence({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "iedb_id":SELECTED_EPITOPES})
        structureSequenceCoords = [structuresequencecoords ( {"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "pdb_id":SELECTED_PDB_CHAIN_IDS[0]["pdb_id"], "chain":SELECTED_PDB_CHAIN_IDS[0]["chain"]})]
        # structureResidueAtoms = structureresidueatoms({"mesh_id":MESH_ID, "alignment":ALIGNMENT_NAME, "atom":"CA","pdbchains":SELECTED_PDB_CHAIN_IDS})
        sequenceLength = 0
        for sequence in sequenceList:
            sequenceString = sequence["seq"]
            if sequence["offset"] != 0 :
                sequenceString = '-' * sequence["offset"] + sequenceString
            # print ( " len(sequenceString) " + str(len(sequenceString) ) )
            if len(sequenceString) > sequenceLength:
                sequenceLength = len(sequenceString)
            residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
            alignmentObj = {"label":sequence["accession"],"residueObjList":residueObjList}
            sequenceRecords = SequenceRecord.objects.filter(accession = sequence["accession"])
            if len(sequenceRecords) > 0:
                sequenceRecord = sequenceRecords[0]
                sequenceObj = {
                    "taxon":str(sequenceRecord.taxon), "accession":str(sequenceRecord.accession), "organism":sequenceRecord.organism, "collection_date":sequenceRecord.collection_date.strftime("Y-%m-%d"), "country":sequenceRecord.country,
                    "host":sequenceRecord.host, "isolation_source":sequenceRecord.isolation_source, "isolate":sequenceRecord.isolate, "coded_by":sequenceRecord.coded_by
                }
                alignmentObj["sequenceObj"] = sequenceObj
                alignmentObjList.append(alignmentObj)

                alignmentObjList = sorted(alignmentObjList, key=lambda o: sequenceObj["host"])

        epitopeOffsetObjs = []

        for epitope in epitopes:
            print(epitope)
            sequenceString = epitope["seq"]

            epitopeOffsetObjs.append({"iedb_id":str(epitope["iedb_id"]),"offset":epitope["offset"], "percOffset":0})
            # print (epitope.offset)
            if epitope["offset"] != 0 :
                sequenceString = '-' * epitope["offset"] + sequenceString
                if len(sequenceString) < sequenceLength:
                     sequenceString += '-'* ( sequenceLength - len(sequenceString))
            # print (sequenceString)
            residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
            epitopeObj = {"iedb_id":str(epitope["iedb_id"]),"residueObjList":residueObjList}

            epitopeexperimentsfilters = epitopeexperimentsfilter({"alignment":ALIGNMENT_NAME, "mesh_id":MESH_ID, "iedb_id":epitope["iedb_id"]})

            if len(epitopeexperimentsfilters) > 0:
                epitopeExperimentObj = epitopeexperimentsfilters[0]
                epitopeObj["epitopeExperimentObj"] = epitopeExperimentObj
                # print (" adding epitope " + epitope.IEDB_ID)
                epitopeObjList.append(epitopeObj)

        maxEpitopeOffset = max([x["offset"] for x in epitopeOffsetObjs])
        minEpitopeOffset = min([x["offset"] for x in epitopeOffsetObjs])
        rangeEpitopeOffset = maxEpitopeOffset - minEpitopeOffset

        print (" minEpitopeOffset " + str(minEpitopeOffset) + " maxEpitopeOffset " + str(maxEpitopeOffset) + " rangeEpitopeOffset " + str(rangeEpitopeOffset) )

        if rangeEpitopeOffset > 0:
            for index, epitopeObj in enumerate(epitopeObjList):
                # print (" for index " + str(index) + " offset is " + str(epitopeOffsetObjs[index]["offset"]) + " seqeuenceLength " + str(seqeuenceLength) )
                epitopeObj["percOffset"] =  ( (epitopeOffsetObjs[index]["offset"] )/sequenceLength ) * 100
                epitopeObj["offset"] =  epitopeOffsetObjs[index]["offset"]
                # print( epitopeObj["percOffset"] )
        # print (" structureSequenceCoords " + str(structureSequenceCoords))
        for structureSequenceCoord in structureSequenceCoords:
            if structureSequenceCoord["offset"] != 0 :
                sequenceString = '-' * structureSequenceCoord["offset"] + structureSequenceCoord["sequence"]
                # if len(sequenceString) < seqeuenceLength:
                #      sequenceString += '-'* ( seqeuenceLength - len(sequenceString))

            residueObjList = [{"residueValue":'-',"residueColor":RESIDUE_COLOR_MAP['-'], "residuePosition":{"x":0, "y":0, "z":0 }, "residueLabel":"residue_" + str(i), "residueIndex":i} for i,x in enumerate(range(structureSequenceCoord["offset"]) ) ]
            coords = structureSequenceCoord["coords"].split(";")

            # print ( " len structureSequenceCoord[sequence] " + str(len(structureSequenceCoord["sequence"]) ) )
            #
            # print ( " end structureSequenceCoord[sequence] " + str(structureSequenceCoord["sequence"][1401:] )  )
            #
            # print ( " len coords " + str( len(coords) ) )

            for i,x in enumerate(structureSequenceCoord["sequence"]):
                # print (" i " + str(i) + " x "  + str(x))

                if i < len(coords):
                    # print ( " len(coords[i]) " + str ( len ( coords[i].split(",") ) ) )
                    if len(coords[i].split(",")) == 3:
                        coordValues = coords[i].split(",")
                        residueObjList.append(
                            {"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":{"x":coordValues[0], "y":coordValues[1], "z":coordValues[2] }, "residueLabel":"residue_" + str(i), "residueIndex":structureSequenceCoord["offset"]+ i}
                            )
                    else:
                        residueObjList.append(
                            {"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":{"x":0, "y":0, "z":0 }, "residueLabel":"residue_" + str(i), "residueIndex":structureSequenceCoord["offset"]+ i}
                            )
                        # print(residueObjList)
                else:
                        residueObjList.append(
                            {"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":{"x":0, "y":0, "z":0 }, "residueLabel":"residue_" + str(i), "residueIndex":structureSequenceCoord["offset"]+ i}
                            )

            structureObj = {"pdbchain":structureSequenceCoord["pdb_id"]+ "." + structureSequenceCoord["chain"],"residueObjList":residueObjList}
            # print(structureObj)
            # pdbData = structureSequence["pdbchain"].split(".")
            pdb_id, chain  = structureSequenceCoord["pdb_id"] , structureSequenceCoord["chain"]

            structures = Structure.objects.filter (pdb_id = pdb_id)

            if len(structures) > 0:

                structure = structures[0]
                structureChainObj = {"taxon":str(structure.taxon), "pdb_id":str(pdb_id), "chain":str(chain)}

                structureObj["structureChainObj"] = structureChainObj

            # print (" adding epitope " + epitope.IEDB_ID)
            structureObjList.append(structureObj)

        # print (" structureObjList " + str(structureObjList))

        sequenceRecords = sequencerecords({"mesh_id":MESH_ID})
        # print ( " len sequenceList = " + str(len (sequenceList)))
        # sequenceLength = 0
        # for sequence in sequenceList:
        #
        #     sequenceString = sequence["seq"]
        #     if sequence["offset"] != 0 :
        #         sequenceString = '-' * sequence["offset"] + sequenceString
        #     # print ( " len(sequenceString) " + str(len(sequenceString) ) )
        #     if len(sequenceString) > sequenceLength:
        #         sequenceLength = len(sequenceString)
        #     residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
        #     alignmentObj = {"label":sequence["accession"],"residueObjList":residueObjList}
        #     alignmentObjList.append(alignmentObj)

        for sequenceRecord in sequenceRecords:

            if  sequenceRecord["accession"] in  SELECTED_ACCESSIONS:
                sequenceRecord["isSelected"] = True
                selectedSequenceRecords.append(sequenceRecord)

            sequenceObjList.append(sequenceRecord)

        fieldList = ['host', 'organism', 'taxon_id', 'accession', 'country','isolation_source' ]
        
        columnFilterList = []
        columnFilterList = [{"columnName":fieldLabel,"columnFilterValues":list(set([x[fieldLabel] for x in sequenceObjList ] )) } for fieldLabel in fieldList]
        fieldObjList = [{"columnName":x, "rowColor":"#A3E4EE"} if x == "host" else {"columnName":x,"rowColor":"#FFFFFF"} for x in fieldList ]

        sequenceResultObj = {"sequenceTableColumnObjs":fieldObjList, "sequenceObjList":sequenceObjList, "sequenceSortColumn":"host", "columnFilterList":columnFilterList}

        epitopeExperiments = EpitopeExperiment.objects.filter(epitope__alignment__name = ALIGNMENT_NAME, epitope__protein__mesh_id = MESH_ID)

        epitopeExperimentObjList = []

        for x in epitopeExperiments:

            epitopeExperimentObj =      {
                                            'host'              : x.host,
                                            'assay_type'        : x.assay_type,
                                            'assay_result'      : x.assay_result,
                                            'mhc_allele'        : x.mhc_allele,
                                            'mhc_class'         : x.mhc_class,
                                            'exp_method'        : x.exp_method,
                                            'measurement_type'  : x.measurement_type,
                                            'iedb_id'           : x.epitope.IEDB_ID
                                        }

            if  x.epitope.IEDB_ID in  SELECTED_EPITOPES:
                epitopeExperimentObj["isSelected"] = True

            epitopeExperimentObjList.append(epitopeExperimentObj)

        fieldList = ['host', 'assay_type', 'assay_result','mhc_allele','mhc_class','exp_method','measurement_type','iedb_id']
        fieldObjList = [{"columnName":x, "rowColor":"#A3E4EE"} if x == "host" else {"columnName":x, "rowColor":"#FFFFFF"} for x in fieldList ]

        epitopeExperimentResultObj = {"epitopeExperimentTableColumnObjs":fieldObjList, "epitopeExperimentObjList":epitopeExperimentObjList, "epitopeSortColumn":"host"}

        structureChainObjs = structurechains ({"mesh_id": MESH_ID})

        structureChainObjList = []

        for x in structureChainObjs:

            structureChainObj =     {
                                        "taxon": x["taxon"],
                                        "taxon_id": x["taxon_id"],
                                        "pdb_id": x["pdb_id"],
                                        "chain": x["chain"]
                                    }

            if  x["pdb_id"] + "." + x["chain"] in  SELECTED_PDB_CHAIN_IDS:
                structureChainObj["isSelected"] = True
            structureChainObjList.append(structureChainObj)

        fieldList = ["taxon", "pdb_id", "chain"]
        fieldObjList = [{"columnName":x, "rowColor":"#A3E4EE"} if x == "taxon" else {"columnName":x, "rowColor":"#FFFFFF"} for x in fieldList ]

        structureChainResultObj = {"structureChainTableColumnObjs":fieldObjList, "structureChainObjList":structureChainObjList, "structureSortColumn":"taxon"}

        nomenclaturePositionObj = {}

        nomenclature = Nomenclature.objects.get(pk=1)
        nomenclaturePositions = NomenclaturePosition.objects.filter(nomenclature = nomenclature)

        nomenclaturePositionStrings = [str(x.major) + "." + str(x.minor).zfill(3) for x in nomenclaturePositions]

        alignmentResultObj["nomenclaturePositionStrings"] = nomenclaturePositionStrings

        alignmentResultObj["alignmentObjList"] = alignmentObjList
        alignmentResultObj["epitopeObjList"] = epitopeObjList
        alignmentResultObj["structureObjList"] = structureObjList

        alignmentResultObj["epitopeOffsetObjs"] = epitopeOffsetObjs

        alignmentResultObj["selectedAccessions"] = SELECTED_ACCESSIONS.split(",")
        alignmentResultObj["selectedEpitopeIds"] = SELECTED_EPITOPES.split(",")
        alignmentResultObj["selectedStructureIds"] = [x["pdb_id"] + "." + x["chain"] for x in SELECTED_PDB_CHAIN_IDS]

        alignmentResultObj["sequenceResultObj"] = sequenceResultObj
        alignmentResultObj["epitopeExperimentResultObj"] = epitopeExperimentResultObj
        alignmentResultObj["structureChainResultObj"] = structureChainResultObj

    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(alignmentResultObj), content_type='application/json')

def reloadAlignment(request):
    '''
        Reload alignment
        Params: None
        Returns: alignmentResultObj (all sequences + selected sequenceRecord)
    '''
    alignmentObjList = []
    try:

         # get params from request
        data = json.loads(request.body.decode('utf-8'))

        selectedAccessions = data["selectedAccessions"]
        print ( " selectedAccessions " + str((",").join(selectedAccessions)))
        sequenceObjList = []

        sequenceList = sequences({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "accession":(",").join(selectedAccessions)})
        print ( " len sequenceList = " + str(len (sequenceList)))
        sequenceLength = 0
        for sequence in sequenceList:

            sequenceString = sequence["seq"]
            if sequence["offset"] != 0 :
                sequenceString = '-' * sequence["offset"] + sequenceString
            # print ( " len(sequenceString) " + str(len(sequenceString) ) )
            if len(sequenceString) > sequenceLength:
                sequenceLength = len(sequenceString)
            residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
            alignmentObj = {"label":sequence["accession"],"residueObjList":residueObjList}
            alignmentObjList.append(alignmentObj)

        print ( " len alignmentObjList = " + str(len (alignmentObjList)))

    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(alignmentObjList), content_type='application/json')

def reloadEpitopes(request):
    '''
        Reload epitopes
        Params: None
        Returns: epitopeObjList
    '''
    epitopeObjList = []
    try:

         # get params from request
        data = json.loads(request.body.decode('utf-8'))

        selectedEpitopeIds = data["selectedEpitopeIds"]

        epitopes = epitopesequence({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "iedb_id":(",").join(selectedEpitopeIds)})

        # get sequence length
        sequenceList = sequences({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "accession":SELECTED_ACCESSIONS})

        sequenceLength = len(sequenceList[0]["seq"])
        #
        # for epitope in epitopes:
        #
        #     sequenceString = epitope["seq"]
        #
        #     if epitope["offset"] != 0 :
        #         sequenceString = '-' * epitope["offset"] + sequenceString
        #         if len(sequenceString) > sequenceLength:
        #              sequenceString += '-'* ( seqeuenceLength - len(sequenceString))
        #     residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
        #     epitopeObj = {"iedb_id":str(epitope["iedb_id"]),"residueObjList":residueObjList}
        #     epitopeObjList.append(epitopeObj)

        epitopeOffsetObjs = []

        for epitope in epitopes:
            print(epitope)
            sequenceString = epitope["seq"]

            epitopeOffsetObjs.append({"iedb_id":str(epitope["iedb_id"]),"offset":epitope["offset"], "percOffset":0})
            # print (epitope.offset)
            if epitope["offset"] != 0 :
                sequenceString = '-' * epitope["offset"] + sequenceString
                if len(sequenceString) < sequenceLength:
                     sequenceString += '-'* ( sequenceLength - len(sequenceString))
            # print (sequenceString)
            residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
            epitopeObj = {"iedb_id":str(epitope["iedb_id"]),"residueObjList":residueObjList}

            epitopeexperimentsfilters = epitopeexperimentsfilter({"alignment":ALIGNMENT_NAME, "mesh_id":MESH_ID, "iedb_id":epitope["iedb_id"]})

            if len(epitopeexperimentsfilters) > 0:
                epitopeExperimentObj = epitopeexperimentsfilters[0]
                epitopeObj["epitopeExperimentObj"] = epitopeExperimentObj
                # print (" adding epitope " + epitope.IEDB_ID)
                epitopeObjList.append(epitopeObj)

        maxEpitopeOffset = max([x["offset"] for x in epitopeOffsetObjs])
        minEpitopeOffset = min([x["offset"] for x in epitopeOffsetObjs])
        rangeEpitopeOffset = maxEpitopeOffset - minEpitopeOffset

        if rangeEpitopeOffset > 0:
            for index, epitopeObj in enumerate(epitopeObjList):
                # print (" for index " + str(index) + " offset is " + str(epitopeOffsetObjs[index]["offset"]) + " seqeuenceLength " + str(seqeuenceLength) )
                epitopeObj["percOffset"] =  ( (epitopeOffsetObjs[index]["offset"] )/sequenceLength ) * 100
                epitopeObj["offset"] =  epitopeOffsetObjs[index]["offset"]

        print(len(epitopeObjList))
    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(epitopeObjList), content_type='application/json')

def reloadStructures(request):
    '''
        Reload structures
        Params: None
        Returns: structureObjList
    '''
    structureObjList = []
    try:
         # get params from request
        data = json.loads(request.body.decode('utf-8'))

        selectedStructureIds = data["selectedStructureIds"]

        print (" selectedStructureIds " + str(selectedStructureIds))

        structureSequences = structuresequence ( {"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "pdbchains":(",").join(selectedStructureIds)} )
        # try:
        structureResidueAtoms = structureresidueatoms({"mesh_id":MESH_ID, 'alignment':ALIGNMENT_NAME, "atom":'CA', "pdbchains":(",").join(selectedStructureIds)})
        # except:
        #     traceback.print_exc(file=sys.stdout)
        # get sequence length
        sequenceList = sequences({"mesh_id":MESH_ID,"alignment":ALIGNMENT_NAME, "accession":SELECTED_ACCESSIONS})
        sequenceLength = len(sequenceList[0]["seq"])

        aaIndex = 0
        for index, structureSequence in enumerate(structureSequences):
            print ("structureSequence" + str(structureSequence) )
            structureResidueAtomsMap = {}
            sequenceString = structureSequence["sequence"]

            if structureSequence["offset"] != 0 :
                sequenceString = '-' * structureSequence["offset"] + sequenceString
                if len(sequenceString) < sequenceLength:
                     sequenceString += '-'* ( sequenceLength - len(sequenceString))
            # print (sequenceString)
            if len(structureResidueAtoms) > index and structureResidueAtoms[index]["pdb_chain"] == structureSequence["pdbchain"]:
                structureResidueAtomsMap = structureResidueAtoms[index]

                for resIndex, aminoAcid in enumerate(sequenceString):
                    residueLocation = {"x":0, "y":0, "z":0}

                    if aminoAcid != '-':
                        atom = structureResidueAtomsMap["atoms"][aaIndex]
                        residueLocation = {"x":atom["x"], "y":atom["y"], "z":atom["z"]}
                        aaIndex += 1
                    residueObjList.append({"residueValue":aminoAcid,"residueColor":RESIDUE_COLOR_MAP[aminoAcid], "residuePosition":residueLocation, "residueLabel":"residue_" + str(resIndex)})
            # residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]

            structureObj = {"pdbchain":structureSequence["pdbchain"],"residueObjList":residueObjList}
            # print (" adding epitope " + epitope.IEDB_ID)
            structureObjList.append(structureObj)

    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(structureObjList), content_type='application/json')
