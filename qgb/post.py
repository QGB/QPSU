import urllib
import urllib2

def post(url, data):
	d={'Host': 'static.zhihu.com',
'Proxy-Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Accept': 'image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
'Referer': 'http://static.zhihu.com/static/ver/aa583b24654a97650f25057ce42d7b62.z.css',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'cap_id="Yzk0NTk2ZDc0Y2I5NGRjOGIzMmFmNDRiODUxYzY1ODE=|1439547224|e094ef1af7d57f9195b8d7e51eced0ac65cc8420"; q_c1=175abda11382471884485792a9c80221|1439604224000|1436955147000; z_c0="QUFEQVdmWWNBQUFYQUFBQVlRSlZUYWt0QUZZRVpvVE51RUY4N2FySXhHeXV4ZDV4SmNoMVJ3PT0=|1440260265|151a99268035adfc673954ba77ba48e034906401"; _ga=GA1.2.1959321976.1437459462; __utma=51854390.1959321976.1437459462.1440503569.1440503569.1; __utmb=51854390.79.9.1440504654638; __utmc=51854390; __utmz=51854390.1440503569.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/34837425; __utmv=51854390.100-1|2=registration_date=20130809=1^3=entry_date=20130809=1'}

	req = urllib2.Request(url,None,d)
	#data = urllib.urlencode(data)
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req, data)
	return response.read()


posturl = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
data = 'method=next&params=%7B%22offset%22%3A1180%2C%22order_by%22%3A%22created%22%2C%22hash_id%22%3A%22dcddea61834f6b2dcb515f393fe29575%22%7D&_xsrf=e09da8ef48321e2367dda9562ac67105'
html=post(posturl, data)

html = unicode(html, "utf8").encode("utf8")
print html
#f=open('zu.html','w')
#f.write(html)



