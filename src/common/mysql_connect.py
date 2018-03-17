# coding:utf-8
__author__ = 'Helen'
'''
description:链接mysql数据库
'''
import MySQLdb


class mysql_connect:
    def __init__(self):
        pass
    # 链接数据库
    def connect(self):
        self.conn= MySQLdb.connect(
                host='192.168.6.245',
                port = 3306,
                user='spring',
                passwd='spring2017',
                db ='spring2017',
                charset='utf8'  # 加上该属性避免输入中文乱码（没有该属性写入中文会乱码）
        )
        self.cur = self.conn.cursor()
        return self.cur

    # 执行SQL
    def sql_execute(self,sql_statement):
        try:
            cur = self.connect()
            cur.execute(sql_statement)
            self.close_connect()
        except Exception,e:
            raise e

    # 执行SQL并返回结果
    def get_data(self,sql_statement):
        try:
            cur = self.connect()
            cur.execute(sql_statement)
            #data = cur.fetchone()
            data = cur.fetchall()
            self.close_connect()
            return data
        except Exception,e:
            raise e

    # 关闭链接
    def close_connect(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()