# coding:utf-8
__author__ = 'Helen'
'''
description:首页
'''
from config import globalparameter as gl
from src.common.Base_Page import BasePage
from selenium.webdriver.common.by import By


class index_page(BasePage):
    # 定位器
    login_link_loc = (By.CSS_SELECTOR, '.loginBox.ml30.fr>li>a:nth-child(1)')
    user_icon_loc = (By.CLASS_NAME, 'userPic')
    classes_link_loc = (By.XPATH, 'html/body/header/div/div[1]/ul/li[2]/a')
    all_MySalesAmount_loc = (By.XPATH, ".//*[@id='app']/div[2]/div/div/div[2]/div[1]/div[1]/dl[1]/dd[1]") # 我的累计业绩
    thisMonth_MySalesAmount_loc = (By.CSS_SELECTOR, '.index-box.index-box-first>dd:nth-child(2)') # 我的本月业绩
    lastMonth_MySalesAmount_loc = (By.CSS_SELECTOR, '.index-box.index-box-first>dd:nth-child(3)') # 我的上月业绩
    all_mySalary_loc = (By.CSS_SELECTOR,'.index-box.index-box-first>dd:nth-child(4)')   # 我的累计绩效
    lastMonth_mySalary_loc = (By.CSS_SELECTOR,'.index-box.index-box-first>dd:nth-child(5)')   # 我的上月绩效
    all_teamSalesAmount_loc = (By.CSS_SELECTOR,'.index-box>dd:nth-child(1)')    # 团队累计业绩
    thisMonth_teamSalesAmount_loc = (By.CSS_SELECTOR,'.index-box>dd:nth-child(2)')   # 团队本月业绩
    lastMonth_teamSalesAmount_loc = (By.CSS_SELECTOR,'.index-box>dd:nth-child(3)')   # 团队上月业绩
    all_teamSalary_loc = (By.CSS_SELECTOR,'.index-box>dd:nth-child(4)') # 团队累计绩效
    lastMonth_teamSalary_loc = (By.CSS_SELECTOR,'.index-box>dd:nth-child(5)')   # 团队上月绩效

    #   团队累计业绩
    def get_allTeamSalesAmount(self):
        s = self.find_element(*self.all_teamSalesAmount_loc).text
        return s[7:]

    # 团队本月业绩
    def get_thisMonthTeamSalesAmount(self):
        s = self.find_element(*self.thisMonth_teamSalesAmount_loc).text
        return s[7:]

    # 团队上月业绩
    def get_lastMonthTeamSalesAmount(self):
        s = self.find_element(*self.lastMonth_teamSalesAmount_loc).text
        return s[7:]

    # 团队累计绩效
    def get_allTeamSalary(self):
        s = self.find_element(*self.all_teamSalary_loc).text
        return s[7:]

    # 团队上月绩效
    def get_lastMonthTeamSalary(self):
        s = self.find_element(*self.lastMonth_teamSalary_loc).text
        return s[7:]

    # 我的累计业绩
    def get_allMysalesAmount(self):
        s = self.find_element(*self.all_MySalesAmount_loc).text
        print s
        return s[7:]

    # 我的上月业绩
    def get_lastMonthMysalesAmount(self):
        s = self.find_element(*self.lastMonth_MySalesAmount_loc).text
        return s[7:]

    # 我的本月业绩
    def get_thisMonthMysalesAmount(self):
        s = self.find_element(*self.thisMonth_MySalesAmount_loc).text
        return s[7:]

    #  我的累计绩效
    def get_allMySalary(self):
        s = self.find_element(*self.all_mySalary_loc).text
        return s[7:]

    #  我的上月绩效
    def get_lastMonthMySalary(self):
        s = self.find_element(*self.lastMonth_mySalary_loc).text
        return s[7:]

    # 点击登录链接
    def click_login_linck(self):
        self.find_element(*self.login_link_loc).click()

    # 用户头像图片
    def user_icon(self):
        return self.find_element(*self.user_icon_loc).is_displayed()

    # 点击课程链接
    def click_classes_link(self):
        self.find_element(*self.classes_link_loc).click()
