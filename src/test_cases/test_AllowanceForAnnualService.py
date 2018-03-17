# coding:utf-8
__author__ = 'Helen'
'''
description:年度服务津贴(个人入职满一年可获得)
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForAnnualService")


@ddt.ddt
class test_AllowanceForAnnualService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkDataForTesting(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        if data['position_id']!='':
            promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        # ----处理team表
            if data['team_type'] !='':
                self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helenTeam_"+str(int(data['team_id']))+"', '0', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', UNIX_TIMESTAMP('"+promoted_dt+"'), UNIX_TIMESTAMP('"+promoted_dt+"'));")
        #   ---------sales表
            self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '4', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+promoted_dt+"'), '1498552796', UNIX_TIMESTAMP('"+promoted_dt+"'), 'helen_"+sales_id+"', '"+entry_date+"');")
            # ------promoted_path
            self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)
            for i in range(1,int(data['position_id'])):
                promoted_dt = self.time_handle.get_timeByMonth(-5+i)
                if i == (int(data['position_id'])-1):
                    promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
            # ----删除业绩
            self.mysql.sql_execute("DELETE FROM order_dtd_account WHERE sales_id="+sales_id)

    def test_02insert_orderDTDAmount(self):
        '''插入1年的业绩'''
        for i in range(12,-1,-1):
            date = self.time_handle.get_timeByMonth(-i)
            for data in orderDTDAmount_data:
                top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                if data['amount_'+str(i)]!='':
                    data['amount']= data['amount_'+str(i)]
                    self.pu.insert_orderDTDAmount(data)
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''生成1年的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(12,-1,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_04CheckResult(self,data):
        '''检查各账号年度服务津贴'''
        if data['position_id']!='':
            sales_id = str(int(data['salesId']))
            try:
                if str(data['allowance'])!=u'空':
                    allowanceFromDataBase = self.mysql.get_data("SELECT annual_service_a from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')")[0][0]
                    self.assertTrue(float(data['allowance'])==float(allowanceFromDataBase))
                else:
                    SalaryRecord = self.mysql.get_data("SELECT COUNT(*) from salary_component where sales_id ="+sales_id+" AND DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')")[0][0]
                    self.assertTrue(int(SalaryRecord)==0)
            except Exception as e:
                print sales_id
                raise e