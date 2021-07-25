#!/home/exec/anaconda3/bin/python
import re
import sys
import os
import time
from sys import argv
import xmltodict
import json
import pandas as pd

def export_json():
    pass


#
if len(sys.argv) < 2:
    message='\n Get Hydrophobic Core of TM regions of membrane proteins from the PDBTM.\n\n Usage: ' + sys.argv[0] + ' [4-letter PDBid] \n' + ' Example1: ' + sys.argv[0] + ' 2rh1\n'
    print (message)
    exit()

pdbID=sys.argv[1]
twoLetter=pdbID[1:3]
xmlFile=pdbID+'.xml'
pdbgzFile=pdbID+'.pdb.gz'
pdbFile=pdbID+'.pdb'
wgetcom='wget http://pdbtm.enzim.hu/data/database/'+twoLetter+'/'+xmlFile+' -O '+xmlFile
os.system(wgetcom)
wgetcom2='wget http://pdbtm.enzim.hu/data/database/'+twoLetter+'/'+pdbgzFile+' -O '+pdbgzFile
os.system(wgetcom2)
wgetcom3='gunzip -f '+pdbgzFile
os.system(wgetcom3)

if (os.stat(xmlFile).st_size == 0):
    print("The xml file is empty.\nCheck the PDBid and make sure that it exists in the PDBTM database!\n\n")
    exit()

# test case for debugging
# xmlFile ='2rh1'+'.xml'
# pdbID='2rh1'

# todo: put back later
with open(xmlFile) as fd:
    doc = xmltodict.parse(fd.read())



###
consensus_domains = []
###
mp=doc['pdbtm']['@TMP']
if (mp == 'yes'):
    x=str(doc['pdbtm']['CHAIN'])
    nchains=x.count('CHAINID')
    if (nchains > 1):
        for i in range(nchains):
            chainData=doc['pdbtm']['CHAIN'][i]
            chainid=chainData['@CHAINID']
            helical=chainData['@TYPE']
            if (helical == 'alpha'):
                regionData=chainData['REGION']
                nregions=len(regionData)
                itm=0
                print('\n')
                for j in range(nregions):
                    if (regionData[j]['@type']=='H'):
                        itm=itm+1
                        begTM=regionData[j]['@pdb_beg'] 
                        endTM=regionData[j]['@pdb_end'] 
                        TMstr='TM'+str(itm)

                        consensus_domains.append([pdbID, chainid, TMstr, begTM, endTM]) # appending data to list to be turned into df later
                        # print(pdbID,chainid,TMstr, begTM, endTM)                      # old output
    else:
       chainData=doc['pdbtm']['CHAIN']
       chainid=chainData['@CHAINID']
       helical=chainData['@TYPE']
       if (helical == 'alpha'):
           regionData=chainData['REGION']
           nregions=len(regionData)
           itm=0
           for j in range(nregions):
               if (regionData[j]['@type']=='H'):
                   itm=itm+1
                   begTM=regionData[j]['@pdb_beg']
                   endTM=regionData[j]['@pdb_end']
                   TMstr = 'TM'+str(itm)

                   consensus_domains.append([pdbID, chainid, TMstr, begTM, endTM])
                   # print(pdbID,chainid,TMstr, begTM, endTM)               # old output
else:
    print("This protein is not a membrane protein.\n")
#
print('\n')

df = pd.DataFrame(consensus_domains,            # turning consensus domain list of lists into pd.df
                  columns=['pdbID', 'chainID', 'TMstr', 'begTM', 'endTM'])
consensus_json = df.to_json(orient="records")   # df to json

json_obj = json.loads(consensus_json)           # formatting nicely
consensus_json_formatted_str = json.dumps(json_obj, indent=2)
print(consensus_json_formatted_str)
