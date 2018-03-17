# coding:utf-8
__author__ = 'Helen'
'''
description:公共模块
'''
import requests,datetime
from dateutil import relativedelta
from src.common import time_Handle,mysql_connect
from selenium import webdriver
from src.pages import login_page
from bs4 import BeautifulSoup
from src.common.mysql_connect import mysql_connect
from src.common.excel_data import excel
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("team_data")

class public_modelu():
    def __init__(self):
        self.time_Handle = time_Handle.time_Handle()
        self.mysql = mysql_connect()
        self.user_Cookies = {
                '__xstn__':'ODM5NzYxNywiaGVsZW5fMTRfMDQiLCJoZWxlbl8xNF8wNCIsbnVsbCxudWxsLDAsMTQ5OTA2NTIyNCwxfDU3NmNhNTRhYWJhMTkwYTE5Y2M0NjJiM2I4YTY3ODM1',
                'CNZZDATA1261429681':'290217822-1498284828-|1499064932',
                'UM_distinctid':'15cd90ab35e6b9-0a72418e6785198-163b7640-1fa400-15cd90ab35f45d'
            }

    def checkTeamData(self):
        '''检查team表，确保组、部、区'''
        mysql = mysql_connect.mysql_connect()
        for data in orderDTDAmount_data:
            mysql.sql_execute("delete from team where id ="+str(data['team_id']))
            sql_insert = "INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', '"+data['name']+"', '"+str(int(data['parent_id']))+"', '"+str(int(data['leader_id']))+"', '"+str(int(data['type']))+"', '0', '0', '1502703540', '1502703540');"
            mysql.sql_execute(sql_insert)

    def IF_position_change_test(self):
        '''查询晋升数据，通过接口查数据'''
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
        return result
        '''
        # 把各类数据装进不同的列表
        itSales = []   # 可晋升到正式班主任的账号
        keepItSales = []   # 可降级的实习班主任
        ftSales = []   # 可晋升到金牌班主任的账号
        keepFtSales = []   # 可降级的正式班主任
        gtSales = []   # 可晋升到销售组长的账号
        keepGtSales = []   # 可降级的金牌班主任
        md1Sales = []   # 可晋升到行销主任的账号
        keepMd1Sales = []   # 可降级的行销主任
        md2Sales = []   # 可晋升到高级行销主任的账号
        keepMd2Sales = []   # 可降级的高级行销主任
        md3Sales = []   # 可晋升到资深行销主任的账号
        keepMd3Sales = []   # 可降级的资深行销主任
        md4Sales = []   # 可晋升到行销经理的账号
        keepMd4Sales = []   # 可降级的行销经理
        slSales = []   # 可晋升到资深销售组长的账号
        keepSlSales = []   # 可降级的销售组长
        smSales[] # 可晋升到销售经理的账号
        keepSmSales[] # 可降级的销售经理
        ssmSales = []   # 可晋升到资深销售经理的账号
        keepSsmSales = []   # 可降级的资深销售经理
        '''

    def select_promoteData(self):
        '''查询晋升数据,通过爬虫抓取数据'''
        try:
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

            # --------------------用爬虫抓取晋升数据
            re_cookies = {
                'PHPSESSID':r.cookies['PHPSESSID']
            }
            # --------班主任升降级页面
            re = requests.get("http://backend.spring.dev.xsteach.com/sales/position-change",cookies=re_cookies)
            soup = BeautifulSoup(re.content,'html5lib')
            promote_result={}
            # 可以晋升为正式班主任的UID
            canUpToFt=soup.find_all('input', {'name':'canUpToFtSales[]'})
            canUpToFtSales=[]
            for s in canUpToFt:
                canUpToFtSales.append(s["value"])
            #  可以晋升为金牌班主任的UID
            canUpToGt = soup.find_all('input',{'name':'canUpToGtSales[]'})
            canUpToGtSales = []
            for s in canUpToGt:
                canUpToGtSales.append(s["value"])
            # 可以晋升为销售组长的UID
            canUpToSl = soup.find_all('input',{'name':'canUpToSlSales[]'})
            canUpToSlSales = []
            for s in canUpToSl:
                canUpToSlSales.append(s["value"])
            # 可以解约的实习班主任
            keepIt = soup.find_all('input',{'name':'keepItSales[]'})
            keepItSales = []
            for s in keepIt:
                keepItSales.append(s["value"])
            #   可降级的正式班主任
            keepFt = soup.find_all('input',{'name':'keepFtSales[]'})
            keepFtSales = []
            for s in keepFt:
                keepFtSales.append(s["value"])
            #   可降级的金牌班主任
            keepGt = soup.find_all('input',{'name':'keepGtSales[]'})
            keepGtSales = []
            for s in keepGt:
                keepGtSales.append(s["value"])
            promote_result['canUpToFtSales']=canUpToFtSales     # 可以晋升为正式班主任的UID
            promote_result['canUpToGtSales']=canUpToGtSales     # 可以晋升为金牌班主任的UID
            promote_result['canUpToSlSales'] = canUpToSlSales   # 可以晋升为销售组长的UID
            promote_result['keepItSales'] = keepItSales     # 可以解约的实习班主任
            promote_result['keepFtSales'] = keepFtSales     # 可降级的正式班主任
            promote_result['keepGtSales'] = keepGtSales     # 可降级的金牌班主任
            return promote_result
        except requests.HTTPError,e:
            raise e

    def insert_orderDTDAmount(self,data):
        '''插入业绩'''
        r_text = ''
        url = ''
        try:
            base_url="http://spring.dev.xsteach.com/api/test/order?"
            url = base_url+"userId="+str(int(data['userId']))+"&salesId="+str(int(data['salesId']))+"&orderNo="+data['orderNo']+"&amount="+str(int(data['amount']))+"&orderId="+str(int(data['orderId']))
            r = requests.get(url=url,cookies=self.user_Cookies)
            r_text = r.text
            assert 'true'in r_text
        except requests.HTTPError,e:
            print url
            print r_text
            raise e

    def SettlementData_insert(self,Settlement_month):
        '''生成结算数据(状态码返回500，但是数据库里面是有生成数据的)'''
        re_text = ''
        try:
            # 数据库中记录的最后结算月份
            date_lastSettlement = self.mysql.get_data("SELECT date from settlement_log where `status`=3 ORDER BY date DESC LIMIT 1;")[0][0]
            # 把结算份从字符串转为datetime，.date()是datetime转date的意思
            date_settlement = datetime.datetime.strptime(Settlement_month+'-01','%Y-%m-%d').date()
            # 判断上个月是否已结算
            a=1
            date_lastSettlement = date_lastSettlement+relativedelta.relativedelta(months=a)
            if date_settlement>date_lastSettlement:
                # print u'上月未结算'
                while date_settlement > date_lastSettlement:
                    Settlement_month = str(date_lastSettlement)[:7]
                    url = "http://spring.dev.xsteach.com/api/test/run?date="+Settlement_month
                    result = requests.get(url=url,cookies=self.user_Cookies)
                    a+=1
                    date_lastSettlement = date_lastSettlement+relativedelta.relativedelta(months=a)
                    print url
                    assert 'success'in(result.text)
            else:
                # print u'可执行'
                Settlement_month = str(date_settlement)[:7]
                url = "http://spring.dev.xsteach.com/api/test/run?date="+Settlement_month
                result = requests.get(url=url,cookies=self.user_Cookies)
                print url
                re_text = result.text
                assert 'success'in(result.text)
        except Exception,e:
            print re_text
            raise e

    def SettlementData_delete(self,Settlement_month):
        '''删除当前月份已生成的结算数据(状态码返回500，但是数据库里面是有删除数据的)'''
        try:
            url = "http://spring.dev.xsteach.com/api/test/delete?date="+Settlement_month
            requests.get(url=url,cookies=self.user_Cookies)
            print(url)
        except Exception,e:
            raise e

    def login(self,username,password):
        profile_directory = r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\sz2448eo.default'
        profile = webdriver.FirefoxProfile(profile_directory)
        self.driver = webdriver.Firefox(profile)
        self.driver.get("http://spring.dev.xsteach.com/site/login")
        self.login_page = login_page.login_page(self.driver)
        self.login_page.input_username(username)
        self.login_page.input_password(password)
        self.login_page.click_submit_btn()
        return self.driver
