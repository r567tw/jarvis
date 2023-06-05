import os
from tracemalloc import start
import requests
from helpers import notify
import time

reports = {"Wx": "天氣現象", "PoP": "降雨機率"}

# todo: use apple shortcut update my current location
# 先寫死台北市
params = {
    "Authorization": os.getenv("WEATHER_TOKEN"),
    "format": "JSON",
    "locationName": "高雄市",
    "sitename": "前金",
}

url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
response = requests.get(url, params)

result = response.json()
# print(result)
content = "\n[{}-{}]\n".format(params["locationName"],params["sitename"])

for element in result["records"]["location"][0]["weatherElement"]:
    if element["elementName"] in reports.keys():
        report = reports[element["elementName"]]

        content += "{}~{} {} {}%".format(
            time.strftime("%H",time.strptime(element["time"][0]["startTime"],"%Y-%m-%d %H:%M:%S")),
            time.strftime("%H",time.strptime(element["time"][0]["endTime"],"%Y-%m-%d %H:%M:%S")),
            report,
            element["time"][0]["parameter"]["parameterName"],
        )

        if element["elementName"] == "PoP":
            content += "%"
        content += "\n"

# 空氣品質
url = "https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON"
response = requests.get(url, params)
result = response.json()

for record in result["records"]:
    if (record["sitename"] == params["sitename"] and record["county"] == params["locationName"]):
        content += "空氣品質: {}".format(record["status"])


notify.send(content)
