import hashlib
import base64
import requests
import pickle
import xlwt
import os
import re
import json
import random


class GsDataAPI:
    def __init__(self):
        self.app_key = 'b523947e120c8ee8a88cb278527ddb5a'
        self.app_secret = '1962972fee15606cd1ad1dc8080bb289'
        self.sort_map = {'1': 'posttime', '2': 'readnum', '3': 'likenum'}
        self.order_map = {'1': 'desc', '2': 'asc'}

        self.news_list = []

    def _gen_access_token(self, params, router):
        params_list = sorted(params.items(), key=lambda x: x[0])
        params_str = ''.join([''.join(params) for params in params_list])
        params_final = '%s_%s_%s' % (self.app_secret, params_str, self.app_secret)
        m = hashlib.md5()
        m.update(params_final.encode('utf-8'))
        sign = m.hexdigest()
        C = base64.b64encode(bytes(self.app_key+':'+sign+':'+router, encoding='utf-8'))
        return C

    def get_msg_info(self, **kwargs):
        '''
        参数	        类型	可空	默认	    描述	        示例
        wx_name	        String  YES	    ---	        微信号	        rmrbwx
        posttime_start	String	YES	    ---	        文章发布开始时间	2018-08-20 10:00:00
        posttime_end	String	YES	    ---	        文章发布结束时间	2018-09-07 06:00:00（不含）
        entertime_start	String	YES	    ---	        文章入库开始时间	2018-08-08 12:00:00
        entertime_end	String	YES	    ---	        文章入库结束时间	2018-08-20 22:00:00（不含）
        keywords	    String	YES	    ---	        检索词	        aaa+bbb,ccc,ddd+eee
        order	        String	YES	    desc	    排序方式	    desc
        sort	        String	YES	    posttime	排序字段	    posttime
        page	        Integer	YES	    1	        第几页	        1
        limit	        Integer	YES	    50	        每页显示条数	    20
        sn	            String	YES	    --	        sn	            aabbcc
        '''
        kwargs['limit'] = str(kwargs.get('limit', 50))
        if kwargs.get('posttime_start') is not None:
            kwargs['posttime_start'] += ' 00:00:00'
        if kwargs.get('posttime_end') is not None:
            kwargs['posttime_end'] += ' 24:00:00'

        sort_type = kwargs.get('sort')
        if sort_type in [None, 'posttime']:
            router = '/weixin/article/search1'
        elif sort_type == 'readnum':
            router = '/weixin/article/search2'
        elif sort_type == 'likenum':
            router = '/weixin/article/search3'
        else:
            return None

        params = kwargs
        self.news_list = []
        while True:
            url = 'http://databus.gsdata.cn:8888/api/service'
            C = self._gen_access_token(params, router)
            r = requests.get(url, headers={'access-token': C}, params=params)
            r_js = r.json()
            if not r_js['success']:
                print(r_js)
            data = r_js['data']
            num_found = data['numFound']
            pagination = data['pagination']
            page = pagination['page']
            if page == 1:
                print('总计%d篇文章' % num_found)
            self.news_list.extend(data['newsList'])
            news_list_len = len(self.news_list)
            print('已获取%d篇' % (news_list_len))
            if news_list_len >= num_found:
                break
            params['page'] = str(page + 1)

        # with open('test.pkl', 'wb') as f:
        #     pickle.dump(self.news_list, f)

    def save_as_excel(self, filename):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet0')
        header = ['标题', '摘要', '发布时间', '作者', '阅读数', '点赞数', '链接']
        for i, field in enumerate(header):
            ws.write(0, i, field)
        col_width = [10000, 10000, 5000, 5000, 5000, 5000, 20000]
        col_count = len(col_width)
        for i in range(col_count):
            ws.col(i).width = col_width[i]

        row = 1
        for news in self.news_list:
            ws.write(row, 0, news['news_title'])
            ws.write(row, 1, news['news_digest'])
            ws.write(row, 2, news['news_posttime'])
            ws.write(row, 3, news['news_author'])
            ws.write(row, 4, news['news_read_count'])
            ws.write(row, 5, news['news_like_count'])
            ws.write(row, 6, news['news_url'])
            row += 1

        wb.save(filename)


class IDataApi:
    def __init__(self):
        self.api_key = 'vYpznyAwychvW7ur6HMbUx08YgO81ZX2eFpLytUGRTHeitTSUIONsZLpps3O18aY'
        self.data_json = None

    def get_msg_info(self, **kwargs):
        url = "http://api01.idataapi.cn:8000/post/weixin?apikey=%s" % self.api_key
        params = kwargs
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "close"
        }

        if not os.path.exists('idata.pkl'):
            r = requests.get(url, headers=headers, params=params)
            self.data_json = r.json()
            if self.data_json['retcode'] == '000000':
                with open('idata.pkl', 'wb') as f:
                    pickle.dump(r.json(), f)
            else:
                print(self.data_json['message'])
                return
        else:
            with open('idata.pkl', 'rb') as f:
                self.data_json = pickle.load(f)

        data_list = self.data_json['data']
        has_next = self.data_json['hasNext']
        page_token = self.data_json['pageToken']
        print(has_next)
        print(page_token)
        print(len(data_list))
        for data in data_list:
            print(data['title'])
            print(data['url'])
            print('')


class WechatAPI:
    def __init__(self):
        self.url = 'https://mp.weixin.qq.com/mp/profile_ext'
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA5NDc1NzQ4MA==&scene=124&uin=MTMxOTI3Mjc1&key=18296be7e87fa916d06e197d2c416373765f9d9507fb1be1ca58b7278b74ab20427f8abc1b76922d43a42c46fe052bc4e7e6cd1a8e8613615ef660c888a2fb12f463a593d439a46d1a7360fa075108b4&devicetype=Windows+7&version=62060833&lang=zh_CN&a8scene=7&pass_ticket=P12nGbyGYqcxMn8TPtsskVbRJo%2BH9Rojj4I0SNfyL9I%3D&winzoom=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
            'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=131927275; devicetype=Windows7; version=62060833; lang=zh_CN; pass_ticket=P12nGbyGYqcxMn8TPtsskVbRJo+H9Rojj4I0SNfyL9I=; wap_sid2=COuZ9D4SXGhFWm10djluQ2NCT0d5SHIwMDB1RzBzZ09MNXhnUzhQanBndFB6TDdfTlNzajU1enllMG91cnBvV29FVkxUbXZxVG9janhtcmxZNUNUMTRGRnlCN2dfNERBQUF+MN6i2OoFOA1AlU4=',
        }
        with open('cookie.txt', 'r') as f:
            cookie = f.read()
        self.cookies = json.loads(cookie)

    def get_token(self):
        url = 'https://mp.weixin.qq.com'
        response = requests.get(url=url, cookies=self.cookies, verify=False)
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        print('token:', token)
        return token

    def get_fakeid(self, mp_id, token):
        header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
        query = mp_id
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=self.cookies, headers=header, params=query_id, verify=False)
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')
        print(search_response.json())
        print('fakeid:', fakeid)
        return fakeid

    def get_msg(self, fakeid):
        params = {
            'action': 'getmsg',
            '__biz': fakeid,
            'f': 'json',
            'offset': 10,
            'count': 10,
            'is_ok': 1,
            'scene': 124,
            'uin': 'MTMxOTI3Mjc1',
            'key': '05eee5e78663c69d88f47c0818a8666d07f12fc80c52ca172928d0d2f7f0bc59ec7fd19cd4b4d4aed825422af5fb0533cefb3abd47cad1705843f61422a0a9ba9e70c3dd8afc9d75ce3d8f50d26b69e7',
            'pass_ticket': 'P12nGbyGYqcxMn8TPtsskVbRJo%2BH9Rojj4I0SNfyL9I%3D',
            'wxtoken': '',
            'appmsg_token': '1022_MIIE0%2BkZ3ICFd%2FeOj_GH9X3jzWdqoH8RvZkHnA~~',
            'x5': 0,
            'f': 'json'
        }
        i = 0
        while True:
            # r = requests.get(self.url, headers=self.headers, params=params, verify=False)
            r = requests.get(self.url, params=params, verify=False)
            r_json = r.json()
            if r_json['errmsg'] == 'ok':
                msg_list = eval(r_json['general_msg_list'])['list']
                for msg in msg_list:
                    try:
                        app_msg_ext_info = msg['app_msg_ext_info']
                        print(app_msg_ext_info['title'])
                        print(app_msg_ext_info['link'])
                    except KeyError:
                        print(msg)
                        continue

            else:
                print(r_json['errmsg'])
                print(r_json)
                break
            if r_json['can_msg_continue'] != 1:
                break
            params['offset'] = r_json['next_offset']
            i += 1
            if i == 100:
                break


if __name__ == '__main__':
    pass
    # api = GsDataAPI()
    # news_list = api.get_msg_info(wx_name='chaping321', posttime_start='2019-07-15', posttime_end='2019-07-28')

    # idata_api = IDataApi()
    #idata_api.get_msg_info(uid='chaping321', searchMode='top', beginDate='2018-03-01', endDate='2019-08-14')

    wechat_api = WechatAPI()
    token = wechat_api.get_token()
    fakeid = wechat_api.get_fakeid('chaping321', token)
    wechat_api.get_msg(fakeid)
