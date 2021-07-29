#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.parse
import urllib.request

url1 = 'https://lomize-group-opm.herokuapp.com/pdbids'
url3 = 'https://lomize-group-opm.herokuapp.com/assemblies'

def request_data_OPM(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as f:
        response = f.read()
        dict1 = {}
        dict1 = response.decode('utf-8')
        print(dict1)


print("Printing all PDB IDs present in OPM database in JSON format") 
request_data_OPM(url1)
print("Printing all assembly details for all PDBIDs present in OPM database in JSON format") 
request_data_OPM(url3)


# In[ ]:




