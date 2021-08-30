# -*- coding: UTF-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import parseaddr, formataddr
import time as Time

# 发送dashboard日报邮件
def send_mail(img_names):
    sender = 'meng.li@forceclouds.com'
    to_address = ['meng.li@forceclouds.com']
    username = 'meng.li@forceclouds.com'
    password = 'Limeng123456'
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = '监控日报'
    msgRoot['From'] = sender
    msgRoot['To'] = ",".join( to_address ) # 发给多人

    content = ''
    for num in range(len(img_names)):
        content += '<html><head><style>#string{text-align:center;font-size:25px;}</style><div id="string">监控面板-%d<div></head><body><img src="cid:image1%d" alt="image1"></body></html>' % ( (num+1),(num+1) )
    msgRoot.attach(MIMEText(content, 'html', 'utf-8'))
    # 获取图片
    for num, img_name in enumerate(img_names):
        with open(img_name, 'rb') as fp:
            img_data = fp.read()
        msgImage = MIMEImage(img_data)
        msgImage.add_header('Content-ID', '<image1%d>' % (num+1)) # 该id和html中的img src对应
        msgRoot.attach(msgImage)

        # 将图片作为附件
        image = MIMEImage(img_data, _subtype='octet-stream')
        image.add_header('Content-Disposition', 'attachment', filename=img_names[num])
        msgRoot.attach(image)

    smtp = smtplib.SMTP_SSL('smtp.forceclouds.com:465')
    smtp.login(username, password)
    smtp.sendmail(sender, to_address, msgRoot.as_string())
    smtp.quit()

# 发送失败提醒邮件
def send_failed_mail():
    sender = 'meng.li@forceclouds.com'
    to_address = []
    username = 'meng.li@forceclouds.com'
    password = 'Limeng123456'
    msgRoot = MIMEMultipart('related')
    time_now = int(Time.time())
    time_local = Time.localtime(time_now)
    dt = Time.strftime("%Y%m%d",time_local)
    msgRoot['Subject'] = '监控日报图获取失败-' + dt
    msgRoot['From'] = sender
    msgRoot['To'] = ",".join( to_address ) # 发给多人

    content = MIMEText("Dashboard图片下载失败",'utf-8')
    msgRoot.attach(content)

    smtp = smtplib.SMTP_SSL('smtp.forceclouds.com:465')
    smtp.login(username, password)
    smtp.sendmail(sender, to_address, msgRoot.as_string())
    smtp.quit()
