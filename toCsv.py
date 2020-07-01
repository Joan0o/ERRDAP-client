import json
import csv
import os
import math

days = 1
num_files = 1

headers = ["time", "latitude", "longitude", "direction", "speed"]
rows = []

for num in range(1, days + 1):
    with open('data/dia_'+str(num)+'.json') as json_file:
        data = json.load(json_file)
    [rows.append(row) for row in data['table']['rows']]

num_rows = int(len(rows)/num_files)

for file_num in range(1, num_files + 1):

    data_file = open('data csv/data_file_'+str(file_num)+'.csv', 'w')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(headers)
    
    for row in rows[(file_num - 1)*num_rows:(file_num)*num_rows]:
        
        time = row[0].replace("T12:00:00Z", "")
        latitude = row[1]
        longitude = row[2]
        u = row[3]
        v = row[4]

        row_treated = []
        row_treated.append(time)
        row_treated.append(latitude)

        # longitude
        if(longitude % 360 < 180):
            row_treated.append(longitude % 360)
        else:
            row_treated.append(((longitude-180) % 360)-180)

        # wind_direction
        row_treated.append(math.degrees(math.atan2(u,v)))

        # wind_speed
        row_treated.append((u*u+v*v)**1/2)
        csv_writer.writerow(row_treated)

    data_file.close()
