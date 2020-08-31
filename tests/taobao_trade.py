import asyncio
import pyppeteer

from qgb import py
U,T,N,F=py.importUTNF()

taobao_trade=U.getMod(__name__)

us=zu=F.dill_load('C:/test/zu-67.dill')  

async def backup_cookie(user=0,page=py.No('auto last -1')):
	if not user:
		user=await page.evaluate(taobao_trade.js_get_user)
	if not page:page=await get_page()
	ck=await get_all_cookies(page)
	print('get_all_cookies len:',len(ck))
	await page.deleteCookie(*ck)
	print('deleteCookie','done !')

	return F.dill_dump(obj=ck,file=f'{user}-{len(ck)}-cookies') 

async def get_all_cookies(page=py.No('auto last -1')):
	if not page:page=await get_page()
	r=await page._client.send('Network.getAllCookies')  
	return r['cookies']
	
async def del_cookies(ck,page=py.No('auto last -1')):
	if not page:page=await get_page()
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

async def get_user(page=None):
	if not page:page=await get_page()
	return await page.evaluate(taobao_trade.js_get_user)


uk='pyppeteer.connect'
browser=U.get(uk)
async def get_page(page=None,url=py.No(URL_TRADE_LIST)):
	global browser,JS_ONLOAD
	if py.istr(page) and ('://' in page) and not url:
		url,page=page,None

	if not url:url=URL_TRADE_LIST
	if not page:
		if not browser:
			browser=U.set( 
				uk,await pyppeteer.connect(browserURL='http://127.0.0.1:9222')
				)
		for n,detected,page,u in (await set_pages_onload()):
			if u.startswith(url):
				break
		else:
			return py.No('can not found page url.startswith:'+url)
		# page=pages[-1]
	U.set('page',page)
	return page
		
	
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
			T.justify(page.url,size=80,cut=1), 
		]
		r.append(row)
	return r

async def set_pages_onload(pages=None,viewport=1):
	if not pages:
		pages = await browser.pages()
	for page in pages:
		try:
			if await page.evaluate(JS_DETECT_AUTOMATION) :
				await page.evaluateOnNewDocument(JS_ONLOAD)
				await page.evaluate(JS_ONLOAD)
				# await page.reload() # 刷新才生效
				if viewport:
					await page.setViewport({'width':1340,'height':670})
		except Exception as e:
			print(e)
	return await get_pages_onload(pages=pages)
async def next_page_trade_list(page=0):
	if not page:page=await get_page()
	return await page.evaluate(taobao_trade.js_trade_list_next)
next=next_page_trade_list

async def is_trade_list_loading(page=0):
	if not page:page=await get_page(url=URL_TRADE_LIST)
	r= await page.evaluate(''' 
 xpath('//div[contains(@class,"loading-mod__hidden")]')

	''')
	return r==None


URL_WULIU_BY_TRADE_ID='https://buyertrade.taobao.com/trade/json/transit_step.do?bizOrderId='
URL_TRADE_LIST='https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
async def get_curent_page_trade_id_wu(page=0):
	if not page:page=await get_page()
	return await page.evaluate(taobao_trade.js_trade_list_id_wu)

async def get_curent_page_trade_list(page=0):
	if not page:page=await get_page()

	# user,max=await page.evaluate(taobao_trade.js_um)
	return await page.evaluate(taobao_trade.js_trade_list)
get_list=get_page_list=get_curent_page_trade_list


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
	Object.defineProperty(navigator, 'webdriver', {
		get: () => undefined
	})
		
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
。如有疑问请电联：13337376037, 投诉电话：0731-89560765,
快件已送达，：18521860158，投诉电话：0731-83398168。
,:18556274583,如您未收到此快递，请拨打投诉电话：0527-83605969! 
正在派件（95720为中通快递员外呼专属号码，请放心接听）
疫情期间不停歇，只为快件早送达。客官对吾若满意，好评点个5星呦！【请在评价快递员处帮忙点亮五颗小星星】百世快递祝福您：身体康健，百世顺心
，请如有疑问请电联：13337376037, 投诉电话：0731-89560765
，风里雨里小哥不易，贴心服务火速送达，五星好评盼您点赞！
,风里来，雨里去，汗也撒泪也流，申通小哥一刻不停留。不求服务惊天下，但求好评动我心，给个好评呗！！
。疫情期间不停歇，只为快件早送达。客官对吾若满意，好评点个5星呦！【请在评价快递员处帮忙点亮五颗小星星】百世快递祝福您：身体康健，百“世”顺心

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