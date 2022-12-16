import requests

cookies = {
    'FA-SID': '9b5be9e6-8bca-4571-9235-650f6e6e216e',
    'Hm_lvt_e8df2744d28cda4c364b8837e3cd9eb1': '1670746230',
    'sajssdk_2015_cross_new_user': '1',
    'FA_SESSION_ID': '66f47e3b-2cdb-4148-acce-1944f697e432',
    '93bdfd49-5e25-465a-bc0b-af72e355f02a': 'webim-visitor-PBEWQ3TTRE22K9JY2FM7',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22185003c5094113-0eecf78074de38-7d5d5474-921600-185003c50965b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg1MDAzYzUwOTQxMTMtMGVlY2Y3ODA3NGRlMzgtN2Q1ZDU0NzQtOTIxNjAwLTE4NTAwM2M1MDk2NWIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22185003c5094113-0eecf78074de38-7d5d5474-921600-185003c50965b%22%7D',
    'XSRF-TOKEN': 'd8722679-e088-4f97-a535-b9c2dc422e84',
    'acw_tc': '78e2b72616707499482316374ef1ea04acd77dd3bca84a88478f61e65f',
    'Hm_lpvt_e8df2744d28cda4c364b8837e3cd9eb1': '1670750814',
}

headers = {
    'authority': 'www.jlcfa.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
    'content-type': 'application/json',
    'origin': 'https://www.jlcfa.com',
    'referer': 'https://www.jlcfa.com/product/G/G03/3V1',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24',
    'x-xsrf-token': 'd8722679-e088-4f97-a535-b9c2dc422e84',
}

json_data = {
    'attrValueIdList': [],
    'optionalParamList': [],
    'paramSelectionList': [
        {
            'paramName': '代码',
            'paramAccessId': '5cc0588c92c040939ce2f165c14a4f76',
            'displayStyle': 1,
            'paramValue': [
                '3V1',
            ],
            'singleParamValue': '3V1',
            'selected': None,
            'paramRange': None,
            'childParamList': None,
            'optionalFlag': False,
        },
 
    ],
    'serialCode': '3V1',
    'model': '',
}

rp=response = requests.post('https://www.jlcfa.com/api/faMall/serial/selection', cookies=cookies, headers=headers, json=json_data)
print(rp,rp.text[:99])

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"attrValueIdList":[],"optionalParamList":[],"paramSelectionList":[{"paramName":"代码","paramAccessId":"5cc0588c92c040939ce2f165c14a4f76","displayStyle":1,"paramValue":["3V1"],"singleParamValue":"3V1","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"电控方式","paramAccessId":"ee30c5dc92674da28a4ea3bcfb3c5177","displayStyle":1,"paramValue":["10"],"singleParamValue":"10","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"接管口径","paramAccessId":"d03eded99c63482e96a3ea0cde130b76","displayStyle":1,"paramValue":["M5"],"singleParamValue":"M5","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"初始状态","paramAccessId":"f268a590d57d408da1bcdc2d7876b5d0","displayStyle":1,"paramValue":["NC"],"singleParamValue":"NC","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"标准电压","paramAccessId":"8c10ee5f5fb64e998a8f6dfd65b344b5","displayStyle":1,"paramValue":["A"],"singleParamValue":"A","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"接电方式","paramAccessId":"0c0cfc4c74f144a1b4553459daef7adf","displayStyle":1,"paramValue":["I"],"singleParamValue":"I","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false},{"paramName":"引导方式","paramAccessId":"b6aa6822f81c486b9c17b58d3909b2c5","displayStyle":1,"paramValue":["W","无"],"singleParamValue":"W","selected":null,"paramRange":null,"childParamList":null,"optionalFlag":false}],"serialCode":"3V1","model":""}'.encode()
#response = requests.post('https://www.jlcfa.com/api/faMall/serial/selection', cookies=cookies, headers=headers, data=data)


# 'cookie': 'FA-SID=9b5be9e6-8bca-4571-9235-650f6e6e216e; Hm_lvt_e8df2744d28cda4c364b8837e3cd9eb1=1670746230; sajssdk_2015_cross_new_user=1; FA_SESSION_ID=66f47e3b-2cdb-4148-acce-1944f697e432; 93bdfd49-5e25-465a-bc0b-af72e355f02a=webim-visitor-PBEWQ3TTRE22K9JY2FM7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22185003c5094113-0eecf78074de38-7d5d5474-921600-185003c50965b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg1MDAzYzUwOTQxMTMtMGVlY2Y3ODA3NGRlMzgtN2Q1ZDU0NzQtOTIxNjAwLTE4NTAwM2M1MDk2NWIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22185003c5094113-0eecf78074de38-7d5d5474-921600-185003c50965b%22%7D; XSRF-TOKEN=d8722679-e088-4f97-a535-b9c2dc422e84; acw_tc=78e2b72616707499482316374ef1ea04acd77dd3bca84a88478f61e65f; Hm_lpvt_e8df2744d28cda4c364b8837e3cd9eb1=1670750814',