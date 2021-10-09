import twstock

stock = twstock.Stock('2330')
decision = twstock.BestFourPoint(stock).best_four_point()
print(decision)