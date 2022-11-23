import requests
cookies = {
    'Hm_lvt_8cceebbdae0934a95c5e89d288c2a2c9': '1667062285',
    '_ga': 'GA1.2.1648201286.1667062326',
    'sensorsdata2015jssdkcross': 'dfm-enc-%7B%22Va28a6y8_aV%22%3A%22EtSsSitSGEHtnI-AVtEyiRuRtSgIG-RVHVHSRS-sARInAA-EtSsSitSGEnSuu%22%2C%22gae28_aV%22%3A%22%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24ki8r28_ergreere%22%3A%22z88O2%3A%2F%2Fm2zMzbu.ymo%2F%22%2C%22%24ki8r28_ki6Va6f_Oifr%22%3A%22z88O2%3A%2F%2FOem.kyrVi.y6%2FrVa8me%23aV%3DsIAAASSnygVtSsRRusVIVyERVSsArnHG%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFfAwq7zpXNHwFKSQqw8w9NSwZQzQs3IpX7owhl8QsNEWXKAQhN8wq0IwhPMwvAJpXNcQ91SQXlJQq7aPaxG%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%22%2C%22Cikbr%22%3A%22%22%7D%2C%22%24VrCayr_aV%22%3A%22EtSsSitSGEHtnI-AVtEyiRuRtSgIG-RVHVHSRS-sARInAA-EtSsSitSGEnSuu%22%7D',
    'lcedaReferer': 'eyJpdiI6ImhtS2ZCU2ZyR1VsZG1sdkF1bmNhZ3c9PSIsInZhbHVlIjoiVEZHSkNnVWY2dUd6TnRsSzV3S2dvazZha2xDQ2tkZHVWSTlralhIczN0OHZiZ1g5YUJ1Q3hiOFFwcEFORHZwSVVoNVdiSlp4dUc5OTlrMW5zVE9ScFFFalFHS3NTK0Zadk1JaVVlQVN6TzZmQTRFS2ZBQzRESHpzRENkSG5uNUEiLCJtYWMiOiJjYTZjNmM0ZWNkNjYxNTIyNzBiNTk0NmFlMmRkZDA0MjllMTYyOGNmYjRjZDZjZWI0NDEyN2MzNGRhZTViMWVhIn0%3D',
    'googtrans': '/auto/zh-CN',
    '_gid': 'GA1.2.870287459.1668585898',
    'easyeda_user': '%7B%22username%22%3A%22[qgb_username]%22%2C%22avatar%22%3A%22%5C%2F%5C%2Fimage.lceda.cn%5C%2Fpullimage%5C%2F9crn67iSeoruG0iO7MTYWCBJWtgBUpXODU3GuKaJ.jpeg%22%2C%22uuid%22%3A%22f87c808f549443acbac8e59cc590cbc3%22%7D',
    'Hm_lpvt_8cceebbdae0934a95c5e89d288c2a2c9': '1668586451',
    'acw_tc': '2f624a3116686575162912550e0a93b67fe7c598723b2f044bad767c27240e',
    'lceda_session': 'eyJpdiI6IjYxRk9tK256bjlmclZ3UTZEdlhaSVE9PSIsInZhbHVlIjoiUE9rRDI1NnhLUmFEYUFIcm9Hc2JuYXRjMUVqNENQRDdQT29QNXd4eHJVdEpnclpiUys2NzdGODdpdFdHcll2dXk3R0k3QlNXVmFQNG54eERnNXpvUUE9PSIsIm1hYyI6IjdlMzliNmM5ZmIzZWY3ZjAyNmMwM2I0ODU4ZjFmNDgwZmU3ZmIyNDUzYmQyNmQxNGZiYTkwZWQ2ZTRjYzcwNTMifQ%3D%3D',
}

headers = {
    'authority': 'lceda.cn',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    'origin': 'https://lceda.cn',
    'referer': 'https://lceda.cn/editor',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24',
    'x-requested-with': 'XMLHttpRequest',
}

def get_all_components():
	return requests.get('https://lceda.cn/api/components?version=6.5.23&docType=4&uid=f87c808f549443acbac8e59cc590cbc3&type=3&tag%5B%5D=All').json()

def delete_component(uuid):
	data = {
		'uuid': uuid,#'f90fe65a90d94ea4a573b0fb60a43ca5',
		'version': '6.5.23',
	}
	rp=response = requests.post(f'https://lceda.cn/api/components/{uuid}/delete', cookies=cookies, headers=headers, data=data)
	return rp,rp.json()