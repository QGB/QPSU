#coding=utf-8
import sys,os
if __name__.endswith('qgb.chrome'):from . import py
else:import py
U,T,N,F=py.importUTNF()

import pychrome  
import pyppeteer  

g=U.get(__name__+'.g')


def open(url='http://127.0.0.1:9222'):
	global g
	if not g:
		# g=pychrome.Browser(url=url)
		g=await pyppeteer.connect(browserURL='http://127.0.0.1:9222')
	return g
	
	
from pyppeteer import launch
import asyncio

url = 'https://okfw.net'

async def main():
	global browser
	# browser = await launch(headless=False, executablePath=r'C:\Users\qgb\AppData\Local\CentBrowser\Application\chrome.exe', userDataDir=r'C:\Users\qgb\AppData\Local\CentBrowser\User Data')
	# page = await browser.newPage()
	# await page.goto(url)
    # await browser.close()

run = asyncio.run(main())	