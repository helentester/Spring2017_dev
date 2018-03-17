﻿# coding:utf-8
__author__ = 'Helen'
'''
description:配置全局参数
'''
import time,os

# 获取项目路径
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)[0]), '.'))
project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), '.'))
# 测试用例代码存放路径（用于构建suite,注意该文件夹下的文件都应该以test开头命名）
test_case_path = project_path+"\\src\\test_cases"
# excel测试数据文档存放路径
test_data_path = project_path+"\\data\\spring2017_data.xlsx"
# 日志文件存储路径
log_path = project_path+"\\log\\mylog.log"
# print u'日志路径：'+log_path
# 测试报告存储路径，并以当前时间作为报告名称前缀
report_path = project_path+"\\report\\"
report_name = report_path+time.strftime('%Y%m%d%H%S', time.localtime())
# 异常截图存储路径,并以当前时间作为图片名称前缀
img_path = project_path+"\\screenshot_img\\"+time.strftime('%Y%m%d%H%S', time.localtime()) + '_'
# 测试项目所有用图片路径
img_for_test_path = project_path + "\\imgForTest\\imgForAutoTest.png"
# 设置发送测试报告的公共邮箱、用户名和密码
smtp_sever = 'smtp.qq.com'  # 邮箱SMTP服务，各大运营商的smtp服务可以在网上找，然后可以在foxmail这些工具中验正
<<<<<<< HEAD
email_name = "542****6@qq.com"  # 发件人名称
email_password = "bgdz****j"  # 发件人登录密码
email_To = '542730016@qq.com;lihailing@xsteach.com'  # 收件人
=======
email_name = "542**16@qq.com"  # 发件人名称
email_password = "**"  # 发件人登录密码
email_To = '542730016@qq.com;lihailing@xsteach.com'  # 收件人
>>>>>>> 2d94fd39d49c40b509189c1328ae9f411f526886
