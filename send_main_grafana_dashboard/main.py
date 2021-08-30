# -*- coding: UTF-8 -*-

import time
import get_grafana_dashboard
import send_mail
import sys

project = sys.argv[1] 

# 获取面板图并发邮件
img_names = get_grafana_dashboard.download(project)
if (img_names == "fail"): # 下载失败，邮件提醒
    send_mail.send_failed_mail()
else: # 成功则发日报邮件
     send_mail.send_mail(img_names)
print("report end")
