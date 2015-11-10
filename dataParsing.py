import requests
import json
import sqlite3
import time

#searching the api key of velib
key_file = open('jcdecaux.key','r')
api_key = key_file.readline().rstrip('\n')
key_file.close()


startime = time.time()

url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Paris&apiKey=' + api_key

response = requests.get(url)

print(response.status_code)

data = response.json()

conn = sqlite3.connect('velib.db')
cursor = conn.cursor()

keep = 0
request_date = int(time.time())

for station in data:

    number = int(station['number'])
    status = station['status']
    bike_stands = int(station['bike_stands'])
    available_bike_stands = int(station['available_bike_stands'])
    available_bikes = int(station['available_bikes'])
    last_update = int(station['last_update'])

    cursor.execute("""
    INSERT INTO statistics(number,request_date,status,bike_stands,available_bike_stands,available_bikes,last_update)
     VALUES(?, ?, ?, ?, ?, ?, ?)""", (number,request_date,status,bike_stands,available_bike_stands,available_bikes,last_update))

    conn.commit()

endtime = time.time()

print(int(endtime - startime))
conn.close()
