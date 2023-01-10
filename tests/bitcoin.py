#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import os
import hashlib

def get_current_bitcoin_price(symbol='USD',time_zone=0,proxy='127.0.0.1:21080'):
	''' support symbol: ['USD', 'GBP', 'EUR']
	
'''	
	import requests

	headers = {
		'authority': 'api.coindesk.com',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		# 'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
	}

	rp = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json', headers=headers,timeout=9,proxies=N.set_proxy(proxy) )
	j=rp.json()
	
	symbol=symbol.upper()
	p=j['bpi'][symbol]['rate_float']
	t=j['time']['updatedISO']
	if time_zone:
		dt=U.parse_time(t)+U.timezone_to_timedelta(time_zone)
		t=U.stime(dt)
	
	return U.FloatRepr(p,repr=f"""{p} #{symbol} {t}""" )
getp=price=get_price=get_current_price=get_current_bitcoin_price


def sha256(data):
	digest = hashlib.new("sha256")
	digest.update(data)
	return digest.digest()


def ripemd160(x):
	d = hashlib.new("ripemd160")
	d.update(x)
	return d.digest()


def b58(data):
	B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

	if data[0] == 0:
		return "1" + b58(data[1:])

	x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
	ret = ""
	while x > 0:
		ret = B58[x % 58] + ret
		x = x // 58

	return ret


class Point:
	def __init__(self,
		x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
		y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
		p=2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1):
		self.x = x
		self.y = y
		self.p = p

	def __add__(self, other):
		return self.__radd__(other)

	def __mul__(self, other):
		return self.__rmul__(other)

	def __rmul__(self, other):
		n = self
		q = None

		for i in range(256):
			if other & (1 << i):
				q = q + n
			n = n + n

		return q

	def __radd__(self, other):
		if other is None:
			return self
		x1 = other.x
		y1 = other.y
		x2 = self.x
		y2 = self.y
		p = self.p

		if self == other:
			l = pow(2 * y2 % p, p-2, p) * (3 * x2 * x2) % p
		else:
			l = pow(x1 - x2, p-2, p) * (y1 - y2) % p

		newX = (l ** 2 - x2 - x1) % p
		newY = (l * x2 - l * newX - y2) % p

		return Point(newX, newY)

	def toBytes(self):
		x = self.x.to_bytes(32, "big")
		y = self.y.to_bytes(32, "big")
		return b"\x04" + x + y


def getPublicKey(privkey):
	SPEC256k1 = Point()
	if py.isbytes(privkey):
		pk = int.from_bytes(privkey, "big")
	elif py.isint(privkey):pk=privkey
	else:
		raise py.ArgumentUnsupported(privkey)
	hash160 = ripemd160(sha256((SPEC256k1 * pk).toBytes()))
	address = b"\x00" + hash160

	address = b58(address + sha256(sha256(address))[:4])
	return address


def getWif(privkey):
	if py.isint(privkey):
		privkey=int.to_bytes(privkey,32,'big')
	wif = b"\x80" + privkey
	wif = b58(wif + sha256(sha256(wif))[:4])
	return wif

def get_pub_and_wif(privkey):
	return getPublicKey(privkey),getWif(privkey)
get_pub_wif=get_pub_and_wif	
	

def bip39(mnemonic_words):
	import pprint
	import binascii
	import mnemonic
	import bip32utils
	
	mobj = mnemonic.Mnemonic("english")
	seed = mobj.to_seed(mnemonic_words)

	bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
	bip32_child_key_obj = bip32_root_key_obj.ChildKey(
		44 + bip32utils.BIP32_HARDEN
	).ChildKey(
		0 + bip32utils.BIP32_HARDEN
	).ChildKey(
		0 + bip32utils.BIP32_HARDEN
	).ChildKey(0).ChildKey(0)

	# return {
	#	 'mnemonic_words': mnemonic_words,
	#	 'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
	#	 'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
	#	 'bip32_derivation_path': "m/44'/0'/0'/0",
	#	 'bip32_derivation_addr': bip32_child_key_obj.Address(),
	#	 'coin': 'BTC'
	# }

	return {
		'mnemonic_words': mnemonic_words,
		# 'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
		# 'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
		# 'path': "m/44'/0'/0'/0",
		'addr': bip32_child_key_obj.Address(),
		'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
		'privatekey': bip32_child_key_obj.WalletImportFormat(),
		'coin': 'BTC'
	}

	
if __name__ == "__main__":
	randomBytes = os.urandom(32)
	print("Address: " + getPublicKey(randomBytes))
	print("Privkey: " + getWif(randomBytes))
	