# coding:utf-8
__author__ = 'Helen'
'''
description:展业津贴（时间以2017年为准）
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForBusinessExpanded")


@ddt.ddt
class test_AllowanceForBusinessExpanded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkDataForTesting(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ----处理sales表
        self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '8397617', '67', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', '1506787200', '1483200000', '0', 'helen_"+sales_id+"', '2017-10-01');")
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
        '''检查各账号的展业津贴'''
        sales_id = str(int(data['salesId']))
        try:
            if data['is_delete']!=1:
                allowanceFromDataBase = self.mysql.get_data("SELECT business_expanded_a from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')")[0][0]
                self.assertTrue(float(data['allowance'])==float(allowanceFromDataBase))
            else:
                allowanceCount = self.mysql.get_data("SELECT COUNT(*) FROM salary_component where sales_id="+sales_id+" AND DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')")[0][0]
                self.assertTrue(int(allowanceCount)==0)
        except Exception as e:
            print sales_id
            raise e

