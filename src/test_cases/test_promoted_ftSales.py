# coding:utf-8
__author__ = 'Helen'
'''
description:正式班主任晋升维持测试
'''
import ddt,unittest
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("promoted_ftSales")


@ddt.ddt
class test_ftSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()
        cls.sales_upGT = []  # 可以晋升的账号（金牌班主任）
        cls.sales_upMD = []     # 可以晋升的账号（行销）
        cls.sales_upSL = []     # 可以晋升的账号（销售组长）
        cls.sales_down = []    # 可以解约的账号

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self,data):
        '''检查用于测试的账号数据,并且删除业绩'''
        sales_id = str(int(data['salesId']))
        # 处理时间参数
        entry_date = self.time_handle.get_timeByMonth(-int(data['entry_date']))
        promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
        # -------检查sales表
        self.mysql.sql_execute("delete FROM sales WHERE id="+sales_id)
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '"+str(int(data['breeder_id']))+"', '67', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+str(promoted_dt)+"'), '1498552796', '1498963877', 'helen_"+sales_id+"', '"+str(entry_date)+"');")
        # -------检查promoted_path表
        self.mysql.sql_execute("DELETE FROM promotion_path WHERE sales_id ="+sales_id)  # 先删除已有数据
        for i in range(1,int(data['position_id'])):
            promoted_dt = self.time_handle.get_timeByMonth(-7+i)
            if i == (int(data['position_id'])-1):
                promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
            self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '67', '8397617', '8397617', '"+str(i)+"', '"+str(i+1)+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
        # 删除业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)

    def test_02insert_orderDTDAmount(self):
        '''插入最近三个月的业绩'''
        for i in range(3,0,-1):
            for data in orderDTDAmount_data:
                data['amount'] = data['amount_'+str(i)]
                if data['amount'] !='':
                    self.pu.insert_orderDTDAmount(data)
                    top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                    date = self.time_handle.get_timeByMonth(-i)
                    self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''删除前三个月的结算数据，再生成前三个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(3,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    def test_04getResult(self):
        '''获取晋升结果列表'''
        result = self.pu.IF_position_change_test()
        for downSales in result['keepFtSales']:
            self.sales_down.append(downSales['sales_id'])
        for upSales_gt in result['ftSales']:
            self.sales_upGT.append(upSales_gt['sales_id'])
        for upSales_md in result['md1Sales']:
            self.sales_upMD.append(upSales_md['sales_id'])
        for upSales_sl in result['gtSales']:
            self.sales_upSL.append(upSales_sl['sales_id'])

    @ddt.data(*orderDTDAmount_data)
    def test_05checkResult(self,data):
        '''检查正式班主任晋升维持结果'''
        sales_id = int(data['salesId'])
        if data['promoted_type']!='':
            promoted_type = str(data['promoted_type']).split(',')
            for p in promoted_type:
                try:
                    if int(float(p)) == -1:    # 降级
                        self.assertIn(sales_id,self.sales_down)
                    elif int(float(p)) == 0:   # 维持
                        self.assertNotIn(sales_id,self.sales_down+self.sales_upGT+self.sales_upSL)
                    elif int(float(p)) == 1:   # 晋升行销
                        self.assertIn(sales_id,self.sales_upMD)
                    elif int(float(p)) == 2:   # 晋升金牌
                        self.assertIn(sales_id,self.sales_upGT)
                    elif int(float(p)) == -3:   # 晋升组长
                        self.assertNotIn(sales_id,self.sales_upSL)  # 2017－11需求更改，不能跳过金牌班主任晋升到销售组长
                    else:   # 异常数据(删除or冻结)
                        self.assertNotIn(sales_id,self.sales_down+self.sales_upGT+self.sales_upMD+self.sales_upSL)
                except Exception as e:
                    print 'sales_id='+str(sales_id)+'   promoted_type='+str(p)
                    raise e

    @classmethod
    def tearDownClass(cls):
        pass