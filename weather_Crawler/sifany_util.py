# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:33:23 2018

@author: lidh
"""
import hashlib
import urllib.request
import ssl
import json
import pymysql
from multiprocessing import Pool
def create_ssl():
    ssl._create_default_https_context = ssl._create_unverified_context
def run_multi_process(func,typess):
    p = Pool(len(typess)+1)
    for types in typess:
        p.apply_async(func, args=(types,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
def get_sql_conn(file_name):
    setting_f=open(file_name,'r')
    setting=json.load(setting_f)
    setting_f.close()
    print(setting)
    conn=pymysql.connect(host=setting["datasource_ip"],\
                    user=setting["datasource_username"],\
                    password=setting["datasource_password"],\
                    db=setting["datasource_sql_name"],\
                    port=setting["port"])
    cursor = conn.cursor()
    return conn,cursor,setting
def getHtml(url,code='utf-8'):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode(code)
    return html
def insert_data(cursor,dbName,data_dict):
    try:
        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')
        dbField = data_dict.keys()
        dataTuple = tuple(data_dict.values())
        dbField = str(tuple(dbField)).replace("'",'')
        sql = """ insert into %s %s values %s """ % (dbName,dbField,data_values)
        params = dataTuple
        cursor.execute(sql, params)
        print("=====  Insert Success  =====")
        return 1
    except Exception as e:
        print("********  Insert Failed    ********")
        print (e)
        return 0
def update_data(cursor,dbName,data_dict,key_field):
    try:
        sql = 'update '+dbName+' set '
        for field in data_dict:
            sql=sql+field+'=%s,'
        sql=sql+') where '+key_field+'="'+data_dict[key_field]+'"'
        sql=sql.replace(',)','')
        cursor.execute(sql, tuple(data_dict.values()))
        print("=====  Update Success  =====")
        return 1
    except Exception as e:
        print("********  Update Failed    ********")
        print (e)
        return 0
def get_index_dict(cursor):
    index_dict=dict()
    index=0
    for desc in cursor.description:
        index_dict[desc[0]]=index
        index=index+1
    return index_dict
def md5(str0):
    m = hashlib.md5()
    m.update(str0.encode(encoding='utf-8'))
    return m.hexdigest()
def get_dict_data_sql(cursor,sql):
    cursor.execute(sql)
    data=cursor.fetchall()
    index_dict=get_index_dict(cursor)
    res=[]
    for datai in data:
        resi=dict()
        for indexi in index_dict:
            resi[indexi]=datai[index_dict[indexi]]
        res.append(resi)
    return res