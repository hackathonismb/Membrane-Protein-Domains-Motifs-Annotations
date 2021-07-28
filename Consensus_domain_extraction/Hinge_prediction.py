#!/usr/bin/env python
# coding: utf-8

# In[1]:


from packman import molecule
from packman.apps import predict_hinge


# In[2]:


mol=molecule.load_structure('2rh1.pdb')


# In[3]:


mol


# In[4]:


#If the backbone atoms of the ALL chains needs to be studied,
backbone=[]
for i in [i.get_id() for i in mol[0].get_chains()]:
        backbone.extend( [k for j in mol[0][i].get_backbone() for k in j if k is not None] )


# In[ ]:


predict_hinge(backbone, Alpha=2.8, outputfile=open('output.txt', 'w'))


# In[ ]:





# In[ ]:





# In[ ]:




