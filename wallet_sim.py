import pandas as pd
from pandas import DataFrame as df
import datetime
import time

class wallet:
    def __init__(self,name,start_money = 1000000):
        self.name = name
        self.cash = start_money
        self.cash_change = []
        self.coin_wallet = df(columns=['unit','buy_price'])
        self.coin_unit = 0
        # self.account_book = df(columns=['price','sell_price','profit & loss']) #index(row) = Date (달/일)
        self.account_books = {}  # 티커별로 묶어주세용


    def buy_coin(self,ticker,unit,buy_price): #티커는 하나씩
        # 추가 매수와 이에 따른 평단가 변화는 구현하지 않음. 1일에 1번 구매한다 가정하였기 때문
        total_price = round(unit * buy_price,4)

        if self.cash > total_price:
            self.cash -= total_price
            try:
                pre_unit = self.coin_wallet.loc[ticker, 'unit']
            except:
                print("해당 티커의 이전 거래기록이 없습니다. 새로 생성합니다.\n")
                self.coin_wallet.loc[ticker] = [0,0]
            u = self.coin_wallet.loc[ticker,'unit']
            b = self.coin_wallet.loc[ticker,'buy_price']
            res_price = (u * b + unit * buy_price)/(u + unit)
            self.coin_wallet.loc[ticker] = [unit + u,res_price]

            self.update_account(ticker,buy_price,unit,'b')
            print("========현재 코인 지갑상황=============")
            print(self.coin_wallet)
            print("잔액: ",round(self.cash,4),"원")
            print("====================================")
        else:
            print("증거금 부족!\n")

    def buy_coins(self,asks): #asks : index = 티커 column = unit, price 인 데이터프레임
        # 여러 티커 한번에 (데이터프레임으로 요구사항을 받음)
        for i in range(asks.shape[0]):
            ticker = asks.index[i]
            unit = asks.column[0]
            price = asks.column[1]
            self.buy_coin(ticker,unit,price)


    def sell_coin(self,ticker,unit,sell_price):


        if self.coin_wallet.loc[ticker]['unit'] >= unit:
            self.coin_wallet.loc[ticker]['unit'] -= unit #전량매도가 규칙이므로 결과는 0이어야 정상
            total_price = unit * sell_price
            self.cash += total_price
            isfail = self.update_account(ticker,sell_price,unit,'s')
            if isfail == False:
                 print("거래가 취소되었습니다. 거래를 중단합니다")

            print("========현재 코인 지갑상황=============")
            print(self.coin_wallet)
            print("====================================")

        else:
            print("코인 잔액 부족!\n")

    def sell_coins(self,asks): #asks : index = 티커 column = unit, price 인 데이터프레임
        # 여러 티커 한번에 (데이터프레임으로 요구사항을 받음)
        for i in range(asks.shape[0]):
            ticker = asks.index[i]
            unit = asks.column[0]
            price = asks.column[1]
            self.sell_coin(ticker,unit,price)

    def update_account(self,ticker,price,unit,state):
        #state : "Sell" == "s"  "Buy" == "b"
        Date = datetime.datetime.today().strftime('%m/%d/%H:%M')
        timestamp = time.time()
        Date = Date + str(timestamp)
        account_book = df(index = ['current'], columns=['buy_price', 'sell_price','unit','profit & loss'])
        if ticker not in self.account_books:
            self.account_books[ticker] = account_book

            self.account_books[ticker].loc['current'] = [0,0,0,0]

            #self.account_books[ticker].loc[0] = [Date,None,None,None,None]
# =======================

        account = self.account_books[ticker]


        if state == "b":
            account.loc[Date] = [None,None,None,None]
            account.loc[Date][0] = price
            account.loc[Date][2] = unit

            if account.loc['current'][0] == None or 0: #평단가 갱신
                account.loc['current'][0] = price
            else:
                temp = price * unit + account.loc['current'][0] * account.loc['current'][2]
                act_price = temp / (unit + account.loc['current'][2]) #평단가
                account.loc['current'][0] = act_price
            account.loc['current'][2] += unit

            print("\n거래 후 상황 =====\n",account.loc['current'])
            self.account_books[ticker] = account
        elif state == "s" :
            account.loc[Date] = [None,None,None,None]
            if account.loc['current'][2] == None or 0: #unit조회
                print("\n매수가가 기록이 안되어있습니다.\n")
                return False
            elif account.loc['current'][2] < unit:
                print("\n보유 코인수가 부족합니다!\n")
                return False
            else:
                account.loc[Date][1] = price #sell_price
                account.loc[Date][2] = -unit

                gap = price - account.loc['current'][0]
                profit = gap * unit

                account.loc['current'][2] -= unit  # 결과는 0개가 될 것임
                account.loc['current'][3] += profit
                account.loc[Date][3] = profit

                self.account_books[ticker] = account
        print("\n거래 결과를 기록했습니다: \n",Date," ",ticker," ",price,"원 ",unit,"개 \n총 ",round(unit * price,2),"원 ",state)

        print("=========결과=========\n",account)
'''
a = wallet('peter')
a.buy_coin("KRW-BTC",3,30000)
a.sell_coin("KRW-BTC",1,10000)
a.buy_coin("KRW-BTC",3,20000)
print(a.coin_wallet.index)
if "KRW-BTC" in a.coin_wallet.index:
    print("있네요")
'''