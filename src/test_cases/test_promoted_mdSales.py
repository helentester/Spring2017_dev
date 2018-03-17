# coding:utf-8
__author__ = 'Helen'
'''
description:行销晋升维持测试
'''
import ddt,unittest
from random import choice
from src.common import mysql_connect, time_Handle
from src.common.excel_data import excel
import public_modelu
# 测试数据
excel_data = excel()
orderDTDAmount_data = excel_data.get_list("promoted_md")

@ddt.ddt
class test_promoted_mdSales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mysql = mysql_connect.mysql_connect()
        cls.time_handle = time_Handle.time_Handle()
        cls.pu = public_modelu.public_modelu()
        cls.sales_down_md1 = []     # 可降级的行销主任
        cls.sales_down_md2 = []     # 可降级的高级行销主任
        cls.sales_down_md3 = []     # 可降级的资深行销主任
        cls.sales_down_md4 = []     # 可降级的行销经理
        cls.sales_up_md2 = []       # 可晋升到高级行销主任的账号
        cls.sales_up_md3 = []       # 可晋升到资深行销主任的账号
        cls.sales_up_md4 = []       # 可晋升到行销经理的账号

    @ddt.data(*orderDTDAmount_data)
    def test_01checkTestData(self,data):
        '''检查测试数据'''
        sales_id = str(int(data['salesId']))
        promoted_dt = self.time_handle.get_timeByMonth(-int(data['promoted_dt']))
        # -----处理sales表
        self.mysql.sql_execute("DELETE from sales where id="+sales_id)
        self.mysql.sql_execute("INSERT INTO `spring2017`.`sales` (`id`, `breeder_id`, `team_id`, `position_id`, `status`, `is_delete`, `promoted_dt`, `created_dt`, `updated_dt`, `name`, `entry_date`) VALUES ('"+sales_id+"', '8397617', '67', '"+str(int(data['position_id']))+"', '"+str(int(data['status']))+"', '"+str(int(data['is_delete']))+"', UNIX_TIMESTAMP('"+str(promoted_dt)+"'), UNIX_TIMESTAMP('2017-05-01'), UNIX_TIMESTAMP('2017-05-01'), 'helen_"+sales_id+"', '2017-05-01');")
        # ----处理promotion_path表
        self.mysql.sql_execute("DELETE from promotion_path where sales_id="+sales_id)
        from_position_id = int(data['position_id'])-1
        if int(data['position_id'])==10:
            from_position_id=choice([2,3])   # 随机从正式班主任或津贴金牌班主任晋升
        self.mysql.sql_execute("INSERT INTO `spring2017`.`promotion_path` ( `sales_id`, `from_team_id`, `to_team_id`, `ft_leader_id`, `tt_leader_id`, `from_position_id`, `to_position_id`, `type`, `promoted_dt`, `operator_id`) VALUES ('"+sales_id+"', '67', '67', '8397617', '8397617', '"+str(from_position_id)+"', '"+str(int(data['position_id']))+"', '2', UNIX_TIMESTAMP('"+promoted_dt+"'), '15');")
        # ----处理order_dtd_account，删除业绩
        self.mysql.sql_execute("DELETE from order_dtd_account where sales_id="+sales_id)

    def test_02insert_orderDTDAmount(self):
        '''插入最近4个月的业绩'''
        for i in range(4,0,-1):
            for data in orderDTDAmount_data:
                data['amount'] = data['amount_'+str(i)]
                date = self.time_handle.get_timeByMonth(-i)
                self.pu.insert_orderDTDAmount(data)
                top_id = self.mysql.get_data("select id from order_dtd_account ORDER BY id DESC LIMIT 1")[0][0]
                self.mysql.sql_execute("UPDATE order_dtd_account set created_dt=UNIX_TIMESTAMP('"+str(date)+"') where id="+str(top_id))

    def test_03insertSalary(self):
        '''删除前4个月的结算数据，再生成前4个月的结算数据'''
        current_month = self.time_handle.get_Current_Month()
        for i in range(4,0,-1):
            month = self.time_handle.get_YearMonth(current_month-i)
            self.pu.SettlementData_delete(month)
            self.pu.SettlementData_insert(month)

    def test_04getResult(self):
        '''获取晋升结果列表'''
        result = self.pu.IF_position_change_test()
        for md1_down in result['keepMd1Sales']:
            self.sales_down_md1.append(md1_down['sales_id'])
        for md2_down in result['keepMd2Sales']:
            self.sales_down_md2.append(md2_down['sales_id'])
        for md3_down in result['keepMd3Sales']:
            self.sales_down_md3.append(md3_down['sales_id'])
        for md4_down in result['keepMd4Sales']:
            self.sales_down_md4.append(md4_down['sales_id'])
        for md1_up in result['md2Sales']:
            self.sales_up_md2.append(md1_up['sales_id'])
        for md2_up in result['md3Sales']:
            self.sales_up_md3.append(md2_up['sales_id'])
        for md3_up in result['md4Sales']:
            self.sales_up_md4.append(md3_up['sales_id'])

    @ddt.data(*orderDTDAmount_data)
    def test_05checkResult(self,data):
        '''检查行销路线4个职位的晋升维持结果'''
        sales_id = int(data['salesId'])
        p = int(data['promoted_type'])
        try:
            if p == -1:
                self.assertIn(sales_id, self.sales_down_md1)
            elif p == -2:
                self.assertIn(sales_id, self.sales_down_md2)
            elif p == -3:
                self.assertIn(sales_id, self.sales_down_md3)
            elif p == -4:
                self.assertIn(sales_id, self.sales_down_md4)
            elif p == 11:
                self.assertNotIn(sales_id, self.sales_down_md1+self.sales_up_md2)
            elif p == 22:
                self.assertNotIn(sales_id, self.sales_down_md2+self.sales_up_md3)
            elif p == 33:
                self.assertNotIn(sales_id, self.sales_down_md3+self.sales_up_md4)
            elif p == 44:
                self.assertNotIn(sales_id, self.sales_down_md4)
            elif p == 2:
                self.assertIn(sales_id, self.sales_up_md2)
            elif p == 3:
                self.assertIn(sales_id, self.sales_up_md3)
            elif p == 4:
                self.assertIn(sales_id, self.sales_up_md4)
            else:   # 冻结或删除状态不出现在晋升和降级列表
                self.assertNotIn(sales_id,self.sales_down_md1+self.sales_down_md2+self.sales_down_md3+self.sales_down_md4+self.sales_up_md2+self.sales_up_md3+self.sales_up_md4)
        except Exception as e:
            print "sales_id="+str(sales_id)+"    promoted_type="+str(p)
            raise e
