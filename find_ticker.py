import pyupbit
import pyupbit as pb
import time
import datetime
import os.path

def get_target_price(ticker): # 티커 하나의 목표가 계산
    df = pb.get_ohlcv(ticker)
    #print(df)
    try:
        yesterday = df.iloc[-2]
    except:
        return 0


    today_open_price = yesterday['close']
    yesterday_high_price = yesterday['high']
    yesterday_low_price = yesterday['low']

    target = round(today_open_price + (yesterday_high_price - yesterday_low_price) * 0.5, 2)

    print(ticker)
    print(today_open_price,'오늘 시작가')
    print(yesterday_high_price,'전날 고가')
    print(yesterday_low_price,'전날 저가')
    print(target,'목표가\n')

    return target

def get_target_prices(): #가능한 모든 티커의 목표가를 계산해서 딕셔너리로 반환
    tickers = pb.get_tickers(fiat = "KRW")
    print(len(tickers),"개의 티커확인됨")
    target_prices={}

    for i, ticker in enumerate(tickers):

        target_value = get_target_price(ticker)
        if target_value != 0:
            target_prices[ticker] = target_value

    print("목표가:",target_prices)
    print("\n 총 ",len(target_prices),"개 종류의 티커의 목표가가 설정됨")
    return target_prices

def get_current_prices(dic_tickers): #임의의 코인의 현재가 조회, 편의상 딕셔너리로 인자를 받고 딕셔너리를 반환
    current_prices = {}
    lst_tickers= []
    for ticker in dic_tickers:
        lst_tickers.append(ticker)
    current_prices = pb.get_current_price(lst_tickers)
    print("현재가 :",current_prices)

    return current_prices


def find_appropriate_coin(target_prices,current_prices): # 적절한 가격의 코인을 찾아냄,
    target_coins = []
    for ticker in target_prices:
        if ticker in current_prices:

            if current_prices[ticker] >= target_prices[ticker]:
                target_coins.append(ticker)

    return target_coins


def test():
    target_coins = []
    target_prices = get_target_prices()
    current_prices = get_current_prices(target_prices)
    target_coins = find_appropriate_coin(target_prices,current_prices)

    print("\n 사야할 코인은 :",target_coins)

test()

