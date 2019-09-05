#! -*- encoding:utf-8 -*-
import requests

# 要访问的目标页面
targetUrl = "http://www.baidu.com"
targetUrl = "https://myip.ipip.net"
# targetUrl = "http://220.248.171.195:30000/%23rpc%0ar=q.META['REMOTE_ADDR']"
# targetUrl = "http://220.248.171.195:5000/%23qgb%0a:23571/r=request.remote_addr"
# 代理服务器
proxyHost = b'\xf1\xf1\xf6K\xf1\xf6\xf1K\xf2\xf5\xf5K\xf5'.decode('cp424')
proxyPort = "33128"

# 代理隧道验证信息
proxyUser = "qqq"
proxyPass = "wxb123456"

#proxyMeta = "http://%(host)s:%(port)s" % {
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
  "user" : proxyUser,
  "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)#

print(resp.status_code)
print(resp.text)