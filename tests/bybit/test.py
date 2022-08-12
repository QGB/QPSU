
# import os
# os.environ["HTTP_PROXY"]=os.environ["HTTPS_PROXY"] = 'socks5://127.0.0.1:21080'

# import requests
# u='https://ipinfo.io'
# rp=requests.get(u)
# print(rp,rp.text)

# u='https://public.bybit.com/trading/BTCUSD/'
# rp=requests.get(u)
# print(rp,rp.text)

from bybit_backtest import Backtest

class MyBacktest(Backtest):

	def strategy(self):
		fast_ma = self.sma(period=5)
		slow_ma = self.sma(period=25)
		# golden cross
		self.sell_exit = self.buy_entry = (fast_ma > slow_ma) & (
			fast_ma.shift() <= slow_ma.shift()
		)
		# dead cross
		self.buy_exit = self.sell_entry = (fast_ma < slow_ma) & (
			fast_ma.shift() >= slow_ma.shift()
		)

ka=dict(	
sqlite_file_name =f'c:/test/trade/{__file__}/bt.db',
download_data_dir=f'c:/test/trade/{__file__}/'
)	

MyBacktest(**ka).run()
