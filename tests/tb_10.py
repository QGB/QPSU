import requests

headers = {
    'pragma': 'no-cache',
    'cookie': 'thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=7adac4c770528ac068c9c758ca99d48c; _fbp=fb.1.1601271299138.1654296065; enc=CNklUX8It%2FZa9354qeivGCorJN0uB9EKpvriCHXg0s65KjKiBC3stmwl9SIauBVzob46b8vUuzjmU3h%2BCJzSdA%3D%3D; cna=umhSFlAx6RcCASv6yQsH8rnL; lgc=151sina; tracknick=151sina; hng=CN%7Czh-CN%7CCNY%7C156; miid=31527926890580832; cookie2=1a13f5678fafebf7f1df735267187993; _tb_token_=e47be355d1eba; v=0; _samesite_flag_=true; _m_h5_tk=4d10e95e86ad63c391230388bfe47cf1_1620389402010; _m_h5_tk_enc=85c6c2988ae80a46c54d964f541789a2; xlly_s=1; unb=2988240925; cookie17=UUGq2QNjG3Rc1Q%3D%3D; dnk=151sina; _l_g_=Ug%3D%3D; sg=a5b; _nk_=151sina; cookie1=U%2BHFT6URORvniYxwyHRifX6gte%2B%2FkCiO0Oerwg74u0o%3D; sgcookie=E100BAPGdimNm77syXLiXYc7S16Zd3Jw439LlvemNNvuOFRiR0cxiWgEJOueepUI1AHDXv0pXqXfxmSmyBHkG6VESg%3D%3D; uc3=id2=UUGq2QNjG3Rc1Q%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dCuwgq7m0EJcjqC60%3D&nk2=UoTdOBPF7g%3D%3D; csg=e2b5d303; skt=e06bf8df1df3684a; existShop=MTYyMDg1NTc3NQ%3D%3D; uc4=nk4=0%40UOx30U9wlIxoWhgakAFjUYbN&id4=0%40U2OdLQ4vi422EWN2%2FIutgZQXsLcg; _cc_=UtASsssmfA%3D%3D; mt=ci=99_1; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&pas=0&existShop=false&cookie21=U%2BGCWk%2F7pY%2FF&cookie14=Uoe2zXI4GEV6Fw%3D%3D; l=eBLhg_x4jbefsyxFBOfZnurza77TKIRfguPzaNbMiOCPOMfH5J0dW66pHE8MCnGVns3pR356CjdgB0LL4yUIh5friDEYKPdi3dLh.; isg=BIKCe8jlVsEkuEq-Tifyzk2g04jkU4ZtzAeVOcyb-vWgHyOZtOMNfYgZzxtjT_4F; tfstk=cyiCBOfTJ6fBp2YPYv9N8UYuHsZPZWI_IGVZdqdz99_MgzDCi-S4i-bzd1ZI9R1..',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'cache-control': 'no-cache',
    'authority': 'trade.taobao.com',
    'referer': 'https://trade.taobao.com/trade/sellerDelayConsignmentTime.htm?biz_order_id=985022369890242509&biz_type=200&user_type=buyer&cell_redirect=0',
}

params = (
    ('cell_redirect', '0'),
    ('is_success', 'T'),
    ('out_trade_no', 'T200P985022369890242509'),
    ('token', 'newTimeOut'),
    ('extend_time', '864000'),
    ('hasRefund', 'false'),
    ('bizType', '200'),
    ('bizOrderId', '985022369890242509'),
)

# response = requests.get('https://trade.taobao.com/trade/seller_delay_consignment_time_callback.do', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
r=resp=response = requests.get('https://trade.taobao.com/trade/seller_delay_consignment_time_callback.do?cell_redirect=0&is_success=T&out_trade_no=T200P985022369890242509&token=newTimeOut&extend_time=864000&hasRefund=false&bizType=200&bizOrderId=985022369890242509', headers=headers)

# 成功 {"status":true,"delayedDays":10}
# 失败 {"status":false,"delayedDays":0}
