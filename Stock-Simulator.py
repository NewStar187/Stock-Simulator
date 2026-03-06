import requests
from bs4 import BeautifulSoup
import time
import os

class StockSimulator:
    def __init__(self, initial_cash=10000000):
        self.cash = initial_cash
        self.stock_count = 0
        self.avg_price = 0
        self.ticker = "005930"  # 삼성전자 종목코드 (네이버)

    def get_realtime_price(self):
        """네이버 금융에서 삼성전자 현재가를 직접 크롤링합니다."""
        url = f"https://finance.naver.com/item/main.naver?code={self.ticker}"
        
        # 봇(Bot) 차단 방지용 헤더를 추가.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 네이버 금융의 현재가 위치 파악.
            price_tag = soup.select_one(".no_today .blind")
            if price_tag:
                price_str = price_tag.text.replace(",", "")
                return int(price_str)
            else:
                return None
        except Exception as e:
            print(f"⚠️ 데이터 수집 오류: {e}")
            return None

    def buy(self, amount):
        current_price = self.get_realtime_price()
        if not current_price: return
        
        total_cost = current_price * amount
        if total_cost > self.cash:
            print("❌ 잔액이 부족합니다!")
            return

        total_spent = (self.avg_price * self.stock_count) + total_cost
        self.stock_count += amount
        self.avg_price = total_spent / self.stock_count
        self.cash -= total_cost
        print(f"✅ 매수 완료! (현재가: {current_price:,}원)")

    def sell(self, amount):
        if amount > self.stock_count:
            print("❌ 보유 수량이 부족합니다!")
            return

        current_price = self.get_realtime_price()
        if not current_price: return
        
        revenue = current_price * amount
        self.stock_count -= amount
        self.cash += revenue
        
        if self.stock_count == 0:
            self.avg_price = 0
        print(f"✅ 매도 완료! (현재가: {current_price:,}원)")

    def show_status(self):
        curr_price = self.get_realtime_price()
        if not curr_price: return

        total_value = self.cash + (self.stock_count * curr_price)
        profit_loss = (curr_price - self.avg_price) * self.stock_count if self.stock_count > 0 else 0
        profit_rate = (profit_loss / (self.avg_price * self.stock_count) * 100) if self.stock_count > 0 else 0

        print("\n" + "="*45)
        print(f"🏛️  [실시간 네이버 증권 연동 계좌]")
        print(f"💵 보유 현금: {self.cash:,.0f}원")
        print(f"📉 보유 주식: {self.stock_count}주 (평단가: {self.avg_price:,.0f}원)")
        print(f"🚀 삼성전자 실시간가: {curr_price:,.0f}원")
        print(f"💰 평가 손익: {profit_loss:,.0f}원 ({profit_rate:+.2f}%)")
        print(f"💳 총 자산 가치: {total_value:,.0f}원")
        print("="*45)

def main():
    sim = StockSimulator()
    print("네이버 실시간 데이터 기반 삼성전자 모의투자 시작")
    
    while True:
        sim.show_status()
        print("\n[1] 매수 | [2] 매도 | [3] 새로고침 | [4] 종료")
        choice = input("입력: ")

        if choice == '1':
            try:
                cnt = int(input("매수 수량: "))
                sim.buy(cnt)
            except: print("숫자만 입력하세요.")
        elif choice == '2':
            try:
                cnt = int(input("매도 수량: "))
                sim.sell(cnt)
            except: print("숫자만 입력하세요.")
        elif choice == '3':
            print("🔄 실시간 정보를 가져오는 중...")
            time.sleep(0.5)
        elif choice == '4':
            print("👋 프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()