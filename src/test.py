# coding:utf-8
__author__ = 'Helen'
'''
description:
'''
import requests
# --------登录接口
url="http://backend.spring.dev.xsteach.com/site/login"
parameter = {'User[username]':'admin15','User[password]':'123456','_csrf':'eTZTZFgwQmdJYjIGalh1VhEBKwYsdDo4FQUKKwtTAQ5LejgFGWcTAg=='}
headers = {
	            'Host': 'backend.spring.dev.xsteach.com',
	            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
	            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	            'Accept-Encoding': 'gzip, deflate',
	            'Referer': 'http://backend.spring.dev.xsteach.com/site/index',
	            'Cookie': 'UM_distinctid=15d7da78be29-024f78918c9b748-163b7640-1fa400-15d7da78be3223; Hm_lvt_666eed3d1138aba8c53e5d28cf45cdff=1501489813,1501504710,1501554087,1501555306; looyu_id=7f6af6532dfddf8613ae7bb1a94fc3e548_20000267%3A7; register_spread_id=8397520; looyu_20000267=v%3A0fcce1a301f1c1ec1924532dc9b531ad38%2Cref%3A%2Cr%3A%2Cmon%3Ahttp%3A//m7827.looyu.com/monitor%2Cp0%3Ahttp%253A//www.xsteach.com/; Hm_lpvt_666eed3d1138aba8c53e5d28cf45cdff=1501555367; XsHm_lvt_ab4e2cebd0f7f7442c57ae9a5cf5fe45=1501155143,1501468503,1501489938,1501555385; XsHm_lpvt_ab4e2cebd0f7f7442c57ae9a5cf5fe45=1501555415; XsHm_cv_ab4e2cebd0f7f7442c57ae9a5cf5fe45=; xst_cic=0; __xstn__=ODM5NzYxNywiaGVsZW5fMTRfMDQiLCJoZWxlbl8xNF8wNCIsbnVsbCxudWxsLDAsMTUwMTU1NTM5OSwwfDVjMDgyOTFjMjhjMmNjNGIyZTI1MzVkNGJmOTdiODU2; __xstn__i__=ODM5NzYxNw%3D%3D; _99_mon=%5B0%2C0%2C0%5D; PHPSESSID=kac591gatnts29hgpntddvju81; _csrf=3a354f21ba4ee38debbbc37626946dd079f92a68cec253f5632879d9e9fdf279a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%220Tab2h71h7xbtDx_l3YOScCi2LkaAWQe%22%3B%7D',
	            'Connection': 'keep-alive'
            }
r = requests.post(url=url,data=parameter,headers=headers,allow_redirects=False)
re_cookies = {
                'PHPSESSID':r.cookies['PHPSESSID']
            }
re = requests.get("http://backend.spring.dev.xsteach.com/sales/position-change-test",cookies=re_cookies)
result = re.json()
print result['keepSmSales']

assert 8397619 in result['keepSmSales']






'''
def getImageCode(posturl):
    res = {}
    headers = getConfig('header/ImageCodeHeader.txt')
    url = baseurl+posturl+datetime.now().strftime('%a %b %d %Y %X %Z')
    code_resp = requests.get(url)
    image = Image.open(BytesIO(code_resp.content))
    (x, y) = image.size
    x_s = 280
    y_s = y * x_s / x
    image_rs = image.resize((x_s,y_s), Image.ANTIALIAS)
    image_rs.save('code.png')
    Image.open('code.png').show()
    code = pytesseract.image_to_string(Image.open('code.png'))
    res['Cookie'] = (code_resp.headers.get('Set-Cookie').split(';'))[0]
    res['code'] = code
    print code
'''