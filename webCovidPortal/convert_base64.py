import numpy as np
from PIL import Image
import datetime
import base64
import nibabel as nib
import os, sys, traceback
import gzip

REGIONS = {'17':'Left_Hippocampus',
           '53':'Right_Hippocampus',
           '1006':'Left_Enthorinal_Cortex',
           '2006':'Right_Enthorinal_Cortex'}

def convertData():

    try:

        print (" no action ")
    except:
        traceback.print_exc(file=sys.stdout)
    return

convertData()
