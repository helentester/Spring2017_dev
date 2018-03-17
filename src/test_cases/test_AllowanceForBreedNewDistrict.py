# coding:utf-8
# @DATE    : 2018/1/19
__author__ = 'Helen'
'''
description:区育成津贴
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForBreedNewDistrict")

@ddt.ddt
class test_AllowanceForBreeNewDistrict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01DeleteDataForTest(self,data):
        '''清除影响测试的数据'''
        # sales
        self.mysql.sql_execute("DELETE from sales where id="+str(int(data['salesId'])))
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+str(int(data['salesId'])))
        # team
        if data['team_type']!='':
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id ="+str(int(data['team_id'])))
        # promoted_path
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+str(int(data['salesId'])))

    @ddt.data(*orderDTDAmount_data)
    def test_02InsertTestData(self,data):
        '''插入测试数据'''
        sales_id = str(int(data['salesId']))
        # 当前职位和晋升时间
        List_position = str(data['position_id'])
        positions = List_position.split(',')
        position = positions[len(positions)-1]  # 以最后一个晋升职位为准
        List_promoted_dt = str(data['promoted_dt'])
        promoted_dts = List_promoted_dt.split(',')
        promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dts[len(promoted_dts)-1]))) # 以最后一个晋升时间为准
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        # sales
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(float(position)))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+str(promoted_date)+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+entry_date+"');")
        # team
        if data['team_type']!='':
            self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helen_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', '0', '0');")
        # promotion_path
        # 正常晋升数据
        promote_type = 2    # 2=晋升,3=降级
        for i in range(1,int(float(positions[0]))+1):
            promoted_date = self.time_handle.get_timeByMonth(-int(data['entry_date'])+i)
            if i == int(float(positions[0])):
                promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dts[0])))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(i-1)+"', '"+str(i)+"', '"+str(promote_type)+"', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")
        # 特殊晋升降级数据
        if len(positions)>1:
            for i in range(1,len(positions)):
                promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dts[i])))
                # 获取promotion type
                if int(float(positions[i-1]))>int(float(positions[i])):
                    promote_type = 3
                else:
                    promote_type = 2
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(positions[i-1])+"', '"+str(positions[i])+"', '"+str(promote_type)+"', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")

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
        '''检查部育成津贴'''
        if data['allowance']!='':
            sales_id = str(int(data['salesId']))
            try:
                if data['allowance']!=u'空':
                    allowanceFromDatabase = self.mysql.get_data("SELECT dist_promotion_a from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m') ")[0][0]
                    self.assertTrue(float(data['allowance'])==float(allowanceFromDatabase))
                else:
                    allowanceRecord = self.mysql.get_data("SELECT COUNT(*)from salary_component where sales_id="+sales_id+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')")[0][0]
                    self.assertTrue(int(allowanceRecord)==0)
            except Exception as e:
                print sales_id
                raise e