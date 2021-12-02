import twstock
import requests
from bs4 import BeautifulSoup
import os

# stock = twstock.Stock('2330')
# decision = twstock.BestFourPoint(stock).best_four_point()
# print(decision)

url = "https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("td")

# - 去分析裡面的日期
# https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule