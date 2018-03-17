# coding:utf-8
__author__ = 'Helen'
'''
description:新人训练津贴（2017.9.18）
'''
import unittest,ddt,requests,MySQLdb
from src.common.excel_data import excel
from src.common import mysql_connect,time_Handle
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForNewSales")

@ddt.ddt
class test_AllowanceForNewSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.public_modelu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # -----检查sales表
        sales_count = self.mysql.get_data("SELECT COUNT(*)FROM sales where id="+sales_id)[0][0]
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_months'])+1)
        if sales_count==0:
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '8397615', '67', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', '1498552796', '1498552796', '1498552796', 'helen_14_01', '"+entry_date+"');")
        else:
            self.mysql.sql_execute("UPDATE `spring2017`.`sales` SET `position_id`='"+str(int(data['position_id']))+"', `status`='"+str(int(data['status']))+"', `is_delete`='"+str(int(data['is_delete']))+"', `entry_date`='"+entry_date+"' WHERE (`id`='"+sales_id+"');")
        # -----检查sales_auth_info表
        auth_count = self.mysql.get_data("SELECT COUNT(*)FROM sales_auth_info where sales_id="+sales_id)[0][0]

        if auth_count==0:
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales_auth_info` (`sales_id`, `name`, `province_id`, `city_id`, `payment_id`, `payment_bank_node`, `payment_bank_account`, `identify_number`, `identify_images`, `is_delete`, `created_dt`, `auditing_dt`, `updated_dt`, `education`, `education_images`) VALUES ( '"+sales_id+"', 'sales_"+sales_id+"', '376', '377', '6', 'guang zhou tian he zhi hang', '0123456789012345677', '888888888555555555', '{\"back\":\"394b4718cd69ca16d3399de0c58278fb001\",\"front\":\"394b4718cd69ca16d3399de0c58278fb001\"}', '0', '1504232964', '0', '1504751734', '"+str(int(data['education']))+"', '[]');")
        else:
            self.mysql.sql_execute("UPDATE `spring2017`.`sales_auth_info` SET `is_delete`='0', `education`='"+str(int(data['education']))+"' WHERE (`sales_id`='"+sales_id+"' );")
        # -----删除业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)

    @ddt.data(*orderDTDAmount_data)
    def test_02insert_orderDTDAmount(self,data):
        '''插入业绩'''
        self.public_modelu.insert_orderDTDAmount(data)

    def test_03insertSalary(self):
        '''执行任务，生成当月结算数据'''
        # 为避免数据重复，先删除当月已结算的数据
        self.public_modelu.SettlementData_delete(self.time_handle.get_Current_YearMonth())
        # 重新生成新的结算数据
        self.public_modelu.SettlementData_insert(self.time_handle.get_Current_YearMonth())

    @ddt.data(*orderDTDAmount_data)
    def test_04checkResult(self,data):
        '''检查新人训练津贴结果'''
        if data['']!=u'空':
            try:
                sql_select = "SELECT newbie_training_a FROM salary_component where sales_id="+str(int(data['salesId']))+" and date=DATE_ADD(curdate(),interval -day(curdate())+1 day);"
                allowance = self.mysql.get_data(sql_select)[0][0]
                self.assertTrue(int(allowance)==int(data['Allowance']))
            except Exception,e:
                print(sql_select)
                raise e
        else:
            allowanceRecord = self.mysql.get_data("SELECT COUNT(*) FROM salary_component where sales_id="+str(int(data['salesId']))+" and DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')")[0][0]
            self.assertTrue(int(allowanceRecord)==0)
