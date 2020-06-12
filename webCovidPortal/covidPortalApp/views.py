from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings

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
from covidPortalApp.covidPortalAppObjs import *
from covidPortalApp.covidPortalAppConstants import *
from django.contrib.auth import authenticate
import time
import paramiko

from conf import *
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

# def fetchSelectedSequences(request):
#     '''
#         Params: selectedAccessions - list of accession ids to get sequences for
#         Returns: selectedSequenceObjs
#     '''
#
#     alignmentResultObj = {}
#
#     try:
#         # get params from request
#         data = json.loads(request.body.decode('utf-8'))
#         selectedaccessions = data["selectedaccessions"]
#
#         selectedSequenceRecords =  SequenceRecord.objects.filter(accession__in = selectedaccessions)
#
#         sequenceObjList = [
#         {"id":row.id, "accession":row.accession,
#          "organism":row.organism, "collection_date":row.collection_date.strftime('%M/%D/%Y'), "country":row.country, "host":row.host, "isolation_source":row.isolation_source, "coded_by":row.coded_by,
#          "protein_id":row.protein_id,"taxon_id":row.taxon_id,"isolate":row.isolate }
#           if row.collection_date else
#         {"id":row.id, "accession":row.accession,
#          "organism":row.organism, "collection_date":'', "country":row.country, "host":row.host, "isolation_source":row.isolation_source, "coded_by":row.coded_by,
#          "protein_id":row.protein_id,"taxon_id":row.taxon_id,"isolate":row.isolate }
#          for row in selectedSequenceRecords
#           ]
#
#         alignment = Alignment.objects.get (pk = 1)
#
#         sequences = list(Sequence.objects.filter(sequence_record__in = selectedSequenceRecords, alignment = alignment) )
#
#         # build list of alighment objs
#         alignmentObjList = []
#         for sequence in sequences:
#
#             sequenceString = sequence.sequence
#             if sequence.offset != 0 :
#                 sequenceString = '-' * sequence.offset + sequenceString
#
#             residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
#             alignmentObj = {"label":sequence.sequence_record.accession,"residueObjList":residueObjList}
#             alignmentObjList.append(alignmentObj)
#
#         fieldList = [str(x) for x in SequenceRecord._meta.fields]
#
#         sequenceResultObj = {"sequenceTableColumns":fieldList, "sequenceObjList":sequenceObjList}
#
#         nomenclature = Nomenclature.objects.filter(accession__in = selectedAccessions, alignment = alignment)
#
#         alignmentResultObj["alignmentObjList"] = alignmentObjList
#         alignmentResultObj["sequenceResultObj"] = sequenceResultObj
#         alignmentResultObj["selectedAccessions"] = selectedAccessions
#         alignmentResultObj["nomenclature"] = nomenclature
#
#
#         print (sequenceResultObj)
#
#     except:
#         traceback.print_exc(file=sys.stdout)
#
#     return HttpResponse(json.dumps(alignmentResultObj), content_type='application/json')

def showAlignment(request):
    '''
        Params: None
        Returns: alignmentResultObj (all sequences + selected sequenceRecord)
    '''
    alignmentObjList = []

    alignmentResultObj = {}

    try:

        print (" alignment ")

         # get params from request
        data = json.loads(request.body.decode('utf-8'))

        # initialAlignment = data["initialAlignment"]
        # print (" data " + str(data))

        selectedAccessions = data["selectedAccessions"]

        print (" selectedAccessions " + str(selectedAccessions))
        initialAlignment = data["initialAlignment"]

        sequenceObjList = []
        selectedSequenceRecords = []

        if initialAlignment:
            selectedAccessions = SELECTED_ACCESSIONS

            sequenceRecords = SequenceRecord.objects.all()

            for row in sequenceRecords:

                sequenceObjMap = {
                                    "id":row.id, "accession":row.accession, "organism":row.organism, "collection_date":"", "country":row.country,
                                    "host":row.host, "isolation_source":row.isolation_source, "coded_by":row.coded_by, "protein_id":row.protein_id,"taxon_id":row.taxon_id,"isolate":row.isolate , "isSelected" : False
                                    }
                if row.collection_date:
                    sequenceObjMap["collection_date"] = row.collection_date.strftime('%M/%D/%Y')

                if  row.accession in  SELECTED_ACCESSIONS:
                    print ( " ******** SELECTED_ACCESSIONS " + row.accession)
                    sequenceObjMap["isSelected"] = True
                    selectedSequenceRecords.append(row)

                sequenceObjList.append(sequenceObjMap)

        else:

            selectedSequenceRecords = SequenceRecord.objects.filter ( accession__in = selectedAccessions)

        alignment = Alignment.objects.get (pk = 1)
        sequences = list(Sequence.objects.filter(sequence_record__in = selectedSequenceRecords, alignment = alignment) )

        for sequence in sequences:

            sequenceString = sequence.sequence
            if sequence.offset != 0 :
                sequenceString = '-' * sequence.offset + sequenceString

            residueObjList = [{"residueValue":x,"residueColor":RESIDUE_COLOR_MAP[x], "residuePosition":i} for i,x in enumerate(sequenceString)]
            alignmentObj = {"label":sequence.sequence_record.accession,"residueObjList":residueObjList}
            alignmentObjList.append(alignmentObj)

        fieldList = [str(x) for x in SequenceRecord._meta.fields]

        sequenceResultObj = {"sequenceTableColumns":fieldList, "sequenceObjList":sequenceObjList}

        nomenclaturePositionObj = {}

        if initialAlignment:

            nomenclature = Nomenclature.objects.get(pk=1)
            nomenclaturePositions = NomenclaturePosition.objects.filter(nomenclature = nomenclature)

            nomenclaturePositionMajor0s = [str(x.major)[0] for x in nomenclaturePositions]
            nomenclaturePositionMajor1s = [str(x.major)[1] if len(str(x.major)) > 1 else '' for x in nomenclaturePositions]
            nomenclaturePositionMajor2s = [str(x.major)[2] if len(str(x.major)) > 2 else '' for x in nomenclaturePositions]
            nomenclaturePositionMinor0s = [str(x.minor)[0] for x in nomenclaturePositions]

            nomenclaturePositionObj = {"nomenclaturePositionMajor0s":nomenclaturePositionMajor0s, "nomenclaturePositionMajor1s":nomenclaturePositionMajor1s, "nomenclaturePositionMajor2s":nomenclaturePositionMajor2s}

        alignmentResultObj["alignmentObjList"] = alignmentObjList
        alignmentResultObj["sequenceResultObj"] = sequenceResultObj
        alignmentResultObj["selectedAccessions"] = selectedAccessions
        alignmentResultObj["nomenclaturePositionObj"] = nomenclaturePositionObj
        # print (sequenceResultObj)

    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(alignmentResultObj), content_type='application/json')
