# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pyupbit
import pyupbit as pb
import time
import datetime
import os.path

path = 'my_money.txt'
mymoney = 0
mywallet ={}
ticker = "KRW-NEAR"

def get_target_price(ticker): # 목표가 계산
    df = pb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open_price = yesterday['close']
    print(today_open_price,'오늘 시작가')
    yesterday_high_price = yesterday['high']
    print(yesterday_high_price,'전날 고가')
    yesterday_low_price = yesterday['low']
    print(yesterday_low_price,'전날 저가')
    target = today_open_price + (yesterday_high_price - yesterday_low_price) * 0.5
    print(target,'목표가')
    return target

def update_wallet(money,coinwallet,tick,unit,checker):
    with open(path,"a") as f:
        today = str(datetime.datetime.today().month) + "/" \
                + str(datetime.datetime.today().day) + " " + checker
        krwdata = "KRW:" + str(money)
        coinwallet[tick]= unit
        coindata = tick + ":" + str(coinwallet[tick])

        f.writelines(["\n",str(today),"\n",str(krwdata),"\n",str(coindata),"\n"])

if not(os.path.isfile(path)):
    mymoney = 100000000 #1억

    mywallet = {ticker:0}
    print("I have ",mywallet[ticker],ticker[-3:],"  now.")

    with open(path,"w") as f:
        today = str(datetime.datetime.today().month) + "/" + str(datetime.datetime.today().day)
        krwdata = "KRW:" + str(mymoney)
        coindata = str(ticker) + ":" + str(mywallet[ticker])
        f.writelines([str(today),"\n",str(krwdata),"\n",str(coindata)+"\n"])
else:
    with open(path,"r") as f:
        lines = f.readlines()
        a=(lines[-2].split(":")[-1][:-4])
        mymoney = int(a)
        mywallet[ticker] = float(lines[-1].split(':')[-1])


        print("현금: ",mymoney,"코인: ", mywallet[ticker])



"""
while True:
    price = pb.get_current_price("KRW-BTC")
    print(price)
    time.sleep(0.2)
"""



now = datetime.datetime.now()
mid = datetime.datetime(now.year,now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price(ticker)

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds = 10) :
            if mywallet[ticker]>0:
                target_price = get_target_price(ticker)
                print("목표가를 갱신했습니다. 목표가: ",target_price)
                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                unit = mywallet[ticker]#전량매도
                orderbook = pb.get_orderbook(ticker)
                buy_price = orderbook['orderbook_units'][0]['bid_price']

                print("현재 판매하는 호가: ",buy_price)
                mymoney += unit * buy_price
                mymoney = round(mymoney,-1)
                mywallet[ticker] -= unit
                print("매도 후 지갑 잔고: ", mymoney, "KRW - and ", mywallet[ticker], ticker)
                update_wallet(mymoney, mywallet,ticker, unit,"SELL")

        current_price = pyupbit.get_current_price(ticker)
       # print(current_price,'-',target_price)
        if current_price > target_price:
            if current_price < mymoney:
                orderbook = pb.get_orderbook(ticker)
                sell_price = orderbook['orderbook_units'][0]['ask_price']

                unit = mymoney / float(sell_price)
                unit = round(unit, 1)

                mymoney -= unit * sell_price
                if mymoney < 0:
                    unit -=1
                    mymoney += sell_price
                mymoney = round(mymoney,-1)
                mywallet[ticker] += unit
                print('현재 구매하는 호가: ',sell_price)
                print("총 ",unit,"개 구매했습니다")
                print("매수 후 지갑 잔고: ",mymoney,"KRW - and ",mywallet[ticker], ticker)
                update_wallet(mymoney, mywallet, ticker, unit,"BUY")
        print(mywallet[ticker])
    except:
        print("에러가 있었습니다.")


    time.sleep(1)

