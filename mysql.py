#coding=utf-8
import pymysql

# gdArgs={}
# def connect(**ka):
	

def excute(sql,**ka):
	# print(sql,ka)
	with pymysql.connect(**ka) as conn:
		conn.execute(sql)
		return [i for i in conn.fetchall()]
	

def executemany(sql,*data,**ka):
	''' "INSERT INTO para5(name,age) VALUES(%s,%s);"

[('次牛444', '12'), ("次牛2", '11'), ('次牛3', '10')]
'''
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