#coding=utf-8
import sys,pathlib
# 如果要修改路径，框选两行，一起删除
#								 *.py /qgb   /[gsqp]  
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py

import pymysql


gargs_list=['host','port','user','passwd','db','charset']
def filter_args(args_dict):
	''' 
pymysql.connect(**ka={
	host(str):      MySQL服务器地址
	port(int):      MySQL服务器端口号
	user(str):      用户名
	passwd(str):    密码
	db(str):        数据库名称
	charset(str):   连接编码
}
	'''
	r={}
	for k,v in args_dict.items():
		if not py.istr(k):continue
		k=k.lower()
		if k=='port':
			v=py.int(v) #  importU().
		if k=='PASSWORD'.lower():k='passwd'
		if k=='NAME'.lower()    :k='db'
		
		if k in gargs_list:
			r[k]=v
			
	return r
# def connect(**ka):
	

def excute(sql,**ka):
	''' copy django settings  database as **ka
	'''
	# print(sql,ka)
	ka=filter_args(ka)
	with pymysql.connect(**ka) as conn:
		conn.execute(sql)
		return [i for i in conn.fetchall()]
	

def executemany(sql,*data,**ka):
	''' "INSERT INTO para5(name,age) VALUES(%s,%s);"

[('次牛444', '12'), ("次牛2", '11'), ('次牛3', '10')]
'''

	ka=filter_args(ka)
	if data:
		if type(data[0]) is tuple:
			pass
		else:
			data=[data]
	conn=pymysql.connect(**ka)
	cursor = conn.cursor()
	try:
		# 执行一条insert语句，返回受影响的行数
		# cursor.execute("INSERT INTO para5(name,age) VALUES(%s,%s);",('次牛','12'))
		# 执行多次insert并返回受影响的行数
		cursor.executemany(sql, data )
		# 提交执行
		conn.commit()
	except Exception as e:
		# 如果执行sql语句出现问题，则执行回滚操作
		conn.rollback()
		print(e)
	finally:
		# 不论try中的代码是否抛出异常，这里都会执行
		# 关闭游标和数据库连接
		cursor.close()
		conn.close()