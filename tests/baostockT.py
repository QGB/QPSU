import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

def get_klines(symbol="sh.600000",interval='5',start_date='2023-07-01', end_date='2023-07-31'):

	rs = bs.query_history_k_data_plus(symbol,
		"date,time,code,open,high,low,close,volume,amount,adjustflag",
		start_date=start_date, end_date=end_date,
		frequency=interval, adjustflag="3")
	print('query_history_k_data_plus respond error_code:'+rs.error_code)
	print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

	#### 打印结果集 ####
	data_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		data_list.append(rs.get_row_data())
	df = pd.DataFrame(data_list, columns=rs.fields)
	
	df['t']=df['time'].apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:8] + ' ' + x[8:10] + ':' + x[10:12] + ':' + x[12:])
	df['t']=pd.to_datetime(df['t'])
	
	# date_index=df.groupby(df['time'].dt.date).groups # 日期 序号 字典
	
	return df

	#### 结果集输出到csv文件 ####   
	# print(len(data_list),'\n',result)
# result.to_csv("D:\\history_A_stock_k_data.csv", index=False)

### 登出系统 ####
# bs.logout()