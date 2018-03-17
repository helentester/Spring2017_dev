# coding:utf-8
__author__ = 'Helen'
'''
description:登录页面
'''
from src.common.Base_Page import BasePage
from selenium.webdriver.common.by import By


class login_page(BasePage):
    # 定位器
    username_loc = (By.NAME,'username')
    password_loc = (By.NAME,'password')
    submit_btn_loc = (By.CSS_SELECTOR,'.el-button.login-btn.el-button--primary')

    def input_username(self,username):
        self.send_keys(username,*self.username_loc)

    def input_password(self,password):
        self.send_keys(password,*self.password_loc)

    def click_submit_btn(self):
        self.find_element(*self.submit_btn_loc).click()
