import find_ticker as ft
import wallet_sim as wa
import pyupbit as pb
import math
import datetime
from pandas import DataFrame as df
import pickle

def buy_order(ticker):
    ans = input(ticker, "를 살까요? : y/n")
    if ans == "y":
        print(ticker, "의 현재가는 :", ft.get_target_price(ticker), "원 입니다.")
        unit = input("그럼 몇 개를 주문할까요? 취소하고 싶으시면 0을 입력하세요 : unit =")
        if unit == 0:
            print("\n주문을 중단합니다.")



def auto_buyorder(wallet,div_unit =5 , state = "a"): #state = "a":입력안받고 자동주문, "s": 수동주문

    if div_unit <=0:
        print("불가능한 단위입니다. 0 이상의 수로 입력해주세요")
        return False
    ans = "y"
    if state == "s":
        print("현재 ",wallet.cash,"원 만큼 현금이 있습니다.\n")
        ans = input((div_unit,"분할로 주문 할까요?: y/n"))


    if ans == "y":
        if wallet.coin_unit == 0:
            wallet.coin_unit = div_unit

        cash_unit = wallet.cash/div_unit

        print("추천 티커를 불러옵니다.")
        tickers = ft.test()

        for i, ticker in enumerate(tickers):
            if wallet.coin_unit == 0:
                print("더이상 주문할 수 없습니다: 잔액부족")
                return True
            if ticker in wallet.coin_wallet.index: #중복구매 방지
                continue
            print(len(tickers),"종류의 코인을 주문합니다.")
            buy_price = ft.pb.get_current_price(ticker)
            unit = round(cash_unit / buy_price , 4)
            wallet.buy_coin(ticker, unit, buy_price)

            wallet.coin_unit -= 1
        return True
    else:
        print("취소되었습니다")
        return False
def auto_sellorder(wallet):

    coins = wallet.coin_wallet.index

    for coin in coins:
        price = ft.get_target_price(coin)
        unit = wallet.coin_wallet.loc[coin][0]
        wallet.sell_coin(coin,unit,price)

    wallet.coin_wallet = df(columns=['unit','buy_price']) #초기화
    print("전량 매도완료 후 초기화 되었습니다")
'''
    wallet.cash_change.append = wallet.cash
    try:
        print("자산 변동: ",wallet.cash_change[-2]-wallet.cash)
    except:
        print("오늘부터 기록합니다.")
'''
