import time
import twstock
from helpers import telegram

# 先寫死～
stocks = [
    # {'number': '00891',  'ideal': 16, 'decision': False},
    # {'number': '00881',  'ideal': 18, 'decision': False},
    {'number': '2330',  'ideal': 600, 'decision': False},
    # {'number': '00878',  'ideal': 15, 'decision': True},
    {'number': '2891',  'ideal': 20, 'decision': True}
]

# 更新台灣的Code表
twstock.__update_codes()

for stock in stocks:
    stockNumber = stock['number']

    # 分析 twstock 資料
    data = twstock.Stock(stockNumber)
    
    try:
        decision = twstock.BestFourPoint(data).best_four_point()
    except:
        decision = None
    
    price = twstock.realtime.get(stockNumber)
    if price['realtime']['latest_trade_price'] != "-":
        realtime_price = int(float(price['realtime']['latest_trade_price']))
    else:
        realtime_price = int(float(price['realtime']['best_bid_price'][0]))

    name = price['info']['name']

    message = name

    if (decision[0] == True and decision != None):
        message += "\ntwStock: 建議買入\n原因：{}".format(decision[1])
    
    if (decision[0] == False and decision != None):
        message += "\ntwStock: 建議賣出\n原因：{}".format(decision[1])

    if stock["decision"]:
        # 個人決策想買
        if (realtime_price < stock['ideal']):
            # 低於購買價格，可能不考慮做任何決策
            message += "\n{} {}<{} 請參考上面四大賣點建議，考慮買進".format(
                name, realtime_price, stock['ideal'])
        else:
            message = "\n{} {}>{} 不做決策({})".format(
                name, realtime_price, stock['ideal'], "想買")
    else:
        # 個人決策想賣
        if (realtime_price > stock['ideal']):
            # 低於購買價格，可能不考慮做任何決策
            message += "\n{} {}>{} 請參考上面四大賣點建議，考慮賣出".format(
                name, realtime_price, stock['ideal'])
        else:
            message = "\n{} {}<={} 不做決策({})".format(
                name, realtime_price, stock['ideal'], "想賣")

    if message != "":
        telegram.send(message)
        # notify.send(message)
    time.sleep(60)
