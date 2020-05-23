#encoding: utf-8
import sys
import http.cookiejar
import urllib.parse
import codecs
import urllib.request
import time
from twilio.rest import Client
import os
import re
from hashlib import md5
import random
import uuid
 
def str_clear(string):
    string=''.join(string)
    string=string.strip("\n")
    return string

def morning():
    t = random.uniform(35.0,37.5)
    g = str(t)
    g = g[:4]
    return(g)

def afternoon():
    t = random.uniform(35.0,37.5)
    g = str(t)
    g = g[:4]
    return(g)

def evening():
    t = random.uniform(35.0,37.5)
    g = str(t)
    g = g[:4]
    return(g)

dir=os.getcwd()#Change
if not os.path.exists(dir+'//Data'):
    os.makedirs(dir+'//Data')
if not os.path.exists(dir+'//status'):
    os.makedirs(dir+'//status')
items = os.listdir(dir+'//Data')
datalist = []
for names in items:
  if names.endswith(".hel"):
    datalist.append(names)
for i in range(0,len(datalist)):
    print('#################################################################################')
    file_now=str(datalist[i])
    file_name=file_now.split('.',1)
    file_name=file_name[0]
    if not os.path.exists(dir+'//status//status_health'+file_name+'.sta'):
        w=open(dir+'//status//status_health'+file_name+'.sta','w',encoding='utf-8')
        w.close
    now=time.strftime('%y%m%d%H')
    minute=time.strftime('%M')
    print('minute:'+minute)
    hour=int(now[-2:])
    print('hour:'+ str(hour))
    now=list(now)
    h = open(dir+'//Data//'+file_now,'r',encoding='utf-8')
    all = h.readlines()
    h.close()
    Uid=all[0:1]
    Pwd=all[1:2]
    IdCard=all[2:3]
    Uid=str_clear(Uid)
    Pwd=str_clear(Pwd)
    IdCard=str_clear(IdCard)

    UA='Mozilla/1.0 (iPhone; CPU iPhone OS 1_0_0 like Mac OS X) AppleWebKit/105.0.00 (KHTML, like Gecko) Version/1.0.0 Mobile/10A001 Safari/100.0'

    uuid_num=uuid.uuid4()
    print('uuid:'+str(uuid_num))
    Pwd=urllib.parse.quote(Pwd)
    print(Pwd)
    url = "http://xgsys.swjtu.edu.cn/SPCPTest/Web/Account/IdCardLogin"
    raw_po='txtUid='+str(Uid)+'&txtPwd='+str(Pwd)+'&txtIdCard='+str(IdCard)+'&codeInput='
    print(raw_po)
    header = {
        'Referer': 'http://xgsys.swjtu.edu.cn/SPCPTest/Web',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UA,
        'Accept-Encoding': 'gzip, deflate',
        'Content-Length': '69',
        'Host': 'xgsys.swjtu.edu.cn',
        'Connection': 'keep-alive',
    }
    raw_po_e=raw_po.encode('utf-8')
    req=urllib.request.Request(url=url,headers=header,data=raw_po_e)
    cj = http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = opener.open(req)
    cookieStr = ''
    for item in cj:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'
    print(cookieStr)
    url_request="http://xgsys.swjtu.edu.cn/SPCPTest/Web/Temperature/StuTemperatureInfo"
    header_selfdefine={
        'Host': 'xgsys.swjtu.edu.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://xgsys.swjtu.edu.cn',
        'User-Agent': UA,
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://xgsys.swjtu.edu.cn/SPCPTest/Web/Temperature/StuTemperatureInfo',
        'Content-Length': '103',
        'Cookie': cookieStr,
        'Connection': 'keep-alive'
    }
    f = open(dir+'//status//status_health'+file_name+'.sta','r',encoding='utf-8')
    data = f.readlines()
    f.close()
    now=list(now)
    now.insert(2,'-')
    now.insert(5,'-')
    now.insert(8,'-')
    print('time:'+str(now))
    now=''.join(now)
    date='20'+str(now)
    print(date)
    hour_b=data[0]
    hour_b=hour_b[-2:]
    print('last_time:'+hour_b)
    if hour<12:
        temp=morning()
    elif hour<16:
        temp=afternoon()
    else:
        temp=evening()
    print('temp:'+str(temp))
    temp_1=temp[0:2]
    temp_2=temp[-1:]
    raw_post='TimeNowHour='+str(hour)+'&TimeNowMinute='+minute+'&Temper1='+temp_1+'&Temper2='+temp_2+'&ReSubmiteFlag='+str(uuid_num)
    print('ext_time:'+str(abs(hour_b-hour)))
    if not(date in data):
        if abs(hour_b-hour)>3:
            for t in range (0,100):
                print("request")
                print(raw_post)
                raw_e=raw_post.encode('utf-8')
                request_obj=urllib.request.Request(url=url_request,headers=header_selfdefine,data=raw_e)
                response_obj=urllib.request.urlopen(request_obj)
                html_code=response_obj.read().decode('utf')
                print(html_code)
                if '每次填报间隔时间应不能小于4小时' in html_code:
                    print('每次填报间隔时间应不能小于4小时')
                    break
                if '今天填报次数已完成，勿需再次填报' in html_code:
                    print('今天填报次数已完成，勿需再次填报')
                    break
                if '未在填报时间段（每天7点到20点）中，不能进行填报操作' in html_code:
                    print('未在填报时间段（每天7点到20点）中，不能进行填报操作')
                    break
                status=response_obj.status
                print(response_obj.status)
                if '填报成功' in html_code:
                    w=open(dir+'//status//status_health'+file_name+'.sta','w',encoding='utf-8')
                    w.write(date)
                    w.close
                    print(date+"上报成功")
                    break
                else:
                    time.sleep(10)
            else:
                print('错误')
                time.sleep(10)
