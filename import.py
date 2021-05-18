#!/usr/bin/env python

import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

#CSV to JSON Conversion
csvfile = open('/home/covid/COVID/history.csv', 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient('localhost', 27017) 
db=mongo_client.covid
db.segment.drop()
header= ["Timestamp","Area","Place","Date","Vaccine","Available"]

for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.VaccinationCenters.insert(row)
