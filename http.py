import os
import urllib2,urllib
#('mstsc')
print "qgb Http"
def getHtml(url):
	html=""
	try:
		response = urllib2.urlopen(url)
		html = response.read()
	except Exception as err:
		print(str(err)+"\n<"+url)
	return html



#os._exit(1)	
url = "http://www.zhihu.com/node/ProfileFolloweesListV2"

data='method=next&params=%7B%22offset%22%3A0%2C%22order_by%22%3A%22created%22%2C%22hash_id%22%3A%22dcddea61834f6b2dcb515f393fe29575%22%7D&_xsrf=e09da8ef48321e2367dda9562ac67105'
url=url+'?'+ data

req_header = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}
req_timeout = 5
req = urllib2.Request(url,None,req_header)
resp = urllib2.urlopen(req,None,req_timeout)
html = resp.read()
print(html)