# coding:utf-8
# @DATE    : 2018/1/26
__author__ = 'Helen'
'''
description:资深销售经理晋升维持考核
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("promoted_SSM")

@ddt.ddt
class test_promoted_SSMSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()
        cls.keepSSMSales = []    # 销售经理降级列表
        cls.BDSales = []   # 晋升列表

    @ddt.data(*orderDTDAmount_data)
    def Ttest_01deleteDataForTest(self,data):
        '''清理数据'''
        # sales+业绩
        self.mysql.sql_execute("DELETE from sales where id="+str(int(data['salesId'])))
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+str(int(data['salesId'])))
        # team+业绩
        if data['team_type']!='':
            self.mysql.sql_execute("DELETE from team where id="+str(int(data['team_id'])))
            self.mysql.sql_execute("DELETE from order_dtd_account where team_id="+str(int(data['team_id'])))
        # promotion_path
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+str(int(data['salesId'])))

    @ddt.data(*orderDTDAmount_data)
    def Ttest_02insertDataForTest(self,data):
        '''插入测试数据'''
        sales_id = str(int(data['salesId']))
        try:
            # sales
            promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '"+str(int(data['team_id']))+"', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"',UNIX_TIMESTAMP('"+str(promoted_dt)+"'), '1483200000', '0', 'helen_"+sales_id+"', '"+entry_date+"');")
            # team
            if data['team_type']!='':
                self.mysql.sql_execute("INSERT INTO `spring2017`.`team` (`id`, `name`, `parent_id`, `leader_id`, `type`, `status`, `is_delete`, `created_dt`, `updated_dt`) VALUES ('"+str(int(data['team_id']))+"', 'helen组_"+str(int(data['team_id']))+"', '"+str(int(data['team_parent_id']))+"', '"+sales_id+"', '"+str(int(data['team_type']))+"', '0', '0', '0', '0');")
            # promotion_path
            for i in range(1,int(data['position_id'])):
                promoted_dt = self.time_handle.get_timeByMonth(-15+i)
                if i == (int(data['position_id'])-1):
                    promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
                self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '67', '8397617', '8397617', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
        except Exception as e:
            print sales_id
            raise e

    def Ttest_03insert_orderDTDAmount(self):
        '''插入最近12个月的业绩'''
        for i in range(12,0,-1):
            for data in orderDTDAmount_data:
                data['amount'] = data['amount_'+str(i)]
                if data['amount']!='':
                    date = self.time_handle.get_timeByMonth(-i)
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def Ttest_04insertSalary(self):
        '''删除前12个月的结算数据，再生成前12个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(12,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    def test_05getResult(self):
        '''获取晋升结果列表'''
        result = self.pu.IF_position_change_test()
        for SSM in result['keepSsmSales']:
            self.keepSSMSales.append(SSM['sales_id'])
        for BD in result['bdSales']:
            self.BDSales.append(BD['sales_id'])

    @ddt.data(*orderDTDAmount_data)
    def test_06checkResult(self,data):
        '''检查资深销售经理晋升维持结果'''
        sales_id = int(data['salesId'])
        if data['promoted_type']!='':
            try:
                if int(data['promoted_type'])==-1: # 降级
                    self.assertIn(sales_id,self.keepSSMSales)
                elif int(data['promoted_type'])==0: # 维持
                    self.assertNotIn(sales_id,self.keepSSMSales+self.BDSales)
                elif int(data['promoted_type'])==1: # 晋升
                    self.assertIn(sales_id,self.BDSales)
                else: # 异常数据(删除or冻结)
                    self.assertNotIn(sales_id,self.keepSSMSales+self.BDSales)
            except Exception as e:
                print 'sales_id='+str(sales_id)+'   promoted_type='+str(int(data['promoted_type']))
                raise e
