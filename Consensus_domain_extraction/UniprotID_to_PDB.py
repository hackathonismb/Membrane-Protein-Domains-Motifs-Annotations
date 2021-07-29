#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Read Uniprot IDS and convert to PDB
import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'
GPCR_file = "uniprot-human-allGPCRs.txt"
lymphycyte_file = "uniprot-t-lymphocyte-activation-antigens.txt"


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
dict2 = {}
dict2 = response.decode('utf-8')
print(dict2)

