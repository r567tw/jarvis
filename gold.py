import requests
from bs4 import BeautifulSoup
import os

url = "https://rate.bot.com.tw/gold/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("td")

price = int(result[2].getText().replace("買進",""))

token = os.getenv("TOKEN")
notify_url = "https://notify-api.line.me/api/notify"

requests.post(
    notify_url,
    headers={'Authorization': "Bearer {}".format(token)},
    data={"message":"\n今日黃金價格: {}元".format(price)}
)