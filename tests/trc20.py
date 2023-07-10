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

def auto_b32(b32):
	if py.istr(b32):
		b=b32.encode('utf-8')[:32]
		b32=b'\x00'*(32-len(b))+b
	return b32

def get_trc20(b32):
	b32=auto_b32(b32)
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
get_address=trc20=get_trc20

def get_erc20(b32):
	'''
pip install coincurve pysha3 

有问题
private_key: b10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6
eth addr: 0xf80999dcaf1cd7ee68f8b72c4e9451581a92bb56
Out[329]: b'\xf8\t\x99\xdc\xaf\x1c\xd7\xeeh\xf8\xb7,N\x94QX\x1a\x92\xbbV'

不等于 0x9858EfFD232B4033E47d90003D41EC34EcaEda94           

'''
	from secrets import token_bytes
	from coincurve import PublicKey
	from sha3 import keccak_256

	b32=auto_b32(b32)

	private_key = keccak_256(b32).digest()
	public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
	addr = keccak_256(public_key).digest()[-20:]

	print('private_key:', private_key.hex())
	print('eth addr: 0x' + addr.hex())
	return addr
erc20=get_erc20