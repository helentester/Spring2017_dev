# coding:utf-8
__author__ = 'Helen'
'''
description:增部奖
'''
import ddt,unittest,datetime
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("bonusForAddDept")


@ddt.ddt
class test_bonusForAddDept(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()

    @ddt.data(*orderDTDAmount_data)
    def test_01checkDataForTesting(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        # 删除测试账号的业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)
        # -------team表
        if data['team_type'] !='':
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            team_Created = self.time_handle.get_timeByMonth(-int(data['team_Created']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helenTeam_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', UNIX_TIMESTAMP('"+team_Created+"'), UNIX_TIMESTAMP('"+team_Created+"'));")
            # 删除本组业绩
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id="+str(int(data['team_id'])))
        #   ---------sales表
        self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
        promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        sql="INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+promoted_dt+"'), '1498552796', UNIX_TIMESTAMP('"+promoted_dt+"'), 'helen_"+sales_id+"', '"+entry_date+"');"
        self.mysql.sql_execute(sql)
        #   -------promoted_path表
        self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)
        for i in range(1,int(data['position_id'])):
            promoted_dt = self.time_handle.get_timeByMonth(-7+i)
            if i == (int(data['position_id'])-1):
                promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")

        # 设计降级后再升级的数据
        if sales_id=='43214445':
            promoted_dt = self.time_handle.get_timeByMonth(-2)
            top_id = self.mysql.get_data("SELECT id from promotion_path where sales_id = 43214445 ORDER BY id DESC LIMIT 1")[0][0]
            self.mysql.sql_execute("UPDATE promotion_path SET promoted_dt=UNIX_TIMESTAMP('"+promoted_dt+"') where id="+str(top_id))
            promoted_dt = self.time_handle.get_timeByMonth(-1)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '6', '5', '3', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
            promoted_dt = self.time_handle.get_timeByMonth(0)
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '"+str(int(data['team_id']))+"', '8397617', '4', '5', '6', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")

    def test_02insert_orderDTDAmount(self):
        '''插入13个月的业绩'''
        for i in range(13,0,-1):
            date = self.time_handle.get_timeByMonth(-i)
            for data in orderDTDAmount_data:
                team_created = self.mysql.get_data("SELECT FROM_UNIXTIME(created_dt) from team where id="+str(int(data['team_id'])))[0][0]
                amount_dt = datetime.datetime.strptime(date,'%Y-%m-%d')
                if team_created>amount_dt:
                    pass
                else:
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''删除前12个月的结算数据，再生成前12个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(12,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_04insertBonus(self,data):
        '''插入增部奖总记录，设计已有增部奖按12个月发放的情况'''
        if data['send_date']!='':
            self.mysql.sql_execute("DELETE FROM bonus_department_promotion where from_before_team_id="+str(int(data['team_id'])))
            date = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`bonus_department_promotion` (`sales_id`, `date`, `from_sales_id`, `from_before_team_id`, `from_before_team_tsc`, `royalty_rate`, `amount`, `times`, `created_dt`) VALUES ('"+str(int(data['breeder_id']))+"', '"+date+"', '"+str(int(data['salesId']))+"', '"+str(int(data['team_id']))+"', '"+str(float(data['bonus_all'])*12)+"', '0.01', '"+str(float(data['bonus_all']))+"', '"+str(int(data['send_date']))+"', UNIX_TIMESTAMP('"+date+"'));")

    def test_05insertSalary(self):
        '''生成当月结算数据'''
        month = self.time_handle.get_Current_YearMonth()
        self.pu.SettlementData_delete(month)
        self.pu.SettlementData_insert(month)

    @ddt.data(*orderDTDAmount_data)
    def test_06checkResult(self,data ):
        '''检查增部奖'''
        sales_id = str(int(data['salesId']))
        # 检查增部奖获得情况
        if data['bonus_all']!='':
            try:
                if str(data['bonus_all'])!=u'空':
                    bonusAll_database = self.mysql.get_data("SELECT amount from bonus_department_promotion where  sales_id="+str(int(data['breeder_id']))+" and from_before_team_id="+str(int(data['team_id'])))[0][0]
                    self.assertTrue(float(data['bonus_all'])==float(bonusAll_database))
                else:
                    bonusAll_count = self.mysql.get_data("SELECT COUNT(*) from bonus_department_promotion where sales_id="+str(int(data['breeder_id']))+" and from_before_team_id="+str(int(data['team_id'])))[0][0]
                    self.assertTrue(int(bonusAll_count)==0)
            except Exception as e:
                print str(int(data['breeder_id']))+u"：增部奖（总）不正确"
                raise e
        # 检查增部奖每月发放情况
        if data['bonus_month']!='':
            try:
                if str(data['bonus_month'])!=u'空':
                    bonusFromDatabase = self.mysql.get_data("SELECT dept_promotion_b from salary_component WHERE DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m') and sales_id="+sales_id)[0][0]
                    self.assertTrue(float(data['bonus_month'])==float(bonusFromDatabase))
                else:
                    bonusCount = self.mysql.get_data("SELECT COUNT(*) from salary_component where sales_id ="+sales_id+" AND DATE_FORMAT(date,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')")[0][0]
                    self.assertTrue(int(bonusCount)==0)
            except Exception as e:
                print sales_id+u"：每月发放的增部奖不正确"
                raise e

