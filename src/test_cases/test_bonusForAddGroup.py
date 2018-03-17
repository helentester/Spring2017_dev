# coding:utf-8
__author__ = 'Helen'
'''
description:增组奖
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("bonusForAddGroup")

@ddt.ddt
class test_AllowanceForBreeNewGroup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ----处理sales表
        # 当前职位和晋升时间
        position = str(data['position_id'])
        promoted_dt = str(data['promoted_dt'])
        if len(position)!=3:
            positions = position.split(',')
            position = positions[2]     # 以最后一个晋升职位为准
            promoted_dts = promoted_dt.split(',')
            promoted_dt = promoted_dts[2]   # 以最后一个晋升时间为准
        self.mysql.sql_execute("DELETE from sales where id="+sales_id)
        promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dt)))
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(float(position)))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+str(promoted_date)+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+entry_date+"');")
        # ------处理team表
        if str(data['team_type'])!='':
            team_id = str(int(data['team_id']))
            self.mysql.sql_execute("DELETE from team where id="+team_id)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+team_id+"', 'helen_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', '0', '0');")
        # ----处理promotion_path表
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+sales_id)
        for i in range(1,int(float(position))):
            promoted_date = self.time_handle.get_timeByMonth(-int(data['entry_date'])+i)
            if i == (int(float(position))-1):
                promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dt)))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")
        # 处理晋升－降级－晋升数据
        if len(str(data['position_id']))!=3:
            self.mysql.sql_execute("DELETE from promotion_path where sales_id="+sales_id)
            positions = str(data['position_id']).split(',')
            promoted_dts = str(data['promoted_dt']).split(',')
            position = positions[0]
            for i in range(1,int(float(position))):
                promoted_date = self.time_handle.get_timeByMonth(-int(data['entry_date'])+i)
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")
            for j in range(1,3):
                promoted_date = self.time_handle.get_timeByMonth(-int(float(promoted_dts[j])))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '"+str(int(data['team_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['breeder_id']))+"', '"+str(int(float(positions[j-1])))+"', '"+str(positions[j])+"', '2', UNIX_TIMESTAMP('"+promoted_date+"'), '15');")
        # -----删除业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)

    @ddt.data(*orderDTDAmount_data)
    def test_02insert_orderDTDAmount(self,data):
        '''根据入职时间插入业绩'''
        entry_date = int(data['entry_date'])
        for i in range(entry_date,-1,-1):
            amount_date = self.time_handle.get_timeByMonth(-i)
            self.pu.insert_orderDTDAmount(data)
            top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
            self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(amount_date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''删除前13个月的结算数据，再生成前13个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(13,-1,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_04checkResult(self,data):
        '''测试增组奖'''
        if data['bonus']!='':
            if data['bonus']!=u'空':
                try:
                    bonusFromDataBase = self.mysql.get_data("SELECT group_promotion_b from salary_component WHERE sales_id ="+str(int(data['salesId']))+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m');")[0][0]
                    self.assertTrue(float(bonusFromDataBase)==float(data['bonus']))
                except Exception as e:
                    print data['salesId']
                    raise e
            else:
                bonusRecord = self.mysql.get_data("SELECT COUNT(*) from salary_component WHERE sales_id ="+str(int(data['salesId']))+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m');")[0][0]
                self.assertTrue(int(bonusRecord)==0)