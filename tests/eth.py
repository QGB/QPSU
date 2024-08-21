#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

from eth_account import Account
Account.enable_unaudited_hdwallet_features() # Hierarchical Deterministic wallet 简称“HD Wallet”
from eth_account.hdaccount import Mnemonic,ETHEREUM_DEFAULT_PATH

def auto_b(b,b_len=16):
	assert len(b)<=b_len
	if py.istr(b):
		b=b.encode('utf-8')[:b_len]
	b=b'\x00'*(b_len-len(b))+b
	return b

def get_mnemonic_privateKey_address(b16,**ka):
	account, mnemonic = get_account_mnemonic(b16)
	address = account.address
	private_key = account.key.hex()

	# print(mnemonic,private_key,address,sep='\n')
	return mnemonic,private_key,address

def get_account_mnemonic(b16,passphrase='',language='english',num_words=12,account_path=ETHEREUM_DEFAULT_PATH,):
	'''
account,mnemonic = Account.create_with_mnemonic()
'''	
	b16=auto_b(b16)
	assert len(b16)== 4 * num_words // 3
	mnemonic = Mnemonic(language).to_mnemonic(b16)
	account =  Account.from_mnemonic(mnemonic, passphrase, account_path)
	return account,mnemonic
	
	