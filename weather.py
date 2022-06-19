import os
from tracemalloc import start
import requests
from helpers import notify
import time

reports = {
    # "Wx" : "天氣現象",
    "PoP": "降雨機率"
}

# todo: use apple shortcut update my current location
# 先寫死台北市
params = {
    'Authorization': 'CWB-8617C293-566E-4A6E-BDBB-59443A4134C1',
    'format': 'JSON',
    'locationName': "臺北市"
}
url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
response = requests.get(url,params)

result = response.json()

content = "\n"
# print(result['records']['location'][0]['weatherElement'])

for element in result['records']['location'][0]['weatherElement']:
    if (element['elementName'] in reports.keys()):
        # print(reports[element['elementName']])
        report = reports[element['elementName']]
        # for timeElement in element['time']:
        #     content += "{}-{} {}為 {}\n".format(
        #         time.strftime("%m/%d %H:%M",time.strptime(timeElement['startTime'],"%Y-%m-%d %H:%M:%S")),
        #         time.strftime("%m/%d %H:%M",time.strptime(timeElement['endTime'],"%Y-%m-%d %H:%M:%S")),
        #         report,
        #         timeElement['parameter']['parameterName']
        #     )
        # content += "\n"

        content += "{}~{} {} {}%".format(
            time.strftime("%H",time.strptime(element['time'][0]['startTime'],"%Y-%m-%d %H:%M:%S")),
            time.strftime("%H",time.strptime(element['time'][0]['endTime'],"%Y-%m-%d %H:%M:%S")),
            report,
            element['time'][0]['parameter']['parameterName']
        )
        
# print(content)

notify.send(content)