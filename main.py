#!/usr/bin/env python
# coding: utf-8

import json
import time
import datetime
import crawler.CAU_Meal_Crawler_toJson as crawler
from google.cloud import firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./crawler/hasikServiceAcountKey.json"

def main():
    cafeteria_data_dic = crawler.getWeekOfMealMenu()
    db = firestore.Client()
    doc_ref = db.collection(u'CAU_Haksik').document('CAU_Cafeteria_Menu')
    print(doc_ref)
    doc_ref.set(cafeteria_data_dic)





