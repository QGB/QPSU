import sys
if __name__.endswith('qgb.N.Backend.taobao_list'):from ... import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()
gdshop_dui=gtb_list=U.set(__name__,  U.get(__name__,{})  )
gn=__name__+'.'
get_set=lambda a,default='':U.set(gn+a,  U.get(gn+a,default)  )
gshop=get_set('shop','')

grows=get_set('rows',[])
# g=get_set('')

from urllib.parse import parse_qs

def init(shop):
	global gshop
	shop=shop.lower()
	if '.taobao.com' in shop:
		shop=T.netloc(shop).replace('.taobao.com','')
	gshop=U.set(gn+'shop',shop)
	if shop not in gtb_list:
		gtb_list[gshop]={}
	return gshop

gdu_pageNo_null=get_set('pageNo_null',{})
def recycle_pageNo_null_url():
	for shop,dui in gdshop_dui.items():
		for u in list(dui):
			if 'pageNo=' not in u:
				gdu_pageNo_null[u]=dui.pop(u)
				U.pln('recycled:',shop,u)
remove_pageNo_null_url=pop_pageNo_null_url=recycle_pageNo_null_url

def pop_item_url_from_id_list(a):
	if not a:return ''
	id=''
	if py.isdict(a):
		id,v=a.popitem()
	if py.islist(a):
		id=a.pop() #-1
	if py.islist(id):
		id=id[-3]
	if not id:return ''
	if 'id=' not in id:
		return 'https://item.taobao.com/item.htm?id='+id
	else:
		return 'https://item.taobao.com/item.htm?id='+T.sub(id,'id=','')
get_item_url=pop_item_url=pop_item_url_from_id_list

def pop_url_from_shop(url,shop=None):
	if not shop:shop=gshop
	

def insert(request):
	''' [href,items,new Date(),  ,...]
	'''
	href,items,*_ = T.json_loads(request.get_data())
	gtb_list[gshop][href]=items
	return len(gtb_list[gshop] )
	
def include(u):
	getn=lambda url:parse_qs(url).get('pageNo',[0])[0]
	n=getn(u)
	for url in gtb_list[gshop]:
		if n==getn(url):
			return True
	return False
	
def max_num():
	mi=[1]
	for url in gtb_list[gshop]:
		if 'pageNo=' not in url:
			U.beep()
			U.pln(gshop,'no pageNo:',url)
			continue
		si=parse_qs(url).get('pageNo')[0]
		si=T.match_int(si) # avoid ValueError: invalid literal for int() with base 10: '56#anchor'
		if not si:
			U.log('no pageNo in :',gshop,url,si,parse_qs(url))
			continue
		i=int(si[0] )
		mi.append(i)
	return max(mi)

def iter_items(shop=None):
	if not shop:shop=gshop
	for url in py.list(gtb_list[shop]):
		page=gtb_list[shop][url]
		yield from page


def iter_sprice(shop=None):
	if not shop:shop=gshop
	for i in iter_items(shop):
		if('class="s-price"' in i):
			yield i
			
def rty(rows=None,**ka):
	if not rows:rows=grows
	rt=''

	dcol_range={}
	for k in py.list(ka):
		for nc,c in py.enumerate(k):
			if c in T._09:
				i=py.int(c)
				v=ka.pop(k)
				if py.isnum(v):
					dcol_range[i]=[v,U.IMAX]
				elif py.istr(v):
					if k[nc-1]=='_':
						dcol_range[-i]=v
					else:
						dcol_range[i]=v
				elif py.len(v)==2:
					dcol_range[i]=v
				else:
					raise py.ArgumentError(' col range must int or [a,b] ')
				break
	if dcol_range:
		print(' dcol_range:', dcol_range)
	for index,row in enumerate(U.sort(rows,**ka)):
		_continue=0
		for ic,ran in dcol_range.items():
				# rt+=f'#  {row}[{ic}]<hr>'
				# _continue=0
			if ic>=0 and py.istr(row[ic]) and py.istr(ran):
				if not ran in row[ic]:
					_continue=1
			if ic<0 and py.istr(row[ic]) and py.istr(ran):
				if ran in row[ic]:
					_continue=1
			if py.isnum(row[ic]) and py.isnum(ran[0]):
				if not ran[0]<=row[ic]<=ran[1]:
					_continue=1
		if _continue:continue

		if 'item.taobao.com/item.htm?id=' in row[-3]:
			row[-3]=T.sub(row[-3],'id=','')
		tb=f'''{row[-1]}
<span>{row[:4]}</span>  <br>
<a target="_blank" href="taobao://item.taobao.com/item.htm?id={row[-3]}">{'%4s'%index}  {row[-2]} </a>
<br><hr>
'''
		rt+=tb
	return rt

def load(file):
	global grows

	grows=F.dill_load(file=file)
	shop=T.sub(file,'','-')
	if shop:
		file=shop
	return file,len(grows)

imgs=[];dis=[];ts=[];ds={}
def result(shop=None):
	global grows
	if not shop:shop=gshop
	if py.islist(shop):
		items=shop
		shop='TB.result-test-{}'.format(len(items))
	else:
		items=iter_items(shop) 
	rows=py.set()
	for html in U.progressbar( items ):
		bs = T.BeautifulSoup(html)
		a=bs.select('.item-name')[0]
		h=a.get('href')
# '//item.taobao.com/item.htm?spm=a1z10.3-c.w4002-21992529001.30.1887510dqsrC5C&id=597761481418'		
		if not h.startswith('//item.taobao.com/item.htm?') or 'id=' not in h:
			U.pln('not correct taobao item href',U.stime())
			py.pdb()
		id=T.get_url_arg(h,'id')
		cp=bs.select('[class=c-price]')[0]
		cp=float(cp.text)
		sp=bs.select('[class=s-price]')
		if sp:
			sp=sp[0]
			sp=float(sp.text)
		else:
			sp=cp
		img=bs.select('img')[0]
		row=[int((sp-cp)*100)/100,cp,sp, id, T.replacey(a.text.strip() ,['【优信电子】',],''),img ]
		row.insert(0,int( (row[0]/row[1])* 100 ) )
		row=tuple(row)
		rows.add(row)
	grows=rows
	return F.dill_dump(obj=rows,file='{}-{}'.format(shop,len(rows)))

def taobao_sku(d):
	'''item html : 
 Hub.config.set('sku', {
     valCartInfo      : {
         itemId : '355190223
         cartUrl: '//cart.ta
     },
     apiRelateMarket  : '//t
     apiAddCart       : '//c
     apiInsurance     : '',
     wholeSibUrl      : '//d
     areaLimit        : '',
     bigGroupUrl      : '',
     valPostFee       : '',
     coupon           : {
         couponApi         :
         couponWidgetDomain:
         cbUrl             :
     },
     valItemInfo      : { #这里开始 大概 1424 行
         
         defSelected: -1,
         skuMap     : {";162}
         ,propertyMemoMap: {...}
		}  # 这个 结束
	'''
	if py.istr(d):d=T.load_js_obj(d)
	m=d['propertyMemoMap']
	skuMap=d['skuMap']
	r=[]
	for i,name in m.items():
		row=[]
		pi=skuMap[ ';{};'.format(i) ] #  {'oversold': False, 'price': '1.80', 'skuId': '4451749127064', 'stock': '2'}
		row=[ U.FloatRepr(pi['price'],size=8) ,U.StrRepr(i,size=20),U.StrRepr(name) , ]
		if pi['oversold']:row.append('oversold')

		r.append(row)
	return r

def get_price_list_from_setMdskip(d):
	'''https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId=597606333219&showShopProm=true&isPurchaseMallPage=false&itemGmtModified=1586583685000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1586591444224&isg=dBNwXtilqQnbNHidBOfgSZlsvAbToIOb4sPP3hrRQICPO41H77k5WZXXqRTMCnGVH6YMR35fHFhYBeYBqMIKnxvOa6Fy_7kSndC..&isg2=BLq611-JsKSWiz8nzofghCAaC-Dcaz5FTP5lBsSyas0Jt1rxrPkTVYCOB0NrJ7bd
	'''
	r=[]
	d=d['defaultModel']
	d=d['itemPriceResultDO']
	p=d['priceInfo']
	for skuid,v in p.items():
		old=v['price']
		old=U.FloatRepr(old,size=9)
		
		pl=v.get('promotionList',[])
		if len(pl)==1:
			new=pl[0]['price']
			new=U.FloatRepr(new,size=9)
		else:
			new=py.No('promotionList.len != 1',skuid,pl)
		
		r.append([skuid,new,old])# 1 , 2 , 3 
		
	return r
tmall_sku=get_price=get_price_list=get_price_list_from_setMdskip

def get_price_num_list_from_setMdskip(d):
	return [i[1] for i in get_price_list_from_setMdskip(d)]
get_price_num=get_price_num_list_from_setMdskip

def count_money(y,max):
	y=U.sort(y)
	if y[0]>=max:return {y[0]:y[0]}
	d={}
	for i in y:

		for j in y:
			yield

cm=count_money		   

def iter_max_list(*a,**ka):
	all=iter_max(*a)
	r=[]
	for row in all:
		r.append((sum(row),row))
	return U.sort(r,**ka)

def iter_max(y,max,layer=0):
	if max==0:
		yield []  ;return
		
	if y[0]>=max: # 不能去掉，否则 RecursionError: maximum recursion depth exceeded in comparison
		yield y[:1]  ;return
	
	for n,i in enumerate(y):
		for j in iter_max(y,max-i,layer=layer+1):
			mr=sum(j,i) # sum(i,j) #TypeError: 'int' object is not iterable
			if mr>=max:
				yield [i, *j]
				# continue
		else:
			if i>=max:
				yield [i]
				return

def iter_max_(y,max,layer=0):
	y=U.sort(y)
	if y[0]>=max:
		# yield y[0]
		return y[:1]
		# return [y[0],{y[0]:1} ]
	else:
		loop_times=int( (max//y[0])+1  )
		# return loop_times

	result=[]
	# n=0
	# for n in range(1,loop_times+1):
	for n,i in enumerate(y):
		print('===',layer,n)
		try:
			r=[i, *iter_max(y,max-i,layer=layer+1) ]
			if sum(r) < max:
				return r
			else:
				raise Exception(r)
		except Exception as e:
			r=e.args[0]
			if layer==0:
				print(r)
			else:
				raise e



	return
	from itertools import product
	for r in product(y, repeat=loop_times):
		mr=sum(r)
		if mr < max:raise Exception('impossible!') 
		# yield r
		n+=1
	return n

gm=0
def rec(y,max,layer=0):
	global gm,gs
	# if y[0]>=max:
	# 	return y[:1]
		# yield y[:1]
		# return [y[0],{y[0]:1} ]
	# else:
	if layer==0:
		gm=int( (max//y[0])  - 1 ) 
		gs=set()

	if layer==gm:
		for i in y:
			yield [i]
			
		return
	
	for i in y:
		for j in rec(y,max,layer=layer+1):
			t= tuple( [i , *j ] )
			if t in gs:
				continue
			else:
				gs.add(t)
			# if tuple(set(t)) in gs:
				# continue
			yield t
		# 
def ec(*a,**ka):
	for i in TB.rec(*a,**ka):
		t





def permutations(arr, position=0,end=None):
	global gs,gt
	
	if end==None:
		end=len(arr)
		gs=set()
		gt=set()
	
	if position == end:
		t=tuple(arr)
		gt.add(t)
		gs.add(tuple(set(arr)))
 
	else:
		for index in range(position, end):
 
			arr[index], arr[position] = arr[position], arr[index]
			permutations(arr, position+1, end)
			arr[index], arr[position] = arr[position], arr[index]
 
	return U.len(gs,gt)
# arr = ["a","b","c"]
# permutations(arr, 0, len(arr))			

