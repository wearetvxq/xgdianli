# -*- coding: UTF-8 -*-
import connexion
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from swagger_server.utitl.common import com
from flask import json, jsonify
from flask import Response,request
from swagger_server.utitl.excleutil import ExcleUtil1
import os, sys
import time
import math
import socket
import random
import tarfile
import zipfile
import datetime
import os
from multiprocessing import Process, Queue, Array, RLock
import multiprocessing

# ##############################################
#                                              #
#                  添加设备                     #
#                                              #
# ##############################################


############
#单独添加设备#
############
#城市选择
def add_one_city():
    resultdict={}
    city_list=['大悟', '汉川', '孝南','应城', '安陆', '孝昌', '云梦']
    mysql=MySQL(2)
    mysql.mysql_connect()
    print('-city_list-:',city_list)
    resultdict['shebei_list']=['空调','2G','4G']
    resultdict['city_list']=city_list
    print(resultdict)
    reps=jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    mysql.mysql_close()
    return reps
#基站选择
def add_sta_name(choose_city=''):
    sta_list=[]
    staict={}
    mysql = MySQL(2)
    mysql.mysql_connect()
    if choose_city=='':
        choose_city='all'
    sql1 = "select sta_num,sta_name from test WHERE area='{}'".format(choose_city)

    print('----sql1--:', sql1)
    result = mysql.query(sql1)
    for i in result:
        sta_list.append(i[0]+'_'+i[1])
    sta_list=list(set(sta_list))
    print('---sta_list---:', sta_list)
    staict['sta_list']=sta_list
    reps = jsonify(staict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    mysql.mysql_close()
    return reps
#生产厂家选择
def air_add_produce_make(choose_type=''):
    producelist={}
    mysql=MySQL(2)
    print(choose_type)
    mysql.mysql_connect()
    print('------------------------------------------')
    if choose_type=='空调':
        result=[]
        sql1="SELECT produce FROM xgyd_gh_kt_sb "
        print('----sql1---:',sql1)
        type=mysql.query(sql1)
        for i in type:
            if i[0]=='':
                pass
            result.append(i[0])
        result=list(set(result))
        print(result)
        result.insert(0,'请选择')
        producelist['producelist']=(result)
    if choose_type=='2G':
        result=[]
        result.append('诺基亚')
        result.insert(0, '请选择')
        producelist['producelist'] = (result)
    if choose_type=='4G':
        result=[]
        result.append('中兴')
        result.insert(0, '请选择')
        producelist['producelist'] = (result)

    print(producelist)
    reps=jsonify(producelist)
    reps.headers["Access-Control-Allow-Origin"]='*'
    mysql.mysql_close()
    return reps
def air_type(choose_air='',produce=''):
    typedict={}
    type_air=[]
    mysql=MySQL(2)
    mysql.mysql_connect()
    if choose_air=='空调':
        sql1="select xinghao FROM xgyd_gh_kt_sb where produce='{}'".format(produce)
        print('----sql---:',sql1)
        result=mysql.query(sql1)
        print(result)
        for i in result:
            type_air.append(i[0])
        typedict['type_air_list']=type_air
    if choose_air=='4G':
        sql1="select sb_xinghao FROM xgyd_gh_4g_sb"
        print('----sql---:',sql1)
        result=mysql.query(sql1)
        print(result)
        for i in result:
            type_air.append(i[0])
        typedict['type_air_list']=type_air
    if choose_air=='2G':
        type_air=['MCPA']
        print(type_air)
        typedict['type_air_list'] = type_air
    reps=jsonify(typedict)
    mysql.mysql_close()
    reps.headers["Access-Control-Allow-Origin"]='*'
    return reps


#提交选项--------------添加设备
def add_one_import(choose_sta='',choose_device='',choose_product='',choose_type='',choose_pow='',choose_area=''):
    print(choose_sta,choose_device,choose_product,choose_type)
    result={}
    mysql=MySQL(2)
    mysql.mysql_connect()
    if choose_device=='空调':
        choose_device='kt'
    sql="insert into test (sta_num,produce,max_pow,sb_type,type,sta_name,area) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(choose_sta.split('_')[0],choose_product,choose_pow,choose_device,choose_type,choose_sta.split('_')[1],choose_area)
    print(sql)
    mysql.Insert(sql)
    mysql.mysql_close()
    result['flag']='1'
    reps=jsonify(result)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps





#根据基站编码修改-----空调设备数据--------增
def sta_num_add_import(sta_num):
    mysql=MySQL(2)
    mysql.mysql_connect()
    mysql.mysql_close()



#根据基站编码修改-----空调设备数据--------改





#根据基站编码修改-----空调设备数据--------减


