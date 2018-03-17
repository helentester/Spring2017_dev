# coding:utf-8
__author__ = 'Helen'
'''
description:时间处理函数
'''
import time,datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

class time_Handle():
    def __init__(self):
        self.now = time.localtime()

    def get_YearMonthDay(self,get_time):
        '''传递时间参数，返回格式为YYYY-mm-dd格式的时间'''
        return datetime.datetime.strptime(get_time,'%Y-%m-%d')

    def get_Current_YearMonthDay(self):
        '''获取当前年月日，返回：YYYY-mm-dd'''
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def get_Current_YearMonth(self):
        '''获取当前年月，返回格式为：YYYY-mm'''
        return '%d-%02d'%(self.now.tm_year,self.now.tm_mon)

    def get_YearMonth(self,month):
        #根据月份递减,返回年月：YYYY-mm
        current_year = self.get_Current_Year()
        if month<=0:
            month = month+12
            current_year = current_year - 1
        return str(current_year)+"-"+str(month)

    def get_Current_Year(self):
        '''获取当年份'''
        return self.now.tm_year

    def get_Current_Month(self):
        '''获取当前月份'''
        return self.now.tm_mon

    def get_months(self,start_date,end_date):
        '''获取时间差(月份)'''
        months = rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)
        return months.count()

    def get_timeByMonth(self,month):
        '''根据月份加减时间'''
        d = datetime.date(self.now.tm_year, self.now.tm_mon, self.now.tm_mday)
        targetDate = d + relativedelta(months=month)
        return str(targetDate)