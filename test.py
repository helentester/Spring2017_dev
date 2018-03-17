# coding:utf-8
import requests,ssl
from bs4 import BeautifulSoup

# 获取娱乐大厅的广告列表
# re = requests.get("http://api.dev.xsteach.com/v2/default/front-cover?tag=rec_mall_ad")
headers={
'Host': 'dev.xsteach.com',
'Connection': 'keep-alive',
'Content-Length': '98',
'Cache-Control': 'max-age=0',
'Origin': 'https://dev.xsteach.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4033.400 QQBrowser/9.6.12624.400',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer': 'https://dev.xsteach.com/site/pop-login?goto=http%3A%2F%2Fdev.xsteach.com%2F&wh=',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'UM_distinctid=1603051743657-0ca737d532b7fe-35487952-1fa400-16030517437253; bdshare_firstime=1513062967093; Hm_lvt_666eed3d1138aba8c53e5d28cf45cdff=1513064496,1513065128,1513065140,1513224448; praiseUser=0.75096700+1513303768.11649; looyu_id=8c879d8e5000a42cf4954b5d1c15560304_20000267%3A51; PHPSESSID=c2c70jemg82q9416alh6jttio3; XsHm_lvt_ab4e2cebd0f7f7442c57ae9a5cf5fe45=1512956345,1513061493,1513149575,1513304078; XsHm_lpvt_ab4e2cebd0f7f7442c57ae9a5cf5fe45=1513309857; XsHm_cv_ab4e2cebd0f7f7442c57ae9a5cf5fe45=; io=r5-Nzjq41Gck0zZOAAM5; looyu_20000267=v%3A4d1fcf39adf97810e55c28f8b8a467515a%2Cref%3A%2Cr%3A%2Cmon%3Ahttps%3A//m7828.looyu.com/monitor%2Cp0%3Ahttp%253A//dev.xsteach.com/; _99_mon=%5B0%2C0%2C0%5D'
}
parameter = {'LoginForm[username]':'云风111','LoginForm[password]':'123456','LoginForm[rememberMe]':'0'}
ssl._create_default_https_context = ssl._create_unverified_context
# 访问HTTPS
# r = requests.post("https://dev.xsteach.com/site/pop-login?",data=parameter,headers=headers,verify=False)
# 访问HTTP
r = requests.post("http://dev.xsteach.com/site/pop-login?",data=parameter)
#print r.text

re_cookies = {
    '__xstn__':r.cookies['__xstn__']
}

# 老师发送挖宝
send_data = {
    'amount':'10',
    'expire_duration':'5',
    'live_course_id':'439',
    'number':'1',
    'signal':u'想要中大奖吗？点我呀'
}
send_request = requests.post('http://api.dev.xsteach.com/v2/new-live/send-treasure',cookies=re_cookies,data=send_data)
print send_request.text
'''
# 学员直播教室挖宝接口
re_data = {
    'live_course_id':'439',
    'treasure_id':'547',
    'user_id':'8397520'}
re = requests.post("http://api.dev.xsteach.com/v2/new-live/dig-treasure",cookies=re_cookies,data=re_data)
# 用户挖宝信息
print re.text
'''