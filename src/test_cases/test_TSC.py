# coding:utf-8
__author__ = 'Helen'
'''
description:测试佣金
'''
import unittest, requests,ddt
from src.common.excel_data import excel
from src.common import mysql_connect,time_Handle
import public_modelu

# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("TSC")


@ddt.ddt
class test_TSC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.pu = public_modelu.public_modelu()
        cls.time_handle = time_Handle.time_Handle()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ------处理sales表
        if data['position_id']!='':
            self.mysql.sql_execute("DELETE from sales where id="+sales_id)
            date = self.time_handle.get_timeByMonth(0)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '4', '700', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+date+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+date+"');")
            # ----删除业绩
            self.mysql.sql_execute("DELETE FROM order_dtd_account WHERE sales_id="+sales_id)

    @ddt.data(*orderDTDAmount_data)
    def test_02insert_orderDTDAmount(self,data):
        '''插入当月业绩数据'''
        self.pu.insert_orderDTDAmount(data)

    def test_03insertSalary(self):
        '''删除当月的结算数据，再生成当月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        month = self.time_handle.get_YearMonth(current_month)
        self.pu.SettlementData_delete(month)
        self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_04CheckResult(self,data):
        '''检查TSC'''
        sales_id = str(int(data['salesId']))
        if data['TSC']!='':
            if data['TSC']!=u'空':
                try:
                    TSCFromDataBase = self.mysql.get_data("SELECT tsc FROM salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m') ")[0][0]
                    self.assertTrue(float(TSCFromDataBase)==float(data['TSC']))
                except Exception as e:
                    print 'sales_id:'+sales_id
                    raise e
            else:
                TSCRecord = self.mysql.get_data("SELECT COUNT(*) FROM salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')")[0][0]
                self.assertTrue(int(TSCRecord)==0)

    @classmethod
    def tearDownClass(cls):
        pass

if __name__=='__main__':
    unittest.main()