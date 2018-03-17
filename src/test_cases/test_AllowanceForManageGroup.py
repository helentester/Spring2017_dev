# coding:utf-8
__author__ = 'Helen'
'''
description:直辖组管理津贴
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForManageGroup")


@ddt.ddt
class test_AllowanceForManageGroup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01deleteDataForTest(self,data):
        '''清理数据'''
        # sales
        self.mysql.sql_execute("DELETE from sales where id="+str(int(data['salesId'])))
        self.mysql.sql_execute("DELETE FROM order_dtd_account where sales_id="+str(int(data['salesId'])))
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+str(int(data['salesId'])))
        # team
        if str(data['team_type'])!='':
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE FROM team where leader_id="+str(int(data['salesId'])))
            if str(data['team_parent_id'])=='0':
                self.mysql.sql_execute("Delete FROM team where parent_id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id="+str(int(data['team_id'])))

    @ddt.data(*orderDTDAmount_data)
    def test_02checkTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ------处理sales表
        promoted_date = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '4', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+str(promoted_date)+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+entry_date+"');")
        # ------处理team表
        if str(data['team_type'])!='':
            self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helen_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', '0', '0');")
        # ------处理promoted_path表
        for i in range(1,int(data['position_id'])):
            promoted_date = self.time_handle.get_timeByMonth(-int(data['entry_date'])+i)
            if i == (int(data['position_id'])-1):
                promoted_date = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '4', '4', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")

    @ddt.data(*orderDTDAmount_data)
    def test_03insert_orderDTDAmount(self,data):
        '''插入当月业绩'''
        self.pu.insert_orderDTDAmount(data)

    def test_04insertSalary(self):
        '''删除当月的结算数据，再生成当月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        month = self.time_handle.get_YearMonth(current_month)
        self.pu.SettlementData_delete(month)
        self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_05checkResult(self,data):
        '''检查直辖组管理津贴'''
        if data['group_manager_a']!='':
            sales_id = str(int(data['salesId']))
            if data['group_manager_a']!='空':
                try:
                    allowanceFromDatabase = self.mysql.get_data("SELECT group_manager_a from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')")[0][0]
                    self.assertTrue(float(data['group_manager_a'])==float(allowanceFromDatabase))
                except Exception as e:
                    print sales_id
                    raise e
            else:
                try:
                    allowanceRecord = self.mysql.get_data("SELECT COUNT(*)from salary_component where sales_id="+sales_id+" and group_manager_a>0 and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')")[0][0]
                    self.assertTrue(int(allowanceRecord)==0)
                except Exception as e:
                    print sales_id
                    raise e