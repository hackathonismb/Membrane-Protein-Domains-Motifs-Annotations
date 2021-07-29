#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.parse
import urllib.request
import json
import pandas

url = 'https://www.uniprot.org/uploadlists/'
GPCR_file = "uniprot-human-allGPCRs.txt"
lymphycyte_file = "uniprot-t-lymphocyte-activation-antigens.txt"


for line in GPCR_file:
    url1="http://www.uniprot.org/uniprot/" 
    

def read_uniprotfile(chk):
    with open(chk, "r") as f:
        uniprot_list1=f.read().splitlines()
        
        str1 = ' '.join(uniprot_list1)
        
    return str1


params = {
'from': 'ACC+ID',
'to': 'PDB_ID',
'format': 'tab',
'query': read_uniprotfile(GPCR_file) #Change to lymphycyte_file
}


data = urllib.parse.urlencode(params)
data = data.encode('utf-8')
req = urllib.request.Request(url,data)

        
with urllib.request.urlopen(req) as f:
   response = f.read()
list1 = response.decode('utf-8')
with open('filename.txt', 'w') as outputfile:
    outputfile.write(str(list1))
    outputfile.close()

    
import pandas as pd
with open('filename.txt','r') as f:
    reader = pandas.read_csv(f, delimiter="\t")   
    reader.columns = ['Uniprot_ID', 'PDB_ID']
    reader['PDB_ID'] = reader['PDB_ID'].str.lower()


    
   # print(reader)
 

def request_data_OPM(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as f:
        response = f.read()
        return response.decode('utf-8')

pdb_ids = pandas.read_csv('opm_database.csv')
import re

r = re.compile(r"(\d+)\(\s*(\d+)-\s*(\d+)\)")

df["segment"] = df["segment"].apply(lambda x: r.findall(x))
df = df.explode("segment")
df[["Domain_type", "start_resid_OPM", "end_resid_OPM"]] = df.pop("segment").apply(pd.Series)
df = df.sort_values(by="Domain_type")
df["Domain_type"] = "TMD" + df["Domain_type"].astype(str)


OPM_list = pd.merge(reader,df,on='PDB_ID')
OPM_list.drop_duplicates(inplace=True)

consensus_json = df.to_json(orient="records")   # df to json
json_obj = json.loads(consensus_json)           # formatting nicely
consensus_json_formatted_str = json.dumps(json_obj, indent=2)
print(consensus_json_formatted_str)

