from qgb import py
U, T, N, F = py.importUTNF()

#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from solders.keypair import Keypair
from mnemonic import Mnemonic
import hashlib

def auto_b(b, b_len=16):
	assert len(b) <= b_len
	if py.istr(b):
		b = b.encode('utf-8')[:b_len]	
	b = b'\x00' * (b_len - len(b)) + b
	return b

def get_mnemonic_privateKey_address(b16, **ka):
    account, mnemonic,seed = get_account_mnemonic(b16)
    address = str(account.pubkey())
    private_key = account.secret().hex()

    return mnemonic, private_key, address

def get_account_mnemonic(b16, passphrase='', language='english', num_words=12):
    b16 = auto_b(b16)
    assert len(b16) == 4 * num_words // 3
    mnemonic = Mnemonic(language).to_mnemonic(b16)
    seed = hashlib.sha256(Mnemonic.to_seed(mnemonic, passphrase)).digest() # 有问题， 不确定这一步是否正确，与钱包软件恢复的地址有区别
    keypair = Keypair.from_seed(seed[:32])  
    return keypair, mnemonic,seed

# ###示例用法
# b16 = b"your_secret_bytes"
# mnemonic, private_key, address = get_mnemonic_privateKey_address(b16)
# print("Mnemonic:", mnemonic)
# print("Private Key:", private_key)
# print("Address:", address)	