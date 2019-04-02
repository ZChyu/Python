# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:52:35 2019

@author: Zcy
"""
from multiprocessing import Pool
import urllib.request as requ
import sifany_util_math
import pymysql
import sifany_util
import time
import json


cicode=[] 
setting={} 
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
def getUrl(url):    
    headers = { 'User-Agent' : user_agent }
    req = requ.Request(url,headers= headers)
    response = requ.urlopen(req)
    the_page = response.read()
    return the_page.decode("utf8")
def getWeather(html,conn,cursor,code):
    timeWeather={}
    try:
        weaInfo=json.loads(html)
        timeWeather['city']=weaInfo['station']['city']
        timeWeather['province']=weaInfo['station']['province']
        timeWeather['publish_time']=weaInfo['publish_time']
        timeWeather['temperature']=weaInfo['weather']['temperature']
        timeWeather['airpressure']=weaInfo['weather']['airpressure']
        timeWeather['humidity']=weaInfo['weather']['humidity']
        timeWeather['rcomfort']=weaInfo['weather']['rcomfort']
        timeWeather['icomfort']=weaInfo['weather']['icomfort']
        timeWeather['info']=weaInfo['weather']['info']
        timeWeather['feelst']=weaInfo['weather']['feelst']
        timeWeather['direct']=weaInfo['wind']['direct']
        timeWeather['power']=weaInfo['wind']['power']
        timeWeather['speed']=weaInfo['wind']['speed']
        timeWeather['cityCode']=code
        sql='SELECT count(*) FROM `new_inf_weather` WHERE cityCode="' +code+ '" AND publish_time="' +str(timeWeather['publish_time'])+'"'
        cursor.execute(sql)
        data=cursor.fetchall()
        if data[0][0]>0:
            pass
        else:
            sifany_util.insert_data(cursor,'new_inf_weather',timeWeather)
            conn.commit()
    except Exception as e:
        print("********  Parse Failed    ********")
        print (e)
        pass
def get_sql_conn():  
    conn= pymysql.connect(host="localhost",user="root",password="root",db="weather_info",port=3306)
    cursor = conn.cursor()
    return conn,cursor

def thread_insert(groups):
#    conn,cursor,setting=sifany_util.get_sql_conn('setting-data.json')
    conn,cursor=get_sql_conn()
    for code in groups:
        try:
            print(code)
            url="http://www.nmc.cn/f/rest/real/"+str(code)
            html=getUrl(url)
            getWeather(html,conn,cursor,code)
        except Exception as e:
            print("********  Insert Failed    ********")
            print (e)
            pass 
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))) 
    print('The end of the current process process')
    
def getCityCodes():
    URL='http://www.nmc.cn/f/rest/province'
    html=getUrl(URL)
    provinceCode=json.loads(html)   
    province=[]
    for i in range(len(provinceCode)):
        province.append(provinceCode[i]['code'])
    for pcode in province:
        url=str('http://www.nmc.cn/f/rest/province/'+str(pcode))
        html=getUrl(url)
        citycode=json.loads(html)    
        for i in range(len(citycode)):
            cicode.append(citycode[i]['code'])
              
def start_Process():
    process=int(setting['processNumber'])
    groupss=sifany_util_math.trans_group(cicode,process)
    p = Pool(process)
    for groups in groupss:
        p.apply_async(thread_insert, args=(groups,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    
if __name__ == '__main__':
    getCityCodes()
    conn,cursor,setting=sifany_util.get_sql_conn('setting-data.json')
    print('---start---')  
    while True:
        start_Process()
        time.sleep(int(setting['sleepTime']))

        
        
        