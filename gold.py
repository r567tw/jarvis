import requests
from bs4 import BeautifulSoup
from helpers import notify

url = "https://rate.bot.com.tw/gold/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("td")

price = int(result[5].getText().replace("回售", ""))

content = "\n 黃金價格: ${}".format(price)

notify.send(content)