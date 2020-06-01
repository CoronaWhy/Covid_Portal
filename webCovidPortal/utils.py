import pandas as pd
import numpy as np
import os
import sys
import traceback
import math
import seaborn as sns
from collections import OrderedDict
from bokeh.charts import Bar, output_file, show
import matplotlib.pyplot as plt

def createMergedDF(fileName1, fileName2, database, direction):

    '''
    plot results from Limma analysis
    Input:
    Output:
    '''

    geneDBMap = {}

    try:

        print ( " before 1" )
        geneDF1 = getGeneDF(fileName1, database, direction)

        print ( " before 2" )
        geneDF2 = getGeneDF(fileName2, database, direction)

        print ( " before merge" )
        pd.merge(geneDF1, geneDF2, on='gene', how='outer')

        geneDFFinal = geneDF1.merge(geneDF2, on = ["gene","pathway"])

        geneDFFinal = geneDFFinal.rename(columns={"count_x":"count_v1", "count_y":"count_v2"})
        
        #geneSymbolDF = pd.read_table("genelistmapping.txt",sep='\t', index_col=None)
        #geneSymbolDF["entrezID"] = geneSymbolDF["entrezID"].astype(int)        
        #entrezIDList = geneSymbolDF["entrezID"].tolist()
        #geneSymbolList = geneSymbolDF["geneSymbol"].tolist()
        
        #geneDFFinal["geneSymbol"] = [geneSymbolList [ entrezIDList.index(int(x))] for x in geneDFFinal["gene"].tolist()]
        
        geneDFFinal = geneDFFinal.sort(['gene','pathway'], ascending=[True,True])

    except:
        traceback.print_exc(file=sys.stdout)

    return geneDFFinal

def getGeneDF(fileName, database, direction):

    '''
    plot results from Limma analysis
    Input:
    Output:
    '''

    print ( " fileName " + str(fileName) + " database " + str(database) + " direction " + str(direction) )

    geneDBMap = {}

    dfFinal1 = pd.DataFrame()

    try:

        df1 = pd.read_table(fileName,sep='\t', index_col=None)

        df1 = df1[[".id", "module", "Adjusted.Pvalue", "feature", "enrichment_overlap"]]

        df1 = df1.rename(columns={".id":"db", "module":"pathway","Adjusted.Pvalue":"adj_P_Val", "feature":"direction", "enrichment_overlap":"geneset"})

        df1 = df1[(df1["db"] == database) & (df1["direction"] == direction)]

        df1['genes'] = df1['geneset'].str.split("|")

        print ( df1.head())

        for index, row in df1.iterrows():

            for gene in row["genes"]:

                if gene not in geneDBMap:

                    geneDBMap[gene] = {}

                if row["pathway"] not in geneDBMap[gene]:

                    geneDBMap[gene][row['pathway']] = 0

                geneDBMap[gene][row["pathway"]] = np.round(-1 * np.log10(row["adj_P_Val"]), 4)

        geneCountList = []

        tempList = []

        [  [ tempList.append([k1, k2, v2]) for k2, v2 in v1.items()] for k1,v1 in geneDBMap.items() ]

        print ( tempList)

        dfFinal1 =  pd.DataFrame(tempList)

        dfFinal1 = dfFinal1.rename(columns={0:"gene", 1:"pathway",2:"count"})

        #print ( dfFinal1.head() )

    except:
        traceback.print_exc(file=sys.stdout)

    return dfFinal1

#Some prelim. code
## BioCarta_pathways
#temp <- as.data.frame(unifiedRes_lyme_v1[unifiedRes_lyme_v1$.id == "BioCarta_pathways", c("enrichment_overlap")])
#colnames(temp) <- c("entrezids")
#temp <- strsplit(as.character(temp$entrezids), "|", fixed=TRUE)
#temp <- unlist(temp)
#temp_table <- as.data.frame(table(temp))
#temp_table <- temp_table[order(temp_table$Freq, decreasing = TRUE),]
## All Pathways
#temp <- as.data.frame(unifiedRes_lyme_v1[ , c("enrichment_overlap")])
#colnames(temp) <- c("entrezids")
#temp <- strsplit(as.character(temp$entrezids), "|", fixed=TRUE)
#temp <- unlist(temp)
#temp_table <- as.data.frame(table(temp))
#temp_table <- temp_table[order(temp_table$Freq, decreasing = TRUE),]
## Need to make unique gene list per pathway? per database?
## ....
