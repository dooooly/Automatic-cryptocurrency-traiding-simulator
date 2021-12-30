import find_ticker as ft
import wallet_sim as wa
import order
import time
import datetime
import pickle
import os.path


if os.path.isfile("wallet.txt"):
    print("이전 저장 기록을 불러옵니다")
    with open("wallet.txt","rb") as f:
        a = pickle.load(f)
    print(a.coin_wallet)
else:
    name = input("당신의 이름은? :")
    start_money = input("초기 자금은?: ")
    start_money = round(int(start_money),1)
    a = wa.wallet(name,start_money) #init
    print("입력한 이름으로 지갑이 생성되었습니다.")

now = datetime.datetime.now()
mid = datetime.datetime(now.year,now.month,now.day) + datetime.timedelta(1)


while True:
    try:
        now = datetime.datetime.now()
        if mid < now <mid + datetime.timedelta(seconds=180):
            print("정각입니다")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            order.auto_sellorder(a)
            print("==========오늘 거래 결산입니다============")
            for ticker in a.account_books:
                print(ticker, ":", a.account_books[ticker])
                print("------------------------------------")
            print("잔액: ",a.cash,"원")
            print("=======================================")

        suc = order.auto_buyorder(a,5,"a")
        if suc==True:
            with open("wallet.txt", "wb") as f:
                pickle.dump(a,f)
    except:
        print("반복 단계에서 에러 발생")
    time.sleep(120)