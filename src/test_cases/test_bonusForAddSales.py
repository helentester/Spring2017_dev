# coding:utf-8
__author__ = 'Helen'
'''
description:增员奖金测试
'''
import ddt,unittest,requests
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("bonusForAddSales")

@ddt.ddt
class test_bonusForAddSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pu = public_modelu.public_modelu()
        cls.time_handle = time_Handle.time_Handle()
        cls.mysql = mysql_connect.mysql_connect()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ------处理sales表
        self.mysql.sql_execute("DELETE from sales where id="+sales_id)
        date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+date+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+date+"');")
        # ----删除业绩
        self.mysql.sql_execute("DELETE FROM order_dtd_account where sales_id in(SELECT id from sales where breeder_id="+str(int(data['breeder_id']))+");")

    @ddt.data(*orderDTDAmount_data)
    def test_02insert_orderDTDAmount(self,data):
        '''生成业绩数据'''
        self.pu.insert_orderDTDAmount(data)

    def test_04CreateSalary(self):
        '''执行任务，生成当月结算数据'''
        # 为避免数据重复，先删除当月已结算的数据
        self.pu.SettlementData_delete(self.time_handle.get_Current_YearMonth())
        # 重新生成新的结算数据
        self.pu.SettlementData_insert(self.time_handle.get_Current_YearMonth())

    @ddt.data(*orderDTDAmount_data)
    def test_05checkResult(self,data):
        '''检查增员奖金（date还需要优化）'''
        sales_id = str(int(data['salesId']))
        if data['bonus']!='':
            if data['bonus']!=u'空':
                try:
                    bonusFromDatabase = self.mysql.get_data("SELECT team_grow_b from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m');")[0][0]
                    self.assertTrue(float(bonusFromDatabase)==float(data['bonus']))
                except Exception,e:
                    print sales_id
                    raise e
            else:
                bonusRecord = self.mysql.get_data("SELECT COUNT(*) from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m');")[0][0]
                self.assertTrue(int(bonusRecord)==0)

    @classmethod
    def tearDownClass(cls):
        pass