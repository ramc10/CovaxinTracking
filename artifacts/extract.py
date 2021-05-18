import os
import requests
import json
import datetime
import csv

date = datetime.datetime.now()

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=589&date=07-05-2021,08-05-2021,09-05-2021,10-05-2021,11-05-2021,12-05-2021,13-05-2021,14-05-2021'
headers = {'accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

resp = requests.get(url=url, headers=headers)
data = resp.json() # Check the JSON Response Content documentation below
result = eval(json.dumps(data))

f = open('output.csv', 'w')
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
