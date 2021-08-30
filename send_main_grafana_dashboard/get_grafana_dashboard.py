# -*- coding: UTF-8 -*-

import os,stat
import urllib.request
from datetime import datetime, date, time, timedelta
import time as Time


# 获取七日前0点与今日0点的时间戳
def last_seven_day():
    midnight = datetime.combine(date.today(), time.min)
    yesterday_mid = midnight - timedelta(days=7) # 想要此前几天的，就改这个参数
    epoch = datetime.utcfromtimestamp(0)
    midnight = midnight - timedelta(seconds=1)
    midnight = int((midnight - epoch).total_seconds() * 1000.0)
    yesterday_mid = int((yesterday_mid - epoch).total_seconds() * 1000.0)
    return str(yesterday_mid), str(midnight)


# 下载指定的dashboard
dashboard_id = [13,7,157,174,156,158]
def download(project):
    # 组装url，跑代码之前现在浏览器试试
    grafana_server = 'https://grafana.xxxxxx.com/'
    uid = '9CWBz0bik'
    Type = 'instance-monitoring'

    auth_token='xxxxxxxxxxxxxxxxxxxx'
    header = {'Authorization': 'Bearer ' + auth_token} # 用管理员去Grafana生成API Key

    time_now = int(Time.time())
    time_local = Time.localtime(time_now)
    dt = Time.strftime("%Y-%m-%d",time_local)

    file_list = []
    for i in dashboard_id:
        url = (grafana_server + 'render/d-solo/' + uid + '/' + Type + '?orgId=1&var-job=node-exporter&var-hostname=' + project + '&var-node=All&var-maxmount=%2Fdata&var-env=&var-name=&from=' +  last_seven_day()[0] + '&to=' + last_seven_day()[1] + '&panelId=' + str(i)  + '&width=1000&height=500&tz=Asia%2FShanghai')
        request = urllib.request.Request(url,headers=header)

        # 访问并下载面板图
        response = urllib.request.urlopen(request)
        img_name = (project + '-' + str(i) + '-' + dt + ".png")
        filename = '/data/grafana_dashboard_mail/images/' + img_name
        if (int(response.getcode()) == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) 
        else:
            return 'fail'

        file_list.append(filename)

    return file_list
