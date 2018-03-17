# coding:utf-8
__author__ = 'Helen'
'''
description:组育成津贴
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("AllowanceForBreedNewGroup")

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
            # --------删除业绩
            # 删除销售组业绩
            if int(data['team_parent_id'])==0:
                self.mysql.sql_execute("DELETE from order_dtd_account where sales_id in(SELECT id from sales where team_id="+team_id+")")
            else:
                self.mysql.sql_execute("DELETE FROM order_dtd_account where sales_id in(SELECT id from sales where team_id IN (SELECT id from team where parent_id="+str(int(data['team_parent_id']))+"))")
        # 删除测试账号的所有业绩]
        self.mysql.sql_execute("DELETE FROM order_dtd_account where sales_id="+sales_id)
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
        # ------处理breeder_lower_sales表，设计育成人级别比被育成人低的记录
        self.mysql.sql_execute("DELETE from breeder_lower_sales where sales_id="+sales_id)
        if sales_id=='43214436':
            created_dt = self.time_handle.get_timeByMonth(-1)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`breeder_lower_sales` (`sales_id`, `breeder_id`, `type`, `created_dt`) VALUES ('43214436', '43214435', '1', UNIX_TIMESTAMP('"+created_dt+"'));")

    @ddt.data(*orderDTDAmount_data)
    def test_02insert_orderDTDAmount(self,data):
        '''插入当月业绩'''
        self.pu.insert_orderDTDAmount(data)

    def test_03insertSalary(self):
        '''删除当月的结算数据，再生成当月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        month = self.time_handle.get_YearMonth(current_month)
        self.pu.SettlementData_delete(month)
        self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_04checkResult_allowanceForBreeNewDept(self,data):
        '''检查部育成津贴'''
        if data['allowance']!='':
            if data['allowance']!=u'空':
                allowance = float(data['allowance'])
                allowanceFromDatabase = self.mysql.get_data("SELECT group_promotion_a from salary_component where sales_id="+str(int(data['salesId']))+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m') ")[0][0]
                try:
                    self.assertTrue(allowance==float(allowanceFromDatabase))
                except Exception as e:
                    print data['salesId']
                    raise e
            else:
                allowanceRecord = self.mysql.get_data("SELECT COUNT(*) from salary_component where sales_id="+str(int(data['salesId']))+" and DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m');")[0][0]
                self.assertTrue(int(allowanceRecord)==0)

    def test_05checkResult_breederLowerRecord(self):
        '''检查是否记录育成人职位低于被育成人的情况'''
        record = self.mysql.get_data("SELECT COUNT(*) from breeder_lower_sales where sales_id=43214436 and breeder_id=43214435")[0][0]
        self.assertTrue(int(record)>0)