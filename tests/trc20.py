#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import ecdsa
import base58
import ecdsa
import random

from Crypto.Hash import keccak


def keccak256(data):
	hasher = keccak.new(digest_bits=256)
	hasher.update(data)
	return hasher.digest()


def get_signing_key(raw_priv):
	return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)


def verifying_key_to_addr(key):
	pub_key = key.to_string()
	primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
	# 0 (zero), O (capital o), I (capital i) and l (lower case L)
	addr = base58.b58encode_check(primitive_addr)
	return addr


def get_address(b32):
	if py.istr(b32):
		b=b32.encode('utf-8')[:32]
		b32=b'\x00'*(32-len(b))+b
	raw=b32
	# raw = bytes(random.sample(range(0, 256), 32))
	# raw = bytes.fromhex('a0a7acc6256c3..........b9d7ec23e0e01598d152')
	key = get_signing_key(raw)
	addr = verifying_key_to_addr(key.get_verifying_key()).decode()
	print('Address    : ', addr)
	print('Address hex: ', base58.b58decode_check(addr.encode()).hex())
	print('Public  Key: ', key.get_verifying_key().to_string().hex())
	print('Private Key: ', raw.hex())
	print('Private b32: ', raw)
	return addr
	# break
