# coding:utf-8
__author__ = 'Helen'
'''
description:销售组长晋升测试
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("promoted_SLSales")


@ddt.ddt
class test_promoted_SLSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()
        cls.sales_up = []     # 可以晋升的账号
        cls.sales_down = []    # 可以降级的账号

    @ddt.data(*orderDTDAmount_data)
    def test_01deleteDataForTest(self,data):
        '''清理数据'''
        # sales
        self.mysql.sql_execute("DELETE from sales where id="+str(int(data['salesId'])))
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+str(int(data['salesId'])))
        # team
        if int(data['position_id']) in(4,5):
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id="+str(int(data['team_id'])))
        # promotion_path
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+str(int(data['salesId'])))

    @ddt.data(*orderDTDAmount_data)
    def test_02insertTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        date = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
        # ------检查team表
        if int(data['position_id']) in(4,5):
            self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helenTeam_"+str(int(data['team_id']))+"', '69', '"+sales_id+"', '1', '0', '0', UNIX_TIMESTAMP('"+str(date)+"'), UNIX_TIMESTAMP('"+str(date)+"'));")
            # ------检查sales表
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+str(date)+"'), UNIX_TIMESTAMP('2017-01-01'), UNIX_TIMESTAMP('"+str(date)+"'), 'helen_"+sales_id+"', '2017-01-01');")
        # ------检查promoted_path表
        for i in range(1,int(data['position_id'])):
            promoted_dt = self.time_handle.get_timeByMonth(-7+i)
            if i == (int(data['position_id'])-1):
                promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '67', '8397617', '8397617', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")

    def test_03insert_orderDTDAmount(self):
        '''插入近7个月的业绩'''
        for i in range(7,0,-1):
            date = self.time_handle.get_timeByMonth(-i)
            for data in orderDTDAmount_data:
                try:
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    data['amount']= data['amount_'+str(i)]
                    self.pu.insert_orderDTDAmount(data)
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))
                except Exception as e:
                    print data['salesId']
                    raise e

    def test_04insertSalary(self):
        '''生成7个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(7,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    def test_05getResult(self):
        '''获取晋升结果列表'''
        result = self.pu.IF_position_change_test()
        for SL in result['keepSlSales']:
            self.sales_down.append(SL['sales_id'])
        for SSL in result['slSales']:
            self.sales_up.append(SSL['sales_id'])

    @ddt.data(*orderDTDAmount_data)
    def test_06checkResult(self,data):
        '''检查销售组长晋升维持结果'''
        sales_id = int(data['salesId'])
        if data['promoted_type']!='':
            try:
                if int(data['promoted_type'])==-1: # 降级
                    self.assertIn(sales_id,self.sales_down)
                elif int(data['promoted_type'])==0: # 维持
                    self.assertNotIn(sales_id,self.sales_down+self.sales_up)
                elif int(data['promoted_type'])==1: # 晋升
                    self.assertIn(sales_id,self.sales_up)
                else: # 异常数据(删除or冻结)
                    self.assertNotIn(sales_id,self.sales_down+self.sales_up)
            except Exception as e:
                print 'sales_id='+str(sales_id)+'   promoted_type='+str(int(data['promoted_type']))
                raise e

    @classmethod
    def tearDownClass(cls):
        pass