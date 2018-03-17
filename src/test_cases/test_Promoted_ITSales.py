# coding:utf-8
__author__ = 'Helen'
'''
description:实习班主任晋升维持测试(不算当前月的TSC，要往回取6个月)
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("promoted_ITSales")


@ddt.ddt
class test_Promoted_ITSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()
        cls.sales_up = []  # 可以晋升的账号
        cls.sales_down = []    # 可以解约的账号

    @ddt.data(*orderDTDAmount_data)
    def test_01checkDataForTesting(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        #   ---------sales表
        self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '43214329', '67', '1', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+str(entry_date)+"'), '1498552796', '1498963877', 'helen_"+sales_id+"', '"+str(entry_date)+"');")
        #   -------promoted_path表
        self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)
        self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` (`sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '0', '67', '0', '8397617', '0', '1', '1', UNIX_TIMESTAMP('"+str(entry_date)+"'), '0');")
        # ----删除业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id ="+sales_id)

    def test_02insert_orderDTDAmount(self):
        '''插入六个月数据并生成结算数据'''
        for i in range(6,0,-1):
            date = self.time_handle.get_timeByMonth(-i)
            # 插入业绩
            for data in orderDTDAmount_data:
                data['amount'] = data['amount_'+str(i)]
                if data['amount']!='':
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''删除前6个月的结算数据，再生成前6个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(6,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    def test_04getResult(self):
        '''获取晋升结果列表'''
        result = self.pu.IF_position_change_test()
        for downSales in result['keepItSales']:
            self.sales_down.append(downSales['sales_id'])
        for upSales in result['itSales']:
            self.sales_up.append(upSales['sales_id'])

    @ddt.data(*orderDTDAmount_data)
    def test_05checkResult(self,data):
        '''检查实习班主任晋升维持结果'''
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