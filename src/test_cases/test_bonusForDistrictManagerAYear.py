# coding:utf-8
# @DATE    : 2018/1/18
__author__ = 'Helen'
'''
description:直辖区年终奖（时间以2017年为准）
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("bonusForDistrictManagerAYear")


@ddt.ddt
class test_bonusForDistrictManagerAYear(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01deleleDataForTesting(self,data):
        '''清理数据'''
        sales_id = str(int(data['salesId']))
        # 删除个人业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)
        # sales
        self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
        # team
        if data['team_type'] !='':
            self.mysql.sql_execute("DELETE from sales where team_id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id ="+str(int(data['team_id'])))

    @ddt.data(*orderDTDAmount_data)
    def test_02checkDataForTesting(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # ----插入满一年的团队数据
        if int(data['team_created'])>11:
            # team表
            if data['team_type'] !='':
                team_created = self.time_handle.get_timeByMonth(-int(data['team_created']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helenTeam_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', UNIX_TIMESTAMP('"+team_created+"'), UNIX_TIMESTAMP('"+team_created+"'));")
            # sales表
            promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '4', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+promoted_dt+"'), '1498552796', UNIX_TIMESTAMP('"+promoted_dt+"'), 'helen_"+sales_id+"', '"+entry_date+"');")
            # promoted_path表
            self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)
            for i in range(1,int(data['position_id'])):
                promoted_dt = self.time_handle.get_timeByMonth(-7+i)
                if i == (int(data['position_id'])-1):
                    promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")

    def test_03insert_orderDTDAmount(self):
        '''插入1至6月的业绩'''
        for i in range(1,7):
            date = '2017-'+str(i)+'-01'
            for data in orderDTDAmount_data:
                if data['amount_'+str(i)]!='':
                    data['amount']= data['amount_'+str(i)]
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_04insertSalary(self):
        '''生成1至6月的结算数据'''
        for i in range(1,7):
            month = '2017-'+str(i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_05updateTestData(self,data):
        '''插入新团队'''
        sales_id = str(int(data['salesId']))
        if int(data['team_created'])<12:
            # team表
            if data['team_type'] !='':
                self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
                team_created = self.time_handle.get_timeByMonth(-int(data['team_created']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helenTeam_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', UNIX_TIMESTAMP('"+team_created+"'), UNIX_TIMESTAMP('"+team_created+"'));")
                # 删除本组业绩
                self.mysql.sql_execute("DELETE from order_dtd_account where team_id ="+str(int(data['team_id'])))
            # sales表
            promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
            sql="INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '4', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+promoted_dt+"'), '1498552796', UNIX_TIMESTAMP('"+promoted_dt+"'), 'helen_"+sales_id+"', '"+entry_date+"');"
            self.mysql.sql_execute(sql)
            # promoted_path表
            self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)
            for i in range(1,int(data['position_id'])):
                promoted_dt = self.time_handle.get_timeByMonth(-7+i)
                if i == (int(data['position_id'])-1):
                    promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
        # 删除团队后半年业绩
        if data['team_type']!='':
            self.mysql.sql_execute("DELETE  from order_dtd_account where team_id="+str(int(data['team_id']))+" and FROM_UNIXTIME(created_dt) between date_sub('2017-12-01',interval 5 month) and '2017-12-01'")

    def test_06insert_orderDTDAmount(self):
        '''插入7至12月的业绩'''
        for i in range(7,13):
            date = '2017-'+str(i)+'-01'
            for data in orderDTDAmount_data:
                if data['amount_'+str(i)]!='':
                    data['amount']= data['amount_'+str(i)]
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_07insertSalary(self):
        '''生成7至12月的结算数据'''
        for i in range(7,13):
            month = '2017-'+str(i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_08checkResult(self,data ):
        '''检查直辖部年终奖'''
        sales_id = str(int(data['salesId']))
        if data['bonusAYear']!='':
            try:
                if str(data['bonusAYear'])!='空':
                    bonusFromDatabase = self.mysql.get_data("SELECT district_year_end_b from salary_component WHERE date='2017-12-01' and sales_id="+sales_id)[0][0]
                    self.assertTrue(float(bonusFromDatabase)==float(data['bonusAYear']))
                else:
                    bonusCount = self.mysql.get_data("SELECT COUNT(*) from salary_component where sales_id="+sales_id+" and date='2017-12-01';")[0][0]
                    self.assertTrue(int(bonusCount)==0)
            except Exception as e:
                print sales_id
                raise e