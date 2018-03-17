# coding:utf-8
__author__ = 'Helen'
'''
description:测试前台首页
'''
import public_modelu
import unittest
from src.pages import index_page

class test_index(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pu = public_modelu.public_modelu()
        #cls.driver = cls.pu.login('helen_14_04','123456')
        #cls.index_page = index_page.index_page(cls.driver)

    def test_my_salesAmount(self):
        '''测试我的累计业绩'''
        #print self.index_page.get_allMysalesAmount()
        self.assertTrue(False)

    @classmethod
    def tearDownClass(cls):
        pass
