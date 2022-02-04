#coding=utf-8   
import sys,pathlib # *.py  /tests /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
# thread,server=N.rpcServer(port=2345,locals=globals())

'''
Refused to connect to 'https://qgb.net/h=T.js_load(q.get_data());r=len(h),U.stime()' 
because it violates the following Content Security Policy directive: "connect-src 'self' blob: https://*.giphy.com https://*.pscp.tv https://*.video.pscp.tv https://*.twimg.com https://api.twitter.com https://api-stream.twitter.com https://ads-api.twitter.com https://aa.twitter.com https://caps.twitter.com https://media.riffsy.com https://pay.twitter.com https://sentry.io https://ton.twitter.com https://twitter.com https://upload.twitter.com https://www.google-analytics.com https://accounts.google.com/gsi/status https://accounts.google.com/gsi/log https://app.link https://api2.branch.io https://bnc.lt wss://*.pscp.tv https://vmap.snappytv.com https://vmapstage.snappytv.com https://vmaprel.snappytv.com https://vmap.grabyo.com https://dhdsnappytv-vh.akamaihd.net https://pdhdsnappytv-vh.akamaihd.net https://mdhdsnappytv-vh.akamaihd.net https://mdhdsnappytv-vh.akamaihd.net https://mpdhdsnappytv-vh.akamaihd.net https://mmdhdsnappytv-vh.akamaihd.net https://mdhdsnappytv-vh.akamaihd.net https://mpdhdsnappytv-vh.akamaihd.net https://mmdhdsnappytv-vh.akamaihd.net https://dwo3ckksxlb0v.cloudfront.net ".

(anonymous) @ qgb.js:104
post @ qgb.js:97
(anonymous) @ VM554:1

'''