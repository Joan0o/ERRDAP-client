import requests as rq
import json
import os
from datetime import timedelta, date

path = os.getcwd() + "/data"

if os.path.isfile(path):
    os.mkdir(path)

# falta T12:00:00Z"
start_date = date(2015,1,1)
end_date = date(2016,1,1)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def getUrl(date):
    date = date + "T12:00:00Z"
    host = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/NCEP_Global_Best.json?"
    params = "ugrd10m%5B("+date+")%5D%5B(-7.0):(15.5)%5D%5B(276.0):(298.5)%5D,vgrd10m%5B("+date+")%5D%5B(-7.0):(15.5)%5D%5B(276.0):(298.5)%5D"
    other_params = "&.draw=vectors&.vars=longitude%7Clatitude%7Cugrd10m%7Cvgrd10m&.color=0x000000&.bgColor=0xffccccff"
    return host + params + other_params

URL_list = []


if end_date == start_date:
    URL_list.append(getUrl(end_date.strftime("%Y-%m-%d")))
else:
    [URL_list.append(getUrl(single_date.strftime("%Y-%m-%d"))) for single_date in daterange(start_date, end_date)]
        
for num, URL in enumerate(URL_list, start=1):
    try:
        r = rq.get(URL)  # Make an API call to URL to retrieve data
        response = r.json()  # Store the json-encoded content in the retrieved data
        
        with open('dia_'+str(num)+'.json', 'w') as outfile:
            json.dump(response, outfile)
    except:
        print(URL)
        continue
    