# coding:utf-8
__author__ = 'Helen'
'''
description:个人季度奖金(需要设置各季度参数：cls.jidu=1  # 测试季度：1、2、3、4)
'''
import unittest, requests,ddt,datetime
from src.common.excel_data import excel
from src.common import mysql_connect,time_Handle
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("bonus_quarter")
# sales_data = excel_data.get_list("sales_data")


@ddt.ddt
class test_bonus_quarter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public_modelu = public_modelu.public_modelu()
        cls.time_handle = time_Handle.time_Handle()
        cls.mysql = mysql_connect.mysql_connect()
        cls.jidu=1  # 测试季度：1、2、3、4
        # 设置各季度的特殊时间
        cls.year = str(cls.time_handle.get_Current_Year())
        cls.quarter = {'month_3':cls.year+'-01','month_2':cls.year+'-02','month_1':cls.year+'-03'}
        cls.months_pd = {'pd_1':11,'pd_2':10}
        if cls.jidu==2:
            cls.quarter = {'month_3':cls.year+'-04','month_2':cls.year+'-05','month_1':cls.year+'-06'}
            cls.months_pd = {'pd_1':8,'pd_2':7}
        elif cls.jidu==3:
            cls.quarter = {'month_3':cls.year+'-07','month_2':cls.year+'-08','month_1':cls.year+'-09'}
            cls.months_pd = {'pd_1':5,'pd_2':4}
        elif cls.jidu==4:
            cls.quarter = {'month_3':cls.year+'-10','month_2':cls.year+'-11','month_1':cls.year+'-12'}
            cls.months_pd = {'pd_1':2,'pd_2':1}

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self, data):
        '''检查用于测试个人季度奖的数据'''
        sales_id = str(int(data['salesId']))
        # -----检查sales表
        sales_count = self.mysql.get_data("SELECT COUNT(*)FROM sales where id = "+sales_id)[0][0]
        if sales_count==0:
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '8397615', '67', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', '1498963733', '1498552796', '1498963877', 'helen_"+sales_id+"', '2015-03-01');")
        else:
            self.mysql.sql_execute("UPDATE `spring2017`.`sales` SET   `position_id`='"+str(int(data['position_id']))+"', `status`='"+str(int(data['status']))+"', `is_delete`='"+str(int(data['is_delete']))+"', `entry_date`='2016-03-01' WHERE (`id`='"+sales_id+"');")
        # -----检查promoted_path表，处理晋升日期
        start_date = datetime.datetime.strptime(self.quarter['month_1']+'-08','%Y-%m-%d')
        # 当前时间与2017年9月的时间差（月份）
        months = self.time_handle.get_months(start_date,datetime.datetime.now())
        promoted_dt = self.time_handle.get_timeByMonth(-months-25)    # 季度开始前晋升为班主任已满一年多
        if sales_id == '8397622':
            promoted_dt = self.time_handle.get_timeByMonth(-months-self.months_pd['pd_1'])    # 季度开始前晋升班主任未满一年，算后两个月
        if sales_id in('8397623','8397624','43214313'):
            promoted_dt = self.time_handle.get_timeByMonth(-months-self.months_pd['pd_2'])    # 季度开始前晋升班主任未满一年，算后1个月
        if sales_id in('43214314','43214315'):
            promoted_dt = self.time_handle.get_timeByMonth(-months-1)    # 晋升班主任未满一年，无季度奖
        # 插入升降级日志
        self.mysql.sql_execute("delete from promotion_path where sales_id="+sales_id)
        # 设置降级日志
        if sales_id in ('43214313','43214315'):
            promoted_dt_d = self.time_handle.get_timeByMonth(-months-15)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` (`sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ( '"+sales_id+"', '67', '67', '8397617', '8397617', '2', '1', '3', UNIX_TIMESTAMP('"+str(promoted_dt_d)+"'), '0');")
        # 设置升级日志
        self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` (`sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ( '"+sales_id+"', '67', '67', '8397617', '8397617', '1', '2', '2', UNIX_TIMESTAMP('"+str(promoted_dt)+"'), '0');")
        # --------删除业绩
        self.mysql.sql_execute("delete from order_dtd_account where sales_id="+sales_id)

    def test_02insert_orderDTDAmount(self):
        '''插入三个月的数据'''
        for i in range(3,0,-1):
            date = self.quarter['month_'+str(i)]+str("-01")
            for data in orderDTDAmount_data:
                top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                data['amount']= data['amount_'+str(i)]
                self.public_modelu.insert_orderDTDAmount(data)
                self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''结算三个月薪酬'''
        for i in range(3,0,-1):
            date = self.quarter['month_'+str(i)]
            self.public_modelu.SettlementData_delete(date)
            self.public_modelu.SettlementData_insert(date)

    @ddt.data(*orderDTDAmount_data)
    def test_04checkResult(self,data):
        '''检查各账号的个人季度奖'''
        # 数据库中取得个人季度奖
        sales_id = str(int(data['salesId']))
        try:
            date = self.quarter['month_1']+str("-01")
            if data['bonus']!=u'空':
                bonus = self.mysql.get_data("SELECT personal_quarter_b from salary_component where date='"+date+"' AND sales_id="+sales_id)[0][0]
                self.assertTrue(float(bonus)==float(data['bonus']))
            else:
                bonusCount = self.mysql.get_data("SELECT COUNT(*) from salary_component where date='"+date+"' AND sales_id="+sales_id)[0][0]
                self.assertTrue(int(bonusCount)==0)
        except Exception as e:
            print sales_id
            raise e

    @classmethod
    def tearDownClass(cls):
        pass

if __name__=='__main__':
    unittest.main()