# built-ins
import json
import re

# external dependencies
from bs4 import BeautifulSoup
import requests

def get_eotb_stations() -> tuple[dict[str,str], list[str]]:
    #These stations provide monthly readings
    station_locations = {}
    response = requests.get('https://eyesonthebay.dnr.maryland.gov/bay_cond/bay_cond.cfm')
    soup = BeautifulSoup(response.text, 'html.parser')
    station_options: list[str] = soup.find_all('table')[0].select('option')
    for option in station_options:
        match = re.search('>(.+)</', str(option))
        temp = match.group(1).split(' - ')
        station_locations[temp[0]]=temp[1] #{Station code: Station location}
    station_ids = [x.replace(".", "") for x in station_locations.keys()]
    return station_locations, station_ids

def eotb_stations_to_json(stations: list[str]) -> str:
    jsondata = {}
    parameters = ['bdo', 'wt', 'sec', 'sal', 'ph']
    for station in stations:
        jsondata[station] = {} #dict[str, dict[str, dict[str, dict[str, str]]]]
        #jsondata[station_id][parameter][month][data_title] = data
        for parameter in parameters:
            payload: dict[str,str] = {'station':station,'param':parameter}
            response = requests.get("https://eyesonthebay.dnr.maryland.gov/bay_cond/bay_cond.cfm", params=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            souparray: list[str] = str(soup.find_all('table')[3].prettify()).split('\n')
            raw_data: list[str] = [data.strip() for data in souparray if "<" not in data]
            data_titles: list[str] = raw_data[3:8]
            #range explained: 9 = first data position. 80 = offset to start of data(8)+number of months(12)*len(titles)(6)
            temp = {raw_data[i-1]:{data_titles[x]:raw_data[i+x] for x in range(len(data_titles))} for i in range(9,80,6)}
            jsondata[station].setdefault(parameter, {}).update(temp)
    json_output = json.dumps(jsondata, indent=4)
    return json_output
