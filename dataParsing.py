import requests
import json
import sqlite3
import time

#searching the api key of velib
key_file = open('api.key','r')
api_key = key_file.readline().rstrip('\n')
key_file.close()

url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Paris&apiKey=' + api_key

print(url)

response = requests.get(url)

print(response.status_code)

data = response.json()

conn = sqlite3.connect('velib.db')
cursor = conn.cursor()

keep = 0
request_date = int(time.time())

for station in data:

    banking = 0
    bonus = 0
    number = int(station['number'])
    contract_name = station['contract_name']
    name = station['name']
    address = station['address']
    position_lat = float(station['position']['lat'])
    position_lng = float(station['position']['lng'])
    if(station['banking'] == 'true'):
        banking = 1
    if(station['bonus'] == 'true'):
        bonus = 1
    status = station['status']
    bike_stands = int(station['bike_stands'])
    available_bike_stands = int(station['available_bike_stands'])
    available_bikes = int(station['available_bikes'])
    last_update = int(station['last_update'])

    cursor.execute("""
    INSERT INTO stats(request_date, number,contract_name,name,address,position_lat,position_lng,banking,bonus,status,bike_stands,available_bike_stands,available_bikes,last_update)
     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (request_date,number,contract_name,name,address,position_lat,position_lng,banking,bonus,status,bike_stands,available_bike_stands,available_bikes,last_update))

    conn.commit()
