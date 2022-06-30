import time
import twstock
from helpers import notify

# 先寫死～
stocks = [
    {'number': '2330',  'ideal': 650}
]

for stock in stocks:
    stockNumber = stock['number']
    
    # 分析 twstock 資料
    data = twstock.Stock(stockNumber)
    decision = twstock.BestFourPoint(data).best_four_point()
    price = twstock.realtime.get(stockNumber) 
    realtime_price = int(float(price['realtime']['latest_trade_price']))
    name = price['info']['name']

    if (decision[0]):
        message = "\n建議買入{} 價格:{}\n 原因：{}".format(stockNumber,realtime_price,decision[1])
    else:
        message = "\n建議賣出{} 價格:{}\n 原因：{}".format(stockNumber,realtime_price,decision[1])
    
    if (realtime_price < stock['ideal']):
        # 低於購買價格，可能不考慮做任何決策
        message = "\n{} 目前:{} 小於理想{}".format(name,realtime_price,stock['ideal'])
    
    notify.send(message)
    # time.sleep(60)

