import os
import requests
from bs4 import BeautifulSoup
from helpers import notify

url = "https://rate.bot.com.tw/gold/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("td")

price = int(result[2].getText().replace("買進",""))

want_buy_price = int(os.getenv("GOLD_BUY",1600))
want_sell_price = int(os.getenv("GOLD_SELL",1700))

content = "\n目前黃金價格: {}元".format(price)

if (price > want_sell_price):
    content += "\n已大於{}元,可以考慮賣出".format(want_sell_price,price)

if (price < want_buy_price):
    content += "\n已低於{}元,可以考慮買進".format(want_buy_price,price)

print(content)
notify.send(content)