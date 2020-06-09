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
from covidPortalApp.models import *
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

def showAlignment(request):
    alignment = {}
    alignmentObjList = []
    try:

        print (" alignment ")

        residueColorMap = {
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
            }

        alignmentMap = {
                 "first": "--------MFVFLVLLP--------------LVSSQCVNLT---------TRTQ-------LPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFH--AIHVSGTNG-------------TKRFDNPVLPFNDGVYFASTEKSNI-------------------IRGWIFGTTLDSKTQSLLI--VN--------------------NATNVVIKVCE---------FQFCNDPFLGVYYHKN-NKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGN-F--KNLREFVFKNIDGYFKIYSKHTPINLV----RDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTP----GDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRF-PNITN-LCPFGEVF--NATRFASVYAWNRKRISNCVADYSVLYNS-ASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKV---------------------------GGNYNYLYRLFRKSNLKPFERDISTEIYQ-------------------AGSTPCNGVEGFNCYF---------------------------PLQSY--------------------------GFQ-----------------------------------P-----TNGVGYQPYRVVVLSFELLHAPATVCGPK-K-----STNLVKNKCVNFNFNGLTGTGVLTE-SNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYST-----GSNVFQTRAGCLIGAEHVNN----SYECDIPIGAGICASYQTQTNSPRRA-RSVA-----SQSIIAYTMSLG-AENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIY--KTPPIK----DFGGFNFSQILPDPS-----------KPSKRSFIEDLLFNKVTLADAGFIKQYGDCLG---DIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHD---GKAHFPREGVFVSNGT----------",
                 "second": "MKIL---IFAFLANLAK---------------AQEGCGIIS---------RKPQ-------PKMAQVSSSRRGVYYNDDIFRSDVLHLTQDYFLPFDSNLTQYF--SLNVD-SDR-------------YTYFDNPILDFGDGVYFAATEKSNV-------------------IRGWIFGSSFDNTTQSAVI--VN--------------------NSTHIIIRVCN---------FNLCKEPMYTVSRG---TQ----QNAWVYQSAFNCTYDRVEKSFQLDTTP-KTGNF--KDLREYVFKNRDGFLSVYQTYTAVNLP----RGLPTGFSVLKPILKLPFGINITSYRVVMAMFSQ----------TTSNFLPESAAYYVGNLKYSTFMLRFNENGTITDAVDCSQNPLAELKCTIKNFNVDKGIYQTSNFRVSPTQEVIRF-PNITN-RCPFDKVF--NATRFPNVYAWERTKISDCVADYTVLYNS-TSFSTFKCYGVSPSKLIDLCFTSVYADTFLIRSSEVRQVAPGETGVIADYNYKLPDDFTGCVIAWNTAKHDT--------------------------------GNYYYRSHRKTKLKPFERDLSSDD--------------------------------GNGVY---------------------------TLSTY--------------------------DFN-----------------------------------P-----NVPVAYQATRVVVLSFELLNAPATVCGPK-L-----STELVKNQCVNFNFNGLKGTGVLTS-SSKRFQSFQQFGRDTSDFTDSVRDPQTLEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVPTAIRADQLTPAWRVYST-----GVNVFQTQAGCLIGAEHVNA----SYECDIPIGAGICASYHTASV----L-RSTG-----QKSIVAYTMSLG-AENSIAYANNSIAIPTNFSISVTTEVMPVSMAKTAVDCTMYICGDSLECSNLLLQYGSFCTQLNRALTGIAIEQDKNTQEVFAQVKQMY--KTPAIK----DFGGFNFSQILPDPS-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGDCLG---DVSARDLICAQKFNGLTVLPPLLTDDMVAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQESLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPSQEKNFTTAPAICHE---GKAYFPREGVFVSNGT----------",
                 'third': "----MFIFLLFLTLTSG--------------SDLDRCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFGNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFSP----------AQDIWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVRF-PNITN-LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFELLNAPATVCGPK-L-----STDLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHTVSL----L-RSTS-----QKSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGECLG---DINARDLICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------",
                 "first1": "--------MFVFLVLLP--------------LVSSQCVNLT---------TRTQ-------LPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFH--AIHVSGTNG-------------TKRFDNPVLPFNDGVYFASTEKSNI-------------------IRGWIFGTTLDSKTQSLLI--VN--------------------NATNVVIKVCE---------FQFCNDPFLGVYYHKN-NKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGN-F--KNLREFVFKNIDGYFKIYSKHTPINLV----RDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTP----GDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRF-PNITN-LCPFGEVF--NATRFASVYAWNRKRISNCVADYSVLYNS-ASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKV---------------------------GGNYNYLYRLFRKSNLKPFERDISTEIYQ-------------------AGSTPCNGVEGFNCYF---------------------------PLQSY--------------------------GFQ-----------------------------------P-----TNGVGYQPYRVVVLSFELLHAPATVCGPK-K-----STNLVKNKCVNFNFNGLTGTGVLTE-SNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYST-----GSNVFQTRAGCLIGAEHVNN----SYECDIPIGAGICASYQTQTNSPRRA-RSVA-----SQSIIAYTMSLG-AENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIY--KTPPIK----DFGGFNFSQILPDPS-----------KPSKRSFIEDLLFNKVTLADAGFIKQYGDCLG---DIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHD---GKAHFPREGVFVSNGT----------",
                 "second1": "MKIL---IFAFLANLAK---------------AQEGCGIIS---------RKPQ-------PKMAQVSSSRRGVYYNDDIFRSDVLHLTQDYFLPFDSNLTQYF--SLNVD-SDR-------------YTYFDNPILDFGDGVYFAATEKSNV-------------------IRGWIFGSSFDNTTQSAVI--VN--------------------NSTHIIIRVCN---------FNLCKEPMYTVSRG---TQ----QNAWVYQSAFNCTYDRVEKSFQLDTTP-KTGNF--KDLREYVFKNRDGFLSVYQTYTAVNLP----RGLPTGFSVLKPILKLPFGINITSYRVVMAMFSQ----------TTSNFLPESAAYYVGNLKYSTFMLRFNENGTITDAVDCSQNPLAELKCTIKNFNVDKGIYQTSNFRVSPTQEVIRF-PNITN-RCPFDKVF--NATRFPNVYAWERTKISDCVADYTVLYNS-TSFSTFKCYGVSPSKLIDLCFTSVYADTFLIRSSEVRQVAPGETGVIADYNYKLPDDFTGCVIAWNTAKHDT--------------------------------GNYYYRSHRKTKLKPFERDLSSDD--------------------------------GNGVY---------------------------TLSTY--------------------------DFN-----------------------------------P-----NVPVAYQATRVVVLSFELLNAPATVCGPK-L-----STELVKNQCVNFNFNGLKGTGVLTS-SSKRFQSFQQFGRDTSDFTDSVRDPQTLEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVPTAIRADQLTPAWRVYST-----GVNVFQTQAGCLIGAEHVNA----SYECDIPIGAGICASYHTASV----L-RSTG-----QKSIVAYTMSLG-AENSIAYANNSIAIPTNFSISVTTEVMPVSMAKTAVDCTMYICGDSLECSNLLLQYGSFCTQLNRALTGIAIEQDKNTQEVFAQVKQMY--KTPAIK----DFGGFNFSQILPDPS-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGDCLG---DVSARDLICAQKFNGLTVLPPLLTDDMVAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQESLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPSQEKNFTTAPAICHE---GKAYFPREGVFVSNGT----------",
                 'third1': "----MFIFLLFLTLTSG--------------SDLDRCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFGNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFSP----------AQDIWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVRF-PNITN-LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFELLNAPATVCGPK-L-----STDLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHTVSL----L-RSTS-----QKSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGECLG---DINARDLICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------",
                 "first2": "--------MFVFLVLLP--------------LVSSQCVNLT---------TRTQ-------LPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFH--AIHVSGTNG-------------TKRFDNPVLPFNDGVYFASTEKSNI-------------------IRGWIFGTTLDSKTQSLLI--VN--------------------NATNVVIKVCE---------FQFCNDPFLGVYYHKN-NKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGN-F--KNLREFVFKNIDGYFKIYSKHTPINLV----RDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTP----GDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRF-PNITN-LCPFGEVF--NATRFASVYAWNRKRISNCVADYSVLYNS-ASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKV---------------------------GGNYNYLYRLFRKSNLKPFERDISTEIYQ-------------------AGSTPCNGVEGFNCYF---------------------------PLQSY--------------------------GFQ-----------------------------------P-----TNGVGYQPYRVVVLSFELLHAPATVCGPK-K-----STNLVKNKCVNFNFNGLTGTGVLTE-SNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYST-----GSNVFQTRAGCLIGAEHVNN----SYECDIPIGAGICASYQTQTNSPRRA-RSVA-----SQSIIAYTMSLG-AENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIY--KTPPIK----DFGGFNFSQILPDPS-----------KPSKRSFIEDLLFNKVTLADAGFIKQYGDCLG---DIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHD---GKAHFPREGVFVSNGT----------",
                 "second2": "MKIL---IFAFLANLAK---------------AQEGCGIIS---------RKPQ-------PKMAQVSSSRRGVYYNDDIFRSDVLHLTQDYFLPFDSNLTQYF--SLNVD-SDR-------------YTYFDNPILDFGDGVYFAATEKSNV-------------------IRGWIFGSSFDNTTQSAVI--VN--------------------NSTHIIIRVCN---------FNLCKEPMYTVSRG---TQ----QNAWVYQSAFNCTYDRVEKSFQLDTTP-KTGNF--KDLREYVFKNRDGFLSVYQTYTAVNLP----RGLPTGFSVLKPILKLPFGINITSYRVVMAMFSQ----------TTSNFLPESAAYYVGNLKYSTFMLRFNENGTITDAVDCSQNPLAELKCTIKNFNVDKGIYQTSNFRVSPTQEVIRF-PNITN-RCPFDKVF--NATRFPNVYAWERTKISDCVADYTVLYNS-TSFSTFKCYGVSPSKLIDLCFTSVYADTFLIRSSEVRQVAPGETGVIADYNYKLPDDFTGCVIAWNTAKHDT--------------------------------GNYYYRSHRKTKLKPFERDLSSDD--------------------------------GNGVY---------------------------TLSTY--------------------------DFN-----------------------------------P-----NVPVAYQATRVVVLSFELLNAPATVCGPK-L-----STELVKNQCVNFNFNGLKGTGVLTS-SSKRFQSFQQFGRDTSDFTDSVRDPQTLEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVPTAIRADQLTPAWRVYST-----GVNVFQTQAGCLIGAEHVNA----SYECDIPIGAGICASYHTASV----L-RSTG-----QKSIVAYTMSLG-AENSIAYANNSIAIPTNFSISVTTEVMPVSMAKTAVDCTMYICGDSLECSNLLLQYGSFCTQLNRALTGIAIEQDKNTQEVFAQVKQMY--KTPAIK----DFGGFNFSQILPDPS-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGDCLG---DVSARDLICAQKFNGLTVLPPLLTDDMVAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQESLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPSQEKNFTTAPAICHE---GKAYFPREGVFVSNGT----------",
                 'third2': "----MFIFLLFLTLTSG--------------SDLDRCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFGNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFSP----------AQDIWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVRF-PNITN-LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFELLNAPATVCGPK-L-----STDLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHTVSL----L-RSTS-----QKSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGECLG---DINARDLICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------",

                }

        for k,v in alignmentMap.items():
            residueObjList = [{"residueValue":x,"residueColor":residueColorMap[x], "residuePosition":i} for i,x in enumerate(v)]
            alignmentObj = {"label":k,"residueObjList":residueObjList}
            alignmentObjList.append(alignmentObj)
            print (alignmentObjList)

    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(alignmentObjList), content_type='application/json')
