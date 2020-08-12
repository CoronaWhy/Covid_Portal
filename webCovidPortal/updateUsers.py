from __future__ import absolute_import
import numpy as np
from PIL import Image
import datetime
import base64
import os, sys, traceback
from imijPortalApp.models import *

def updateUsers():

    try:

        users = User.objects.all()
        for user in users:
            if user.username.lower().find("imij") != -1:
                covidUsers = CovidUser.objects.filter(user = user)
                if len(covidUsers) == 0:

                    covidUser = CovidUser()

                    covidUser.user = user
                    covidUser.addressLine1 = "addressLine1 test"
                    covidUser.addressLine2 = "addressLine2 test"
                    covidUser.city = "city test"
                    covidUser.state = "NY"
                    covidUser.zipCode = "1234566"
                    covidUser.phoneNumber = "99988877789"

                    covidUser.save()

    except:
        traceback.print_exc(file=sys.stdout)
    return

updateUsers()
