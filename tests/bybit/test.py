
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
		# fast_ma = self.sma(period=5)
		# slow_ma = self.sma(period=25)
		# bb=self.bbands(band=3)
		# golden cross
		# self.df['C']
		
		
		self.sell_exit = self.df.L.rolling(20).min()<10540
		self.buy_entry = (  self.df.L.rolling(20).min()<4000		)
		# dead cross
		self.buy_exit = self.df.H.rolling(20).max()>10000 
		self.sell_entry = (	 self.df.H.rolling(20).max()>10540 	)

ka=dict(	
sqlite_file_name =f'c:/test/trade/{__file__}/bt.db',
download_data_dir=f'c:/test/trade/{__file__}/'
)	

MyBacktest(**ka).run()
