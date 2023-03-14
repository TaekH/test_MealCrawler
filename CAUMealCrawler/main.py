#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json
import time
import datetime
import crawler.CAU_Meal_Crawler_toJson as crawler
from google.cloud import firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./crawler/hasikServiceAcountKey.json"

def main(request):
    crawler.getWeekOfMealMenu()
    with open('./CAU_Cafeteria_Menu.json', 'r') as f:
        cafeteria_data_dic = json.load(f)
    db = firestore.Client()
    doc_ref = db.collection(u'CAU_Haksik').document('CAU_Cafeteria_Menu')
    doc_ref.set(cafeteria_data_dic)


# In[ ]:




