import csv
total_cash = 100.0
total_share = 0.0
do_nothing_share = 0
sell_margin_200 = 0.88
buy_margin_50 = 1.00
sell_gap_margin = 1
buy_gap_margin = 1#0.98
in_cash = True
latest_price = 0
init = True
can_sell = False
with open('SPY.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        # print row
        if init:
            init = False
            continue
        
        date = row[0]
        day_close_price = float(row[4])
        avg_50 = float(row[7])
        avg_200 = float(row[8])
        can_buy = avg_50 > avg_200 * buy_gap_margin
        can_sell = avg_200 > avg_50 * sell_gap_margin
        # initialize
        if avg_200 == day_close_price:
            total_share = total_cash / avg_200
            do_nothing_share = total_share
            in_cash = False
        # sell all if 90% of avg_200
        if not in_cash:
            if day_close_price <= avg_200 * sell_margin_200 and can_sell:
                total_cash = total_share * day_close_price
                in_cash = True
                print 'Sell on: ' + date + ' price: ' + str(day_close_price)
        # buy all if day close > 1.1 avg_50
        if in_cash:
            if day_close_price >= avg_50 * buy_margin_50 and can_buy:
                total_share = total_cash / day_close_price
                in_cash = False
                print 'Buy on: ' + date + ' price: ' + str(day_close_price)
        latest_price = day_close_price
if in_cash:
    print 'Total cash: ' + str(total_cash)
else:
    print 'Total cash: ' + str(total_share * latest_price)

print 'Do nothing cash: ' + str(do_nothing_share * latest_price)