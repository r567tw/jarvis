import time
import twstock
from helpers import notify

# 先寫死～
stocks = [
    {'number': '2330',  'ideal': 600, 'decision': False},
    {'number': '0056',  'ideal': 30, 'decision': True},
    {'number': '2891',  'ideal': 25, 'decision': True}
]

# 更新台灣的Code表
twstock.__update_codes()

for stock in stocks:
    stockNumber = stock['number']

    # 分析 twstock 資料
    data = twstock.Stock(stockNumber)
    decision = twstock.BestFourPoint(data).best_four_point()
    price = twstock.realtime.get(stockNumber)
    if price['realtime']['latest_trade_price'] != "-":
        realtime_price = int(float(price['realtime']['latest_trade_price']))
    else:
        realtime_price = int(float(price['realtime']['best_bid_price'][0]))

    name = price['info']['name']

    message = name

    if (decision[0]):
        message += "\ntwStock: 建議買入\n原因：{}".format(decision[1])
    else:
        message += "\ntwStock: 建議賣出\n原因：{}".format(decision[1])

    if stock["decision"]:
        # 個人決策想買
        if (realtime_price < stock['ideal']):
            # 低於購買價格，可能不考慮做任何決策
            message += "\n{} {}<{} 請參考上面四大賣點建議，考慮買進".format(
                name, realtime_price, stock['ideal'])
        else:
            message = "\n{} {}>{} 不做決策".format(
                name, realtime_price, stock['ideal'])
    else:
        # 個人決策想賣
        if (realtime_price > stock['ideal']):
            # 低於購買價格，可能不考慮做任何決策
            message += "\n{} {}>{} 請參考上面四大賣點建議，考慮賣出".format(
                name, realtime_price, stock['ideal'])
        else:
            message = "\n{} {}<={} 不做決策".format(
                name, realtime_price, stock['ideal'])

    if message != "":
        notify.send(message)
    time.sleep(10)
