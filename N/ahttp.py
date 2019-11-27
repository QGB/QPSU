#coding:utf-8
import asyncio,aiohttp
import aiohttp.connector
import sys;'qgb.U' in sys.modules or sys.path.append('/home/qgb/')
import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/')
from qgb import *
U.r(aiohttp.connector)

sub_domains=['www', 'mail', 'bbs', 'blog', 'demo', 'forum', 'dev', 'member', 'a', 'img', 'test', 'ftp', 'smtp', 'pop', 'm', 'webmail', 'pop3', 'imap', 'localhost', 'autodiscover', 'admin', 'mx', 'en', 'email', 'wap', 'oa', 'ns1', 'vpn', 'ns2', 'www2', 'mysql', 'webdisk', 'old', 'news', 'calendar', 'shop', 'potala', 'mobile', 'web', 'sip', 'mobilemail', 'game', 'product', 'gov', 'n', 'qq', 'r', 'v','123','z']


url = 'https://{}.baidu.com/'
async def hello(url,semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,timeout=5) as response:
                t= await response.read()
                h=dict(response.headers)
                # U.ipyEmbed()()
                return url,t,h
                # return len(t)

domains=F.dill_load('domains.dill')
async def run():
    semaphore = asyncio.Semaphore(5000) # 限制并发量为500
    # to_get = [hello(url.format(sub),semaphore) for sub in sub_domains] #总共1000任务
    to_get = [hello(u,semaphore) for u in domains] #总共1000任务
    taskset,set0=await asyncio.wait(to_get)

    r=[]
    re=[]
    for i in taskset:
        try:
            i=i.result()
            r.append(i)
        except Exception as e:
            re.append(e)
    # ur=U.unique(r)
    U.ipyEmbed()()
    # print(r)

    # print()
    # print(U.len(r,ur))

def main():
    U.log(U.stime())
    loop = asyncio.get_event_loop()
    U.log(U.stime())
    loop.run_until_complete(run())
    U.log(U.stime())
    loop.close()
    U.log(U.stime())

if __name__ == '__main__':
    main()