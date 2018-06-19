# -*- coding: UTF-8 -*-
import connexion
from operator import itemgetter
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
#                  机房列表页面                  #
#                                              #
# ##############################################


#机房列表城市检索
def city_device_management(choose_city=''):
    '''
    对应的城市
    :return:
    '''
    # choose_city = 'all'
    print('---choose_city:-', choose_city)
    if choose_city=='' or choose_city=='全部':
        choose_city='all'
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    if choose_city == 'all':
        city_list = ['全部']
        sql = "select fuzai from duibi"
        print('--sql-1-', sql)
        result = mysql.query(sql)

        for i in range(len(result)):
            city_list.append(result[i][0])
        city_list=list(set(city_list))
        # 排序
        for x in range(len(city_list)):
            if city_list[x] == '全部':
                haha = city_list[0]
                city_list[0] = '全部'
                city_list[x] = haha
    else:
        city_list = [choose_city]
    print('---city_list:-', city_list)
    resultdict['city_list'] = city_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
#机房列表基站名称
def sta_device_management(choose_city=''):
    '''
    #选择城市对应的基站名称
    :param type_sta:
    :return:
    '''
    print('---choose_city:-', choose_city)
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    if choose_city=='' or choose_city=='全部':
        choose_city='all'
    if choose_city!='孝昌':
        sta_name_list=['全部']
        sql="select sta_name FROM new_test WHERE area='{}'".format(choose_city)
        print(sql)
        result=mysql.query(sql)
        for i in result:
            if i not in sta_name_list:
                sta_name_list.append(i[0])
        print(len(sta_name_list))
    if choose_city=='孝昌':
        sta_name_list=['全部']
        sql="select sta_name FROM new_test WHERE area='{}'".format(choose_city)
        print(sql)
        result = mysql.query(sql)
        for i in result:
            print(i)
            if i[0] not in sta_name_list:
                sta_name_list.append(i[0])
        print(len(sta_name_list))
    if choose_city=='all':
        sta_name_list = ['全部']
        sql = "select sta_name FROM new_test"
        print(sql)
        result = mysql.query(sql)
        for i in result:
            if i not in sta_name_list:
               sta_name_list.append(i[0])
        print(len(sta_name_list))
    print('---sta_name_list:-', sta_name_list)
    resultdict['sta_name_list'] = sta_name_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
#机房列表表单
def room_table_list(choose_sta='',choose_city='',PageIndex=1,sort='0',sort_air='1'):
    resultidct={}
    table_list=[]
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultidct['title']=['地区','基站名称','基站额定功率','超出频率','额定用电','是否存在空调','操作']
    if choose_city!='' and choose_city!='全部':
        #有地区有基站名
        if choose_sta!='' and choose_sta!='全部':
            sql="select * from new_test where sta_name='{}'".format(choose_sta)
            table_list=[[mysql.query(sql)[0][0],mysql.query(sql)[0][1],mysql.query(sql)[0][3],float(mysql.query(sql)[0][2]),str(mysql.query(sql)[0][6])+'度/天',mysql.query(sql)[0][4]]]


        else:
            if sort_air=='1':
                #有地区没有基站名
                sql5="select * from new_test where area='{}'".format(choose_city)
                print('sql5---:', sql5)
                result = mysql.query(sql5)
                print(result)
                for i in range(len(result)):
                    print(result[i])
                    table_list_more = [result[i][0], result[i][1], float(result[i][3]),float(result[i][2]),str(result[i][6])+'度/天', result[i][4]]
                    table_list.append(table_list_more)
                print(table_list)
                if sort == '1':
                    table_list = sorted(table_list, key=itemgetter(3), reverse=True)
                if sort == '0':
                    table_list = sorted(table_list, key=itemgetter(3))
            if sort_air=='0':
                # 有地区没有基站名
                sql5 = "select * from new_test where area='{}' and is_kt='存在'".format(choose_city)
                print('sql5---:', sql5)
                result = mysql.query(sql5)
                print(result)
                for i in range(len(result)):
                    table_list_more = [result[i][0], result[i][1], float(result[i][3]), float(result[i][2]),str(result[i][6]) + '度/天', result[i][4]]
                    table_list.append(table_list_more)
                if sort == '1':
                    table_list = sorted(table_list, key=itemgetter(3), reverse=True)
                if sort == '0':
                    table_list = sorted(table_list, key=itemgetter(3))



    else:
        if sort_air=='1':
            choose_city='孝昌'
            sql5 = "select * from new_test"
            print('sql5---:', sql5)
            result = mysql.query(sql5)
            print(result)
            for i in range(len(result)):
                table_list_more = [result[i][0], result[i][1], float(result[i][3]),float(result[i][2]) ,str(result[i][6])+'度/天',result[i][4]]
                table_list.append(table_list_more)
            print(table_list)
            if sort == '0':
                table_list = sorted(table_list, key=itemgetter(3), reverse=True)
            if sort == '1':
                table_list = sorted(table_list, key=itemgetter(3))
        if sort_air=='0':
            choose_city = '孝昌'
            sql5 = "select * from new_test where is_kt='存在'"
            print('sql5---:', sql5)
            result = mysql.query(sql5)
            print(result)
            for i in range(len(result)):
                table_list_more = [result[i][0], result[i][1], float(result[i][3]), float(result[i][2]),str(result[i][6]) + '度/天', result[i][4]]
                table_list.append(table_list_more)
            print('--------------len------',len(table_list))
            if sort == '0':
                table_list = sorted(table_list, key=itemgetter(3), reverse=True)
            if sort == '1':
                table_list = sorted(table_list, key=itemgetter(3))


    print(len(table_list))
    show_tz = com.paging(table_list, everyPage_count=10, PageIndex=PageIndex)

    table_list = show_tz[0]
    print(len(table_list))
    rowCount = show_tz[1]
    pageCount = show_tz[2]
    resultidct['table_list'] = table_list
    resultidct['rowCount'] = rowCount
    resultidct['pageCount'] = pageCount
    mysql.mysql_close()
    reps=jsonify(resultidct)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps
def room_desc_show(choose_sta=''):
    print('---choose_sta:--', choose_sta)
    '''
    当前基站数据展示
    :param sta_name:
    :return:
    '''
    data_list=[]
    load_list=[]
    resultdict={}
    mysql=MySQL(2)
    mysql.mysql_connect()

    choose_sta_new=choose_sta.split('_')[-1]
    sql0 = "SELECT id from Xgdl_Basic_Load where sta_no='{}'".format(choose_sta_new)
    resulttest=mysql.query(sql0)
    print(sql0)
    print(resulttest)
    if resulttest==():
        new_sta=choose_sta_new.replace('-','')
        sql="select `date`,`load` from Xgdl_Basic_Load where sta_no='{}'".format(new_sta)
    else:
        sql = "select `date`,`load` from Xgdl_Basic_Load where sta_no='{}'".format(choose_sta_new)
    sql1="select sta_name from Xgdl_Basic_Stalist where sta_no='{}'".format(choose_sta_new)
    print(sql)
    result=mysql.query(sql)
    result1=mysql.query(sql1)
    for i in range(len(result)):
        data_list.append(result[i][0])
        load_list.append(result[i][1])
    print(data_list)
    print(load_list)

    resultdict['name']=choose_sta
    resultdict['date_list'] = data_list
    resultdict['load_list'] = load_list
    print(len(data_list))
    print(len(load_list))
    reps = jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin'] = '*'
    return reps

def air_duibi_table(choose_sta1='',choose_sta2=''):
    mysql=MySQL(2)
    mysql.mysql_connect()
    air_list1=[]
    air_list2=[]
    resultdict={}
    new_choose_sta1 = choose_sta1.split('_')[1]
    new_choose_sta2 = choose_sta2.split('_')[1]
    resultdict['title']=['基站名称','空调生产厂家','空调型号','实际功率','最大功率','制冷功率']
    sql1="select kt_xinghao from xgyd_gh_kt where sta_num='{}'".format(new_choose_sta1)
    sql2="select kt_xinghao from xgyd_gh_kt where sta_num='{}'".format(new_choose_sta2)
    result1=mysql.query(sql1)
    result2=mysql.query(sql2)
    print(result1)
    print(result2)
    resultdict['air_list1'] = []
    for x in range(len(result1)):
        if result1[x][0] not in air_list1:
            sql_air1="select `produce`,`max_pow` from xgyd_gh_kt_sb where xinghao='{}'".format(result1[x][0])
            air_msg1=mysql.query(sql_air1)
            for x1 in range(len(air_msg1)):
                resultdict['air_list1'].append([choose_sta1, air_msg1[x1][0], result1[x][0], air_msg1[x1][1], '暂无', '暂无'])
    for y in range(len(result2)):
        if result2[y][0] not in air_list2:
            sql_air2 = "select `produce`,`max_pow` from xgyd_gh_kt_sb where xinghao='{}'".format(result2[y][0])
            air_msg2 = mysql.query(sql_air2)
            for y1 in range(len(air_msg2)):
                resultdict['air_list1'].append([choose_sta2, air_msg2[y1][0], result2[y][0], air_msg2[y1][1], '暂无', '暂无'])
    if air_list1==[]:
        air_list1=[choose_sta1,'暂无','暂无','暂无','暂无','暂无']
    if air_list2==[]:
        air_list2=[choose_sta2,'暂无','暂无','暂无','暂无','暂无']
    print(air_list2)

    reps=jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps


#查看详情
#2g
def one_room_desc(choose_sta='',sta_pow=''):
    roomdict={}
    two_g_list=[]
    four_g_list=[]
    kt_list=[]
    mysql=MySQL(2)
    mysql.mysql_connect()
    choose_sta=choose_sta.split('_')[1]
    try:
        sql1="select `produce`,`type`,`max_pow` from test WHERE sta_num='{}' and sb_type='2G'".format(choose_sta)
        print('---sql2g----:',sql1)
        result2g=mysql.query(sql1)
        print(result2g[0])
        for i in range(len(result2g)):
            two_g_list.append(result2g[i])
        two_g_list = sorted(two_g_list, key=itemgetter(2), reverse=True)
        print(two_g_list)
    except:
        two_g_list=[]
# 4g
    try:
        sql1 = "select `produce`,`type`,`max_pow` from test WHERE sta_num='{}' and sb_type='4G'".format(choose_sta)
        print('---sql4g----:', sql1)
        result4g = mysql.query(sql1)
        print(result4g[0])
        for i in range(len(result4g)):
            four_g_list.append(result4g[i])
            four_g_list = sorted(four_g_list, key=itemgetter(2), reverse=True)
        print(four_g_list)
    except:
        four_g_list=[]
# kt
    try:
        sql1 = "select `produce`,`type`,`max_pow` from test WHERE sta_num='{}' and sb_type='kt'".format(choose_sta)
        print('---sqlkt----:', sql1)
        resultkt = mysql.query(sql1)
        for i in range(len(resultkt)):
            kt_list.append(resultkt[i])
            kt_list = sorted(kt_list, key=itemgetter(2), reverse=True)
        print(kt_list)
    except:
        kt_list=[]
#基站信息

    sql4="select `area`,`sta_name` from test where sta_num='{}'".format(choose_sta)
    print(sql4)
    result_baisc=mysql.query(sql4)
    print(result_baisc)
    if two_g_list==[]:
        two_g_list=[['暂无','暂无','暂无']]
    if kt_list==[]:
        kt_list=[['暂无','暂无','暂无']]
    if four_g_list==[]:
        four_g_list=[['暂无','暂无','暂无']]
    print(result_baisc[0][0],result_baisc[0][1],choose_sta)
    roomdict['Biasc']=[result_baisc[0][0]+'_'+result_baisc[0][1]+'_'+choose_sta]
    roomdict['two_g_list']=two_g_list
    roomdict['four_g_list']=four_g_list
    roomdict['kt_list'] = kt_list
    print(two_g_list)
    print(four_g_list)
    print(kt_list)
    roomdict['sta_pow']=sta_pow
    roomdict['title']=['生产厂家','设备型号','设备功率','操作']

    reps=jsonify(roomdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps


#查看详情修改接口
def update_room_desc(choose_sta='',old_produce='',old_type='',old_pow='',new_produce='',new_type='',new_pow='',sb=''):
    status_code={}
    mysql=MySQL(2)
    mysql.mysql_connect()
    print(sb)
    choose_sta=choose_sta.split('_')[-1]
    try:
        if  sb=='2G':
            print(old_produce,old_type,old_pow)
            print(new_produce,new_type,new_pow)
            sql_2g="select * from test where sta_num='{}' and sb_type='2G'".format(choose_sta)
            update_id=mysql.query(sql_2g)[0][0]
            #updata
            sql_update_2g="UPDATE test SET produce='{}',max_pow='{}',type='{}' WHERE ID='{}'".format(new_produce,new_pow,new_type,update_id)
            print(sql_update_2g)
            mysql.Update(sql_update_2g)
            status_code['status_code']=1
        if sb=='4G':
            print(old_produce, old_type, old_pow)
            sql_4g = "select * from test where sta_num='{}' and sb_type='4G' and type='{}'".format(choose_sta,old_type)
            update_id = mysql.query(sql_4g)[0][0]
            #update
            sql_update_4g="UPDATE test SET produce='{}',max_pow='{}',type='{}' WHERE ID='{}'".format(new_produce,new_pow,new_type,update_id)
            print(sql_update_4g)
            mysql.Update(sql_update_4g)
            status_code['status_code'] = 1

        if sb=='空调':
            print('----------')
            print(old_produce, old_type, old_pow)
            sql_kt="select * from test WHERE sta_num='{}' and type='{}'".format(choose_sta,old_type)
            print('sql_kt',sql_kt)
            update_id =mysql.query(sql_kt)[0][0]
            #Update type
            sql_update_kt="UPDATE test set produce='{}',max_pow='{}',type='{}' where ID ='{}'".format(new_produce,new_pow,new_type,update_id)
            print(sql_update_kt)
            mysql.Update(sql_update_kt)
            status_code['status_code']=1
    except:
        status_code['status_code'] = 0
    reps=jsonify(status_code)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps














