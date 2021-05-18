#!/usr/bin/env python

import os
import requests
import json
import datetime
import csv

date = datetime.datetime.now()

def alerting(place,date,count):
    from twilio.rest import Client 
    account_sid = 'ACe2b7ce8b38bac23053d91884452aab4c' 
    auth_token = 'bcf645f3460e45bd89a5190d44832de9' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(  
                              messaging_service_sid='MG04c1caa9c20486bdfb6362f885c55f33', 
                              body = count + ' COVAXIN AVALIABLE ON '+ date + ' at ' + place,      
                              to='+919944402533' 
                          ) 

def importing():
    import pandas as pd
    import sys, getopt, pprint
    from pymongo import MongoClient

    #CSV to JSON Conversion
    csvfile = open('/home/covid/COVID/output.csv', 'r')
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

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=589&date=17-05-2021,18-05-2021,19-05-2021,20-05-2021,11-05-2021,12-05-2021,13-05-2021,14-05-2021,15-05-2021,16-05-2021'
headers = {'accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

resp = requests.get(url=url, headers=headers)
data = resp.json() # Check the JSON Response Content documentation below
result = eval(json.dumps(data))

f = open('/home/covid/COVID/output.csv', 'w')
with f:
    fnames = ['Timestamp', 'Area','Place','Date','Vaccine','Available']
    writer = csv.DictWriter(f, fieldnames=fnames)  
    writer.writeheader()
    for data in result['centers']:
        for doc in data['sessions']:
            print('Area: '+ data['block_name'])
            print('Date: ' + doc['date'])
            print('Vaccine: ' + doc['vaccine'])
            print('Available: ' + str(doc['available_capacity']))
            
            writer.writerow({'Timestamp' : date, 'Area': data['block_name'], 'Place': data['name'], 'Date': doc['date'], 'Vaccine': doc['vaccine'], 'Available': doc['available_capacity']})

csv_file = csv.reader(open('/home/covid/COVID/output.csv', "r"), delimiter=",")

for row in csv_file:
    if row[4] == 'COVAXIN':
         print (row)
         count = int(row[5])
         if count == 0:
             print 'Unavailable'
         else:
            print 'Vaccine Avaliable'
            place = row[2]
            date = row[3]
            count = row[5]

            alerting(place,date,count)


from subprocess import call
rc = call("/home/covid/COVID/backup.sh")

importing()
