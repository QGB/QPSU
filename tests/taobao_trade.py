import asyncio
import pyppeteer

from qgb import py
U,T,N,F=py.importUTNF()
from qgb import A

taobao_trade=U.getMod(__name__)
URL_WULIU_BY_TRADE_ID='https://buyertrade.taobao.com/trade/json/transit_step.do?bizOrderId='
URL_TRADE_LIST='https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
URL_WebDriver_DETECT=URL_WEBDRIVER_DETECT='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
us=zu=F.dill_load('C:/test/zu-67.dill')  

def _registed_click_pop_cart():
	if U.isWin():
		from qgb import Win
		ox,oy=Win.get_cursor_pos()
		x,y=1080,123
		
		Win.click(884,717) #scroll bottom
		U.sleep(0.3)
		Win.click(657,674) #add btn
		U.sleep(1.6)
		for i in range(19):
			if Win.get_color([889, 485])!=12698049:#grey
				Win.click(1080,123)#pop btn
				U.log(i)
				break
			U.sleep(0.3)
		else:
			return 'error'
		Win.click(888,274)#s top
		U.sleep(0.3)
		Win.click(ox,oy)
		return ox,oy

def registe_click_pop_cart_hotkey(hotkey='alt+z',callback=_registed_click_pop_cart):
	k=U.get(hotkey)
	# if k:
		# print(U.stime(),'using registed hotkey',hotkey)
		# return k
	import keyboard
	
	keyboard.unhook_all_hotkeys() #
	
	k=keyboard.add_hotkey(hotkey, callback)
	return hotkey,U.set(hotkey,k),id(k)
hotkey=bind_click_pop_cart_hotkey=registe_click_pop_cart_hotkey

async def get_element_absolute_position_of_system_screen(page,selector,green=False):
	if green:
		await page.evaluate(''' e=document.querySelector('%s').style.backgroundColor='green' '''%selector)
		
	x,y= await page.evaluate(''' e=document.querySelector('%s').getBoundingClientRect();[e.x,e.y] '''%selector)
	return x+34,y+71
	
get_xy=get_abs_xy=get_element_xy=get_element_absolute_position_of_system_screen	
	 
async def try_evaluate(page,code):
	try:
		return await page.evaluate(code)
	except Exception as e:
		return py.No(e)
try_eval=evaluate=try_evaluate

u_key_defs='pyppeteer.us_keyboard_layout.keyDefinitions'
async def press_keys(page,*s,xy=(None,None)):
	from qgb import Win
	if len(s)==1 and py.istr(s[0]):
		key_defs=U.get(u_key_defs)
		if not key_defs:
			key_defs=[]
			for k,v in pyppeteer.us_keyboard_layout.keyDefinitions.items():
				if py.len(k)>1:
					key_defs.append(k)
			U.set(u_key_defs,key_defs)
		## cache end
		if s not in key_defs: # if in, s=tuple(skey)
			s=s[0]
	xy=Win.click(*xy)
	for k in s:
		await page.keyboard.press(k)
	return s,xy
	
async def backup_cookie(user=0,page=py.No('auto last -1')):
	if not user:
		user=await get_taobao_user()
	if not page:page=await get_page()
	ck=await get_all_cookies(page)
	print('get_all_cookies len:',py.len(ck))
	if not ck:return ck
	
	f=F.dill_dump(obj=ck,file=f'{user}-{len(ck)}-cookies') 
	
	await page.deleteCookie(*ck)
	cks=await get_all_cookies(page)
	print('deleteCookie','done !','now len == %s'%py.len(cks))

	return f

async def get_all_cookies(page=py.No('auto last -1')):
	if not page:page=await get_page()
	r=await page._client.send('Network.getAllCookies')  
	return r['cookies']
	
async def del_cookies(ck,page=py.No('auto last -1')):
	page=await get_or_new_page(page)
	if py.islist(ck):
		await page.deleteCookie(*ck)
	if py.isdict(ck):
		await page.deleteCookie(ck)
		
async def set_cookies(ck,page=py.No('auto last -1')):
	if not page:page=await get_page()
	if py.islist(ck):
		await page.setCookie(*ck)
	if py.isdict(ck):
		await page.setCookie(ck)

async def set_viewport(pages=py.No('auto all pages'),**ka):
	''' 	#1347 看不到，1322 有留白'''
	if 'width' not in ka:
		ka['width']=1366-26
	if 'height' not in ka:
		ka['height']=768-98
	a={'width':ka['width'],'height':ka['height']}
	
	if not pages:pages=await taobao_trade.browser.pages()
	if not py.islist(pages):
		if not isinstance(pages,pyppeteer.page.Page):
			return py.No(U.v.isinstance(pages,pyppeteer.page.Page) )
		pages=[pages]
	for page in pages:
		await page.setViewport(a)
	return len(pages),ka

def is_chrome_process_exists():
	if U.iswin():
		ps= U.ps('chrome.exe')
		if ps:
			U.set('chrome.exe',ps[0].exe())
		return ps
	elif U.isnix():
		return U.ps('chrome')
	else:
		raise EnvironmentError('#TODO not support this system')
uk='pyppeteer.connect'
browser=U.get(uk)
async def get_browser(browserURL='http://127.0.0.1:9222',browserWSEndpoint='',
	executablePath=r'C:\Users\qgb\AppData\Local\CentBrowser\Application\chrome.exe'):
	''' await tb.pyppeteer.launcher.get_ws_endpoint('http://127.0.0.1:9222')
# if not chrome.exe or : BrowserError: Browser closed unexpectedly:	
	'''
	global browser
	browser=U.get(uk)
	if browser:
		try:
			await browser.version()
			# pages = await browser.pages()#这样不能检测浏览器是否关闭
			return browser
		except:
			browser=U.set(uk,py.No(U.stime()))
			
	try:
		if browserWSEndpoint:
			browser=await pyppeteer.connect(browserWSEndpoint=browserWSEndpoint)
		else:
			with pyppeteer.launcher.urlopen(browserURL) as f:
				data = T.json_loads(f.read().decode())			
			browser=await pyppeteer.connect(browserURL=browserURL)
	except Exception as e: #
		U.log(e)
		# if is_chrome_process_exists(): # 会自动开一个 全新环境
			# ret
		browser=await pyppeteer.launcher.launch({'executablePath': executablePath, 'headless': False, 'slowMo': 30})
	
	return U.set( uk,browser)

	
	
async def get_all_pages():
	ps=await browser.pages()
	# r=[]
	for n,pa in py.enumerate(ps):
		t=await pa.title()
		print(fr'{n:>02d} {t[:33]:33} {pa.url[33:]:33} {py.repr(pa)[-11:] }' )
	return ps
async def new_page(url='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html',timeout=30*1000):
	''' Go to the ``url``.

:arg string url: URL to navigate page to. The url should include
				 scheme, e.g. ``https://``.

Available options are:

* ``timeout`` (int): Maximum navigation time in milliseconds, defaults
  to 30 seconds, pass ``0`` to disable timeout. The default value can
  be changed by using the :meth:`setDefaultNavigationTimeout` method.
* ``waitUntil`` (str|List[str]): When to consider navigation succeeded,
  defaults to ``load``. Given a list of event strings, navigation is
  considered to be successful after all events have been fired. Events
  can be either:

  * ``load``: when ``load`` event is fired.
  * ``domcontentloaded``: when the ``DOMContentLoaded`` event is fired.
  * ``networkidle0``: when there are no more than 0 network connections
	for at least 500 ms.
  * ``networkidle2``: when there are no more than 2 network connections
	for at least 500 ms.

The ``Page.goto`` will raise errors if:

* there's an SSL error (e.g. in case of self-signed certificates)
* target URL is invalid
* the ``timeout`` is exceeded during navigation
'''
	browser=await get_browser()
	page=await browser.newPage()
	await page.setViewport(VIEW_PORT)
	await page.evaluateOnNewDocument(JS_ONLOAD)
	if '://' not in url:
		url='https://'+url
	if '#' not in url:
		url+='#'+U.stime()
	await page.goto(url,timeout=timeout)
	return page
	
async def _get_page_by_url(browser,url):
	for i in range(8):
		try:
			all_pages=await get_pages_onload()
			break
		except Exception as e:
			print('_get_page_by_url ',U.stime(),e)
			print()
			continue
	for n,detected,page,u in all_pages:
		if u.startswith(url):
			return page
	else:
		for n,detected,page,u in all_pages:
			if url in u: # 优先 startswith，因为是两次循环匹配
				return page
		else:
			return py.No('can not found page.url.startswith  or  in page.url:'+url)
		return py.No('can not found page url.startswith:'+url)

async def get_page(page=None,url=py.No(URL_TRADE_LIST),wait=None,browser=None):
	global JS_ONLOAD
	# py.pdb()()
	if py.istr(page) and not url: # and ('://' in page) 
		url,page=page,None
	if not browser:browser=await get_browser()
	if not page and not url:
		return (await browser.pages())[-1]
	if not url:url=URL_TRADE_LIST
	if not wait and not page:
		page=await _get_page_by_url(browser,url)
	if wait and not page:
		start=U.timestamp()
		while not page:
			page=await _get_page_by_url(browser,url)
			await A.sleep(py.max(0.1,wait/10))
			if U.timestamp()-start > wait:
				return py.No('%s sec timeout!,can not found page.url:%s'%(wait,url))
	return U.set('page',page)
	
		
	
	# await page.goto('https://okfw.net/r='+repr(U.stime() )  )
	# nw=await page.evaluate(JS_DETECT_AUTOMATION) 
	# if nw:
	# 	# ###JS_ONLOAD=F.read('C:/test/p.js')
	# 	await page.evaluateOnNewDocument(JS_ONLOAD)
	# 	await page.reload() # 刷新才生效

	# await page.setViewport({'width':1340,'height':670})

	# return page
	
async def get_pages_onload(pages=None,viewport=None):
	if not pages:
		pages = await browser.pages()
	r=[]			
	for n,page in enumerate(pages):
		row=[n,await page.evaluate(JS_DETECT_AUTOMATION),page,
			U.StrRepr(page.url,size=80,cut=1), 
		]
		r.append(row)
	return r
VIEW_PORT={'width':1340,'height':670}
async def set_pages_onload(pages=None,viewport=VIEW_PORT):
	if not pages:
		p4s=await get_pages_onload()
		pages=[i[2] for i in p4s]
	for page in pages:
		try:
			if await page.evaluate(JS_DETECT_AUTOMATION) :
				await page.evaluateOnNewDocument(JS_ONLOAD)
				await page.evaluate(JS_ONLOAD)
				# await page.reload() # 刷新才生效
				if viewport and py.isdict(viewport):
					await page.setViewport(viewport)
		except Exception as e:
			print(e)
	return await get_pages_onload(pages=pages)

async def scroll_page_bottom(page):
	return await page.evaluate('window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);')
page_scroll_bottom=scroll_page_bottom	

async def get_or_new_page(url,select_tab=True,timeout=30*1000):
	tb=taobao_trade
	pa=await tb.get_page(url)
	if not pa:
		pa=await tb.new_page(url,timeout=timeout)
	if select_tab:
		await pa.bringToFront()
	return pa
	
# async def   (url):
######### taobao  start ######################################################
######### taobao  start ######################################################

async def get_taobao_user(page=None):
	if page:
		return await page.evaluate(taobao_trade.js_get_user)
	ps=await browser.pages()
	 # r=[]
	for n,pa in py.enumerate(ps):
		u=await try_evaluate(pa,taobao_trade.js_get_user)
		if u:
			t=await pa.title()
			print(n,(t+'\t'+pa.url)[:99])
			return u
	raise NotFound_taobao_user
get_user=get_taobao_user
	
async def delay_trade_time(ipage_or_ids):
	import requests
	tb=taobao_trade
	headers={'authority': 'trade.taobao.com',
 'accept': '*/*',
 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
 'content-type': 'application/x-www-form-urlencoded',
 'origin': 'https://trade.taobao.com',
 'sec-fetch-site': 'same-origin',
 'sec-fetch-mode': 'cors',
 'sec-fetch-dest': 'empty',
 'referer': 'https://trade.taobao.com/trade/sellerDelayConsignmentTime.htm',
 'accept-language': 'zh-CN,zh;q=0.9'}
	cks=await tb.get_all_cookies()
	dck={}
	for n,c in py.enumerate(cks):
		if 'taobao.com' in c['domain'] and not U.one_in(['login.','airunit.','cart.',], c['domain']):
			dck[c['name'] ]=c['value']
			print(n,'%-15s'%c['name'],c['domain'])
	##########		
	if py.isint(ipage_or_ids):
		pa=await tb.get_or_new_page('https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?action=itemlist%2FBoughtQueryAction&event_submit_do_query=1&tabCode=waitSend')
		await pa.evaluate('''document.querySelector('[class*="pagination-item pagination-item-%s"]').click()   '''%ipage_or_ids)

		ids=await pa.evaluate('''(function(){
	  var xa=xpath_all("//span[contains(., '订单号')]/following-sibling::span[1+1]")
	  r=[]
	  for(var i of xa){
		  r.push(i.textContent)
	  }
	   return r
	})()''')
	else:
		ids=py.list(ipage_or_ids)
	didr=U.get_or_set('id-resp',{})
	didrg=U.get_or_set('id-resp_g',{})
	print(ids,U.len(dck,ids,didr,didrg ))
	for n,id in enumerate(ids):
		if id in didr:
			print('# skip',n,id)
			continue
		data = {  'bizType': '200',
	'bizOrderId': id,
	'stepNo': '0'
	}
		resp=response = requests.post('https://trade.taobao.com/trade/sellerDelayConsignmentTimeHandler.do', headers=headers,cookies=dck,data=data)
		print('[%s]  '%n,id,resp,resp.text[:99])
		didr[id]=resp
		try:resp.json()
		except Exception as e:
			print(id,e,resp.content)
			continue
			

		resp_g = requests.get(resp.json()['callBackUrl'], headers=headers ,cookies=dck)
		print('[%s]  '%n,id,resp_g,resp_g.text[:99])
		didrg[id]=resp_g

	return ids,F.dp(U.get_multi_return_list('id-resp','id-resp_g'),'[didr,didrg]'+U.stime()),U.len(ids,didr,didrg )
	


async def save_item_html_and_sku(url,close=False,timeout=30*1000):
	tb=taobao_trade
	f=T.filename_legalized(url)[:250]
	if not f.endswith('.html'):f+='.html'
	if F.exist(U.gst+f[:-5]+'.dill'):
		return py.No('exist',f)	
	# return	py.pdb()()
	pa=await tb.get_or_new_page(url,timeout=timeout)
	nspeed=1024*99
	while nspeed > 1024*80:
		nt,nm=U.ftime(),U.get_net_io_bytes()
		await A.sleep(1)
		nspeed=F.IntSize( (U.get_net_io_bytes()-nm)/(U.ftime()-nt) )
		
	
	h=await pa.evaluate("document.documentElement.outerHTML") 
	f=F.write(f,h)
	try:
		sku=await pa.evaluate(''' [window.Hub,KISSY.Env.mods["item-detail/promotion/index"].exports.get("promoData") ] ''')   
		if not sku or not sku[1]:
			sku=await pa.evaluate(''' window.Hub ''')
			sku.append(await pa.evaluate(''' KISSY.Env.mods["item-detail/promotion/index"].exports  ''') )
			
	except Exception as e:
		sku=e
	fd=F.dp(obj=sku,file=f[:-5])   
	if close:await pa.close()
	return pa,f,fd

async def get_current_buyertrade_json(page_or_url=None):
	tb=taobao_trade
	pa=await tb.get_or_new_page(page_or_url)
	h=await pa.evaluate("document.documentElement.outerHTML") 
	return T.json_loads( eval("'%s'"% T.sub(h,"JSON.parse('","');") ) )
	
async def get_current_dianpu_goods_list_tmall(url=None):
	return
async def get_current_dianpu_goods_list_taobao(page_or_url=None):
	tb=taobao_trade
	if not page_or_url:page_or_url="orderType=price_"
	pa=await tb.get_page(page_or_url)
	page_info=await pa.evaluate("document.querySelector('span.page-info').textContent")
	ds=await pa.evaluate('''
async function(){
	var ds=document.querySelectorAll('div[class*=shop-hesper-bd]  dl[class*=item]')	
	r=[]
	for(var i of ds){
		var u=i.querySelector('a[href*="item.taobao.com/item.htm"]').href
		var title=i.querySelector('a[class*="item-name"]').text.trim()
		var c_price=i.querySelector('[class="c-price"]').textContent.trim()
		var img=i.querySelector('img[src*="alicdn.com"]').src
		var sale=i.querySelector('[class="sale-area"]').textContent.trim() 
		var comment=i.querySelector('a[href*="on_comment=1"]').textContent
		r.push([u,title,c_price,img,sale,comment])
	}
	return r
}	
	''')
	return ds, page_info


def taobao_login(user,pw,user_input_xy=(1050, 383+9)):#incorrect tips + 9
	return U.simulate_system_actions([('for','淘宝网 - 淘！我喜欢'),user_input_xy,'ctrl+a','backspace',user,'tab',pw,'Enter']) 
login=taobao_login
	
async def buy_item_sku(id,sku):
	if py.isint(id):id=py.str(id)
	if '://' not in id:
		id='https://item.taobao.com/item.htm?id='+id.strip()
	tb=taobao_trade
	p=await tb.get_page(id)
	if not p:
		p=await tb.new_page(id)
	print(p)
	await p.evaluate(''' e=xpath("//span[contains(., '%s')] ") ; e.click() ''' % sku)
	print('click sku')
	await A.sleep(0.4)#sec
	await p.evaluate(''' e=xpath('//div[@class="tb-btn-buy"]/a');e.click() ''')
	print('click 立即购买')
	await A.sleep(1)#sec ,过早获取到
	
	p=await tb.get_page('https://buy.taobao.com/auction/buy_now.jhtml',wait=4)
	for i in range(9):
		await evaluate(p,''' document.querySelector('#submitOrderPC_1 > div.wrapper > a').style.backgroundColor='green' ''')
		green=await evaluate(p,''' document.querySelector('#submitOrderPC_1 > div.wrapper > a').style.backgroundColor ''')
		if green=='green':
			break
		await A.sleep(0.9)
		print('buy——btn not green',i,green)
		if i==8:return p
		
	print(green,U.stime())
	await p.evaluate(''' e= document.querySelector('#submitOrderPC_1 > div.wrapper > a') ;e.click() ''')
	# return p
	await A.sleep(3)#sec
	
	pa=await tb.get_page('https://cashierstm.alipay.com/standard',wait=9)#https://cashierstm.alipay.com/standard/lightpay/lightPayCashier.htm?orderId=  
	#https://cashierstm.alipay.com/standard/gateway/agentFeeEnoughPay.htm?orderId=
	
	return await alipay_buy(pa)
async def alipay_buy(pa,pw_file='130_pw.txt'):
	tb=taobao_trade
	from qgb import Win
	
	if not pa:return pa
	await pa.bringToFront()
	Win.set_foreground(title='支付宝 - 网上支付 安全快速！ - Cent Browser')
	# x,y=await tb.get_abs_xy(pa,'label[class=ui-label]')#(x+222,y+5)
	x,y=await tb.get_abs_xy(pa,'a[seed="sc_edit_forgetPwd"]')#(x-180,y+5)
	
	s,[x,y]=await tb.press_keys(pa,F.read(pw_file),xy= (x-160,y+5))
	await A.sleep(0.6)#sec
	Win.click(x,y+67)
	
	return pa
	

async def next_page_trade_list(page=0):
	if not page:page=await get_page()
	return await page.evaluate(taobao_trade.js_trade_list_next)
next=next_page_trade_list

async def add_cart(id,sku=py.No('click all')):
	'''  
await post('https://okfw.net/b=q.get_data();s=T.json_loads(b);r=len(s)',$0.innerHTML)
	'''
	tb=taobao_trade
	id=str(id)
	r=[]
	p=await tb.get_page(url=id)
	if not p:
		if '://' not in id:
			id='https://item.taobao.com/item.htm?id=%s'%id
		p=await tb.new_page(url=id)
	t=await p.title()
	r.append([U.stime(),p,[T.sub(p.url,'id=',''),t] , ])
	await p.bringToFront()
	if 'detail.tmall.com/item.htm' in p.url:
		await p.evaluate('''r=xpath('//a[contains(@id,"J_LinkBasket" )]');r.click();''')
		raise NotImplementedError()
	await page_scroll_bottom(p)
	top_add_cart_btn=await p.querySelector('a#J_TabShopCart')
	await top_add_cart_btn.click()# 页面初始加载必须先点击才会出现 popsku 
	popsku=await p.querySelector('div.tb-popsku' )
	async def check_popsku():
		style=await popsku.getProperty('style')
		display=await style.getProperty('display')
		value=await display.jsonValue()
		if 'none' in value:
			await top_add_cart_btn.click()
			await A.sleep(0.01)
			
	add=await p.querySelector('a.J_PopSKUAddCart')
	cancel=await p.querySelector('a.J_PopSKUCancer')
	
	try:await cancel.click()
	except:pass
	
	props=await p.querySelectorAll('.J_PopSKUProps>.J_Prop ')
	if len(props)>1: #TODO
		U.beep()
		await A.sleep(3)
		U.beep()
		await A.sleep(6)
		return r,len(props)
		
	
	
	ses=await p.querySelectorAll('.J_PopSKUProps > dl.J_Prop > dd > ul > li > a > span')
	for se in ses:
		await check_popsku()
		t=await (await se.getProperty('textContent')).jsonValue()
		for s in sku:
			if t in s:
				break
		else:
			if sku:# 指定了sku，但是没有找到（not break）
				continue
		await se.click()
		await A.sleep(0.1)
		await add.click()
		await A.sleep(1)
		r.append(t)
		
	return r

async def is_trade_list_loading(page=0):
	if not page:page=await get_page(url=URL_TRADE_LIST)
	r= await page.evaluate(''' 
 xpath('//div[contains(@class,"loading-mod__hidden")]')

	''')
	return r==None

async def get_curent_page_trade_id_wu(page=0):
	if not page:page=await get_page()
	return await page.evaluate(taobao_trade.js_trade_list_id_wu)

async def get_curent_page_trade_list(page=0):
	if not page:page=await get_page()

	# user,max=await page.evaluate(taobao_trade.js_um)
	return await page.evaluate(taobao_trade.js_trade_list)
# get_list=get_page_list=get_curent_page_trade_list


async def iter_wuliu_json(ids):
	p=await taobao_trade.get_page(url=taobao_trade.URL_WULIU_BY_TRADE_ID)
	# id_wu=await taobao_trade.get_curent_page_trade_id_wu()
	print(p,p.url,len(ids))
	from qgb import A
	for id,w in ids:
		U.p(U.ct(ids),id)
		if not w:
			print(' ### No Wuliu')
			continue
		url=taobao_trade.URL_WULIU_BY_TRADE_ID+id
		fn='C:/test/buyertrade/'+T.filename(url)
		if F.exist(fn):
			print(' ## exist ##',fn[-28:])
			continue
		await p.goto(url)
		s=await p.content()
		f=F.write(fn,s)
		print(f[-38:])
		await A.sleep(U.get('asleep',0.9))

async def iter_wuliu_detail(us=0):
	if not us:
		# sync_get_user=sync_get_user=U.get('sync_get_user')
		# try:
		# 	user=sync_get_user() #  RuntimeError: This event loop is already running
		# except:
			# py.pdb()

		user=await get_user()
		assert user
		fs=[]
		for f in F.ls(U.gst,r=0):
			if 'trade_list' in f and user in f:
				fs.append(f)
		assert len(fs)>0
		us=F.dill_load(fs[-1])

	page=await get_page()
	ls=F.ls(U.gst+__name__)
	for u in us:
		row=u
		if py.islist(u):
			u=u[-1]

		if not u:
			print(row)
			continue
		f=U.gst+__name__+'/'+T.fileName(u)
		if f in ls:
			print('#skip',u)
			continue

		await page.goto(u)
		await asyncio.sleep(U.randomInt(9,66)) 
		# await asyncio.sleep(1)
		s=await page.content()
		f=F.write(f,s,mkdir=1)
		print(f,U.stime())
wuliu_detail=iter_wuliu_detail	
	
		
js_check_automation = js_detect_automation = JS_CHECK_AUTOMATION = JS_DETECT_AUTOMATION = """
 navigator.webdriver  
 
 """
JS_QGB=F.read(U.get_qpsu_file_path('chromExt/qgb.js') )	
QGB_JS_FUNCTION_LIST=['post', 'rpc_sleep', 'xpath', 'xpath_all']
JS_ONLOAD='''
() => {
	if(navigator.webdriver){
		Object.defineProperty(navigator, 'webdriver', {
			get: () => undefined
		})	
	}
		
%s

	window.post=post
	window.rpc_sleep=rpc_sleep
	window.xpath=xpath
	window.xpath_all=xpath_all
}
''' % '\n\n'.join(T.get_javascript_function(JS_QGB,k) for k in QGB_JS_FUNCTION_LIST)
# {k: for k in QGB_JS_FUNCTION_LIST }

JS_GET_USER=js_get_user='''async function js_get_user(){
	var user=''
	var euser=xpath("//a[contains(@class, 'login-info-nick')]")
	if(euser){ user=euser.textContent }
	return user
}'''

async def get_umn(page=0):
	if not page:page=get_page()
	return await (await taobao_trade.get_page()).evaluate(taobao_trade.JS_UMN)
# 直接 await page.evaluate(taobao_trade.JS_UM) 就可以，js中只要定义不用再调用
JS_UMN=JS_UM=js_trade_list_info=js_um='''async function get_um(){
	var user=''
	var max=0
	var n=0
	var euser=xpath("//a[contains(@class, 'login-info-nick')]")
	if(euser){ user=euser.textContent }
	var emax=xpath('//li[@title="下一页"]/preceding-sibling::li[1]')
	if(emax){  max=Number.parseInt(emax.textContent)  }
	var en=xpath_all("//li[contains(@class, 'active')]")[0]
	var n=Number.parseInt(en.textContent)    
	return [user,max,n]
}'''
js_trade_list='''async function js_trade_list(){
	var user=xpath('//a[@class="site-nav-login-info-nick "]').textContent
	var emax=xpath('//li[@title="下一页"]/preceding-sibling::li[1]')
	var max=Number.parseInt(emax.textContent) 

	var es=xpath_all("//table[contains(., '订单号')]")
	var ts=Array.from(es).map(i=> i.innerHTML)
	   
	var en=xpath_all("//li[contains(@class, 'active')]")[0]
	var n=Number.parseInt(en.textContent)    
	
	var r=await post("https://okfw.net/r=taobao_trade.write(request)",
		{user:user,max:max, n:n,ts:ts, } )
	
	console.log(ts.length,n,r)
	return r
}'''

js_trade_list_id_wu='''async function js_trade_list(){
	var user=xpath('//a[@class="site-nav-login-info-nick "]').textContent
	var emax=xpath('//li[@title="下一页"]/preceding-sibling::li[1]')
	var max=Number.parseInt(emax.textContent) 

	var en=xpath_all("//li[contains(@class, 'active')]")[0]
	var n=Number.parseInt(en.textContent)    

	var es=xpath_all("//table[contains(., '订单号')]")
	var r=[]
	for(var n in es){
		var i=es[n]
		// function xpath
		var id=xpath("//span[contains(., '订单号')]/following-sibling::span[1+1]",i).innerText
		var e=xpath("//a[contains(., '查看物流')]",i)
		var w=''
		if(e){
			w=e.href
		}
		r.push([id,w])
	}
	//return Array.from(es).map(i => i.innerHTML)
	return r

	// await post("https://okfw.net/r=taobao_trade.write(request)",{html:})
	//var ts=Array.from(es).map(i => i.innerHTML)
	return ts[0]
	var r=await post("https://okfw.net/r=taobao_trade.write(request)",
		{user:user,max:max, n:n,ts:ts, } )
	
	console.log(ts.length,n,r)
	return r
}'''

js_trade_list_id_tk='''async function js_trade_list_tk(){
	var es=xpath_all("//table[contains(., '订单号')]")
	var r=[]
	for(var n in es){
		var i=es[n]
		var id=xpath("//span[contains(., '订单号')]/following-sibling::span[1+1]",i).innerText
		tks=[]
		for(var j of i.querySelectorAll('tbody>tr')
					){
					
			var tk=xpath("//a[contains(@href, 'refund2.taobao.com/dispute/applyRouter.htm')]",j)
			//tks.push([tk.href,tk.outerHTML])
			tks.push([j+'',tk+''])
			
		}
		r.push([id,tks])
	}
	return r

}'''

def parse_row(h,parse_wuliu_detail_file=False):
	et=T.xpath(h,'//span[contains(@class,"create-time")]')[0] #
	date=et.text
	id=T.sub(et.get('data-reactid'),'$order-','.$')
	
	es=T.xpath(h,'//a[contains(@class,"seller-mod")]')[0]  #seller
	sname=es.text
	surl=es.get('href')
	
	ww=T.xpath(h,'//a[@class="ww-inline ww-online"]')[0].get('href')   
	
	ep=T.xpath(h,'//div[contains(@class,"suborder-mod")]')[0]  #
	purl=ep.xpath('//a[contains(@class,"production-mod__pic")]')[0].get('href')  
	img=ep.xpath('//img')[0].get('src')  
	
	ept=ep.xpath('//div[@style="margin-left:90px;"]')[0]  #
	title=ept.xpath('//span[@style="line-height:16px;"]')[0].text
	snap=ept.xpath('//a[contains(., "交易快照")]')
	if not snap:
		# raise Exception(id,'snap')  # 话费充值订单没有 快照
		snap=py.No('snap',h)
	else:
		snap=snap[0].get('href')
	
	ew=T.xpath(h,"//a[contains(., '查看物流')]")
	if len(ew)!=1:
		t=T.html2text(h)
		t=T.replace_all_space(t)[:99]
		wuliu=py.No('查看物流',t,h)
	else:
		ew=ew[0]
		wuliu=ew.attrib['href']
		# u=convert_wuliu_url( e.attrib['href'])

	esku=T.xpath(h,'//p/span[contains(@class,"production-mod__sku-item")]/parent::p')
	sku=[]
	if esku:
		#一个订单可能有多个商品，多个sku，所以 不能 #assert len(esku)==1
		for esku_i in esku:
			sku_i=[]
			for ei in esku_i.xpath('span'):
				hei=T.xpath_element_to_str(ei)
				ei_text=T.html2text(hei).strip()
				if ei_text:
					sku_i.append(ei_text)
				else:
					py.pdb()
					t=T.html2text(h).strip()
					print(id,t[:66])
					# U.set(id,T.xpath_element_to_str(h))
					continue
					(T.justify(title,44,cut=1),T.justify(t,47,cut=1,method='rjust'),)
					# data=[id,date, sname,surl,ww,  purl,img, title,snap, wuliu,sku,,sku_i,esku,esku_i,ei]
					raise Exception(data)
			if sku_i:
				sku.append(tuple(sku_i))
	
	ep=T.xpath(h,'//div[contains(@class,"price-mod__price")]/p/span/parent::*')[0]
	price=T.html2text(T.xpath_element_to_str(ep)).strip()
	esp=T.xpath(h,'//div[contains(@class,"price-mod__price")]/p/strong/span/parent::*')[0]
	sprice=T.html2text(T.xpath_element_to_str(esp)).strip()

	ew=T.xpath(h,"//span[contains(., '(含运费：')]/parent::*")
	if ew:
		assert len(ew)==1
		wprice=T.html2text(T.xpath_element_to_str(ew[0])).strip()
	else:
		wprice=py.No('含运费',id,h)
	if parse_wuliu_detail_file:
		winfo=taobao_trade.parse_wuliu_detail_file(wuliu)
	else:
		winfo=py.No('不需要物流详情')
	return id,date, sname,surl,ww,  purl,img, title,snap, wuliu,sku, [price,sprice,wprice],winfo

def parse_wuliu_detail_file(url):
	winfo=[]
	# if wuliu:
	wu=convert_wuliu_url(url)
	s=read_html_by_url(wu)
	e=T.xpath(s,'//ul[@id="J_listtext1"]') 
	# status_list=[]
	# wc=wid=wtel=''
	if e:
		status_list=[i for i in e[0].xpath('li/child::*/text()') ]
		e=T.xpath(s,'//div[@class="info"]') 
		assert len(e)==1
		e=e[0]
		ew=e.xpath('//label[contains(.,"物流公司：")]/following-sibling::span[1]')
		if ew: # 包裹1 包裹2 包裹3
			wc=ew[0].text.strip()
			wid=e.xpath('//label[contains(.,"运单号码：")]/following-sibling::span[1]')[0].text.strip()
			
			wtel=''
			ew=e.xpath('//label[contains(.,"客服电话：")]/following-sibling::span[1]')
			if ew: # 
				wtel=ew[0].text.strip()
				
			wsname=e.xpath('//label[contains(.,"卖家昵称：")]/following-sibling::span[1]')[0].text.strip()
			ea= e.xpath('//label[contains(.,"发货地址")]/following-sibling::*')[0]
			waddress= T.html2text(T.xpath_element_to_str(ea))
			
			ea= e.xpath('//label[contains(.,"收货地址")]/following-sibling::*')[0]
			myaddress= T.html2text(T.xpath_element_to_str(ea))

			wid=U.StrRepr(wid)
			wid.wlxq=wid.xq=wid.list=wid.status=wid.status_list=status_list
		
			ea= T.xpath(s,'//div[@class="cainiao-content"]')
			if ea:
				# ea= e.xpath('//p[contains(.,"取货密码")]/following-sibling::*')
				pw=T.html2text(T.xpath_element_to_str(ea[0]))
				pw=T.sub(pw,'取货密码：','\n')
				# if not pw:
				assert pw
				myaddress+='取件码'+pw
	
			winfo=[wc,wid,myaddress,waddress,wsname,wtel,T.join(status_list[-8:],split='  \n')]
	return winfo	
	
	
def file_md5s():
	md5s=U.get_or_set('md5s',set())
	for f in F.ls(r'C:\test\taobao_trade'):
	#    b=F.read_byte(f)
		m=U.md5(file=f)
		md5s.add(m)
	print(len(md5s))
	return md5s
	
def write(q):
	if py.isbytes(q):
		b=q
	else:
		b=q.get_data()
	if not b:return py.No(b,U.dir(q))
	f='taobao_trade/'+T.fileName( b[:55].decode('utf-8') )
	
	md5s=U.get('md5s')
	if not md5s:
		md5s=U.set('md5s',file_md5s())

	m=U.md5(b)
	if m in md5s:
		U.msgbox(f,m+' duplicated in md5s')
		return py.No('duplicated md5 '+m,m,f)	
	md5s.add(m)
	return F.write(f,b,mkdir=1)

def read_file_by_url(url):
	f='C:/test/qgb.tests.taobao_trade/'+T.fileName(url)
	s=F.read(f,encoding='utf-8')
	if not s:
		return py.No(url+' Not Found!',s)
	r= U.StrRepr(s,repr=f'<U.StrRepr {F.ssize(len(s))} {f}  >') # |{s[:44]}...
	r.f=r.file=f
	return r
get_html_by_url=read_html_by_url=read_file_by_url

FILTER_WULIU_TEXT='''您已在
，感谢使用菜鸟驿站，期待再次为您服务。
您的快件已
 您的快递已经妥投。风里来雨里去, 只为客官您满意。上有老下有小, 赏个好评好不好？【请在评价快递员处帮忙点亮五颗星星哦~】
举手之劳勿忘送件人，请在【评价快递员】处赐予我们五星好评~
商铺店菜鸟驿站
如有疑问请联系
。疫情期间顺丰每日对网点消毒、小哥每日测温、配戴口罩，感谢您使用顺丰，期待再次为您服务。
。起早摸黑不停忙，如有不妥您见谅，好评激励我向上，求个五星暖心房。
客官，您的包裹已安全送达，风里来雨里去，送个快递不容易，请动动您发财的小手，戳开快递员评价帮忙点亮五颗小星星，愿您的生活如五颗星一般闪亮如意
及时领取。
。如有疑问请电联：13337376037, 投诉电话：0731-89560765
快件已送达，：18521860158，投诉电话：0731-83398168。
,:18556274583,如您未收到此快递，请拨打投诉电话：0527-83605969! 
正在派件（95720为中通快递员外呼专属号码，请放心接听）
疫情期间不停歇，只为快件早送达。客官对吾若满意，好评点个5星呦！【请在评价快递员处帮忙点亮五颗小星星】百世快递祝福您：身体康健，百世顺心
，请如有疑问请电联：13337376037, 投诉电话：0731-89560765
，风里雨里小哥不易，贴心服务火速送达，五星好评盼您点赞！
,风里来，雨里去，汗也撒泪也流，申通小哥一刻不停留。不求服务惊天下，但求好评动我心，给个好评呗！！
。疫情期间不停歇，只为快件早送达。客官对吾若满意，好评点个5星呦！【请在评价快递员处帮忙点亮五颗小星星】百世快递祝福您：身体康健，百“世”顺心
 ，快件已消毒，小哥体温正常，将佩戴口罩为您派送，您也可联系小哥将快件放置指定代收点或快递柜，祝您身体健康【95114/95121/95013/95546为韵达快递员外呼专属号码，请放心接听】
 分部进行
 】在湖南长沙
 。 185211号段上海号码为圆通业务员专属号码
 185211号段上海号码为圆通业务员专属号码
 签收】。。有问题请联系【18279937959】
,顺丰已开启“安全呼叫”保护您的电话隐私,请放心接听！）
，地址：好家园十栋沁甜水果店
 手机号:17708443546。 185211号段上海号码为圆通业务员专属号码
在湖南长沙观沙岭公司
请在20点前取件。有问题请联系百世邻里
分部进行派件扫描  快递员 
客户签收：已签收。快件已从【新泉乡麻田街
,如有疑问请电联：13337376037, 投诉电话：0731-89560765
，如有问题请电联快递员：段伟【19848000881】，投诉电话：0731-89593132,
，如有问题请电联快递员：段伟【19848000881】，投诉电话：0731-89593132
。 快件已送达，：18521188786，投诉电话：0319-5125000。
。 快件已送达，：18032995716，投诉电话：0319-5125000。
】，如有任何疑问，请联系【15574972878】/
】，期待再次为您服务。
快件已送达，：18907490644，投诉电话：0731-88918099。
如有问题请电联快递员：
，投诉电话：0731-89593132
, 投诉电话：0731-89560765,
。 快件已送达，：17377874879，投诉电话：0731-83398168。
,如您未收到此快递，请拨打投诉电话：0769-33555666! 
，：17708443546，投诉电话：0731-88918099。
，请拨打投诉电话：021-31181333! 
，18279937959(共配站客服电话)
小哥今日体温正常，将佩戴口罩为您配送，也可联系小哥将包裹放置指定地点，祝您身体健康。
，联系电话：18170720533
，：13218828100，投诉电话：0514-85209999。
【快递超市的沁甜水果快递超市】

'''
def filter_wuliu_text(w):
	r=T.replacey(w,
FILTER_WULIU_TEXT.splitlines(),'')
	return r
wuliu_text_filter=filter_wuliu_text

def convert_wuliu_url(u):
	if '／／' in u:return u
	tid,uid=T.get_url_args(u,'trade_id','seller_id')
	u='https://detail.i56.taobao.com/trace/trace_detail.htm?tId={}&userId={}'.format(tid,uid)
	return U.StrRepr(u)
	
def iter_file_user_trade_list(user=0):
	if not user:
		from syncer import sync
		sync_get_user=U.get_or_set('sync_get_user',sync(taobao_trade.get_user) )

		user=sync_get_user()
		print('sync_get_user :',user)
	
	v=[]
	for f in F.ls(r'C:\test\taobao_trade'):
		if user not in f:
			continue
		b=F.read_byte(f)
		d=T.json_loads(b)
		assert d['user']==user

		for n,t in enumerate(d['ts']):
			e=T.xpath(t,"//a[contains(., '查看物流')]")
			if len(e)!=1:
				t=T.html2text(t)
				t=T.replace_all_space(t)[:99]
				u=py.No(t)
			else:
				e=e[0]
				u=convert_wuliu_url( e.attrib['href'])
			

			row=[d['user'],d['n'],n,u]
			v.append(row)	
	if not v:
		return py.No('can not found user: %s trade_list' % user)
	U.set(user,v)
	return F.dill_dump(obj=v,file=f'{user}-{len(v)}-trade_list')
get_trade_list=get_trade_list_by_user=get_user_trade_list=get_file_user_trade_list=iter_file_user_trade_list
	
js_trade_list_next='''async function js_trade_list_next(){
	var next=xpath('//li[@title="上一页"]')
	if(next){
		next.click()	
		return next.getAttribute('class')
	}else{
		return '### not found next'
	}
}'''
	

		
JS_='''
async function main(){
	user=xpath('//a[@class="site-nav-login-info-nick "]').textContent
	emax=xpath('//li[@title="下一页"]/preceding-sibling::li[1]')
	max=Number.parseInt(emax.textContent) 
	n=0
	while(n!=1){
		es=xpath_all("//table[contains(., '订单号')]")
		ts=Array.from(es).map(i=> i.innerHTML)
		   
		en=xpath_all("//li[contains(@class, 'active')]")[0]
		n=Number.parseInt(en.textContent)    
		
		r=await post("https://okfw.net/b=q.get_data();r=F.write('taobao_trade/'+U.stime()+T.fileName( b[:55].decode('utf-8') ),b,mkdir=1)",
			{ user:user,max:max,n:n,ts:ts, } )
		
		console.log(user,n,r)
		  
		next=xpath('//li[@title="上一页"]')
		next.click()

		await rpc_sleep('1+U.randomInt(0,9)/10')

		en=xpath_all("//li[contains(@class, 'active')]")[0]
		n1=Number.parseInt(en.textContent)    
		if(n===n1){
			break;
		}

	}

  
	console.log('done')
   // await rpc_sleep()
	
}

main()
'''

