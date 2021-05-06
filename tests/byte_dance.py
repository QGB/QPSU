lr=U.get_or_set('lr',[])

import requests
offset=py.str(0)
cookies = {
    'channel': 'office',
    'platform': 'pc',
    's_v_web_id': 'koctiste_NlH2CNOB_EzGx_4U3H_B3tJ_EEH9pdgV5jpZ',
    'device-id': '6959140809849538084',
    'atsx-csrf-token': 'Ajb6R8nh0MRLludN_aY-KVI2Sb3b7-kPw042x9aEcNA%3D',
    'SLARDAR_WEB_ID': 'd48b13fc-1873-4a2d-bd82-31a75c714d56',
}

headers = {
    'Origin': 'https://jobs.bytedance.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'x-csrf-token': 'Ajb6R8nh0MRLludN_aY-KVI2Sb3b7-kPw042x9aEcNA=',
    'accept-language': 'zh-CN',
    'env': 'undefined',
    'Portal-Channel': 'office',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Cache-Control': 'no-cache',
    'Referer': 'https://jobs.bytedance.com/experienced/position?keywords=&category=6704215862603155720%2C6704215862557018372%2C6704215886108035339%2C6704215888985327886%2C6704215897130666254%2C6704215956018694411%2C6704215957146962184%2C6704215958816295181%2C6704215963966900491%2C6704216109274368264%2C6704216296701036811%2C6704216635923761412%2C6704217321877014787%2C6704219452277262596%2C6704219534724696331%2C6938376045242353957&location=&project=&type=&job_hot_flag=&current=2&limit=10',
    'website-path': 'society',
    'Portal-Platform': 'pc',
}

params = (
    ('keyword', ''),
    ('limit', '20'),
    ('offset', offset),
    ('job_category_id_list', '6704215862603155720,6704215862557018372,6704215886108035339,6704215888985327886,6704215897130666254,6704215956018694411,6704215957146962184,6704215958816295181,6704215963966900491,6704216109274368264,6704216296701036811,6704216635923761412,6704217321877014787,6704219452277262596,6704219534724696331,6938376045242353957'),
    ('location_code_list', ''),
    ('subject_id_list', ''),
    ('recruitment_id_list', ''),
    ('portal_type', '2'),
    ('portal_entrance', '1'),
    ('_signature', 'Hk80KwAAAADsYAZsuyOq8B5PNDAAH7k'),
)
params={} # 这个没用，改 data 就行

data = '{"keyword":"","limit":10000,"offset":%(offset)s,"job_category_id_list":["6704215862603155720","6704215862557018372","6704215886108035339","6704215888985327886","6704215897130666254","6704215956018694411","6704215957146962184","6704215958816295181","6704215963966900491","6704216109274368264","6704216296701036811","6704216635923761412","6704217321877014787","6704219452277262596","6704219534724696331","6938376045242353957"],"location_code_list":[],"subject_id_list":[],"recruitment_id_list":[],"portal_type":2,"portal_entrance":1}'%py.locals()

r=response = requests.post('https://jobs.bytedance.com/api/v1/search/job/posts', headers=headers, params=params, cookies=cookies, data=data)

lr.append(response)
print(response,len(lr))

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://jobs.bytedance.com/api/v1/search/job/posts?keyword=&limit=10&offset=10&job_category_id_list=6704215862603155720%2C6704215862557018372%2C6704215886108035339%2C6704215888985327886%2C6704215897130666254%2C6704215956018694411%2C6704215957146962184%2C6704215958816295181%2C6704215963966900491%2C6704216109274368264%2C6704216296701036811%2C6704216635923761412%2C6704217321877014787%2C6704219452277262596%2C6704219534724696331%2C6938376045242353957&location_code_list=&subject_id_list=&recruitment_id_list=&portal_type=2&portal_entrance=1&_signature=Hk80KwAAAADsYAZsuyOq8B5PNDAAH7k', headers=headers, cookies=cookies, data=data)
