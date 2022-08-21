#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


from binance.client import Client

requests_params = {
	'proxies': {'http': 'socks5h://127.0.0.1:21080', 'https': 'socks5h://127.0.0.1:21080'},
}


client =U.get_or_set(__name__+'.client',
	lazy_default=lambda:Client(*F.dill_load(r'C:\test\binance_testnet_k_s-2.dill'), requests_params=requests_params,testnet=True)
)

symbol='BTCUSDT'
btc_data =U.get_or_set(__name__+'.'+symbol,
 lazy_default=lambda:client.get_historical_klines(symbol,Client.KLINE_INTERVAL_1MINUTE, "3 day ago UTC")
)

#########################
import pandas as pd
df = pd.DataFrame(btc_data)
df[0] = pd.to_datetime(df[0],unit='ms')
df[6] = pd.to_datetime(df[6],unit='ms')
df.rename(columns={0:'DateTime', 1:'open', 2:'high', 3:'low', 4:'close',5:'volume',6:'CloseTime',7:'QuoteAssetVolume',8:'NumberTrades',9:'TakerBuyBaseAssetVolume',10:'TakerBuyQuoteAssetVolume',11:'Ignore'}, inplace=True)
df[['open','high','low','close','volume','TakerBuyBaseAssetVolume','TakerBuyQuoteAssetVolume']] = df[['open','high','low','close','volume','TakerBuyBaseAssetVolume','TakerBuyQuoteAssetVolume']].astype(float)
df['NumberTrades'] = df['NumberTrades'].astype(int)
df.set_index('DateTime', inplace=True)
df['adj close'] = df['close'] # Some functions need adj close
btc_data_df = pd.DataFrame()
btc_data_df[['Open','High','Low','Close','Volume']] = df[['open','high','low','close','volume']]

# Run default strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
	def init(self):
		price = self.data.Close
		self.ma1 = self.I(SMA, price, 10)
		self.ma2 = self.I(SMA, price, 20)

	def next(self):
		if crossover(self.ma1, self.ma2):
			self.buy()
		elif crossover(self.ma2, self.ma1):
			self.sell()


bt = Backtest(btc_data_df, SmaCross, commission=.002,
			  exclusive_orders=True)
stats = bt.run()
bt.plot()
stats