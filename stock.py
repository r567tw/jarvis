import time
import twstock
from helpers import notify

message = ""
stocks = [
    {'number': '00878', 'cost': 19.36, 'volume': 1000},
    {'number': '00888', 'cost': 14.24, 'volume': 6000},
    {'number': '00896', 'cost': 14.63, 'volume': 1000},
    {'number': '2891', 'cost': 23.13, 'volume': 1000}
]

need_decisions = ['00888']

def get_stock_info(stock_number):
    try:
        price = twstock.realtime.get(stock_number)
        if price['success']:
            # print(price)
            name = price['info']['name']
            realtime_price = float(price['realtime']['latest_trade_price'])
            # print(realtime_price)
            return name, realtime_price
        else:
            print(f"無法獲取 {stock_number} 的實時數據")
            return None, None
    except Exception as e:
        print(f"錯誤: {e}")
        return None, None

def analyze_investment(stock, name, realtime_price):
    profit = round(realtime_price * stock['volume'] - stock['cost'] * stock['volume'], 2)
    status = "賺錢中" if profit > 0 else "賠錢中"
    return f"{name} {status} 預估 {profit} 元\n",profit

total_profit = 0

for stock in stocks:
    stock_number = stock['number']
    name, realtime_price = get_stock_info(stock_number)

    if name and realtime_price:
        suggestion,profit = analyze_investment(stock, name, realtime_price)
        total_profit += profit
        if profit < 0:
            message += suggestion

        data = twstock.Stock(stock_number)
        try:
            if stock_number in [decision for decision in need_decisions]:
                decision = twstock.BestFourPoint(data).best_four_point()
                action = "買進" if decision[0] else "賣出"
                message += f"建議{action} {name}, 原因：{decision[1]}\n"
        except Exception as e:
            message += f"{name}資料過少，無法分析四大買賣點。錯誤: {e}\n"

    time.sleep(5)  # 延遲時間
    # break

print("Finish !")
message += f"其餘股票損益為正數\n"
message += f"預估總損益：{total_profit}"
notify.send(message=message)