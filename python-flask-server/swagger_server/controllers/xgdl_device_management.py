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
#                  设备管理页面                  #
#                                              #
# ##############################################

#设备管理城市检索
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
        sql = "select city from Xgdl_Basic_Stalist"
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
#设备管理基站名称
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

    if choose_city != '' and choose_city!='全部':
        sta_name_list=[('全部',)]
        sql="select 节点_基站名称 FROM Air_node_total_table WHERE 县='{}'".format(choose_city)
        print(sql)
        result=mysql.query(sql)
        for i in result:
            if i not in sta_name_list:
                sta_name_list.append(i)
        print(len(sta_name_list))

    # 默认条件下，查找安陆的所有基站
    else:
        sta_name_list = [('全部',)]
        sql = "select 节点_基站名称 FROM Air_node_total_table"
        print(sql)
        result = mysql.query(sql)
        for i in result:
            if i not in sta_name_list:
               sta_name_list.append(i)
        print(len(sta_name_list))
    print('---sta_name_list:-', sta_name_list)
    resultdict['sta_name_list'] = sta_name_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


#设备管理的表接口（空调）
def table_device_management_chm(choose_city='',sta_name='',PageIndex=1):
    basic_list = []
    resultdict={}
    if choose_city=='':
        choose_city='全部'
    if sta_name=='':
        sta_name='全部'
    resultdict['title']=['地区','基站名称','数量','功率','操作']
    print('---sta_name-:',sta_name)
    mysql=MySQL(2)
    mysql.mysql_connect()
    #所属基站和数量.功率

    if choose_city!='全部':
        sql="SELECT * FROM test WHERE sb_type='kt' and area='{}'".format(choose_city)
        print('sql-----',sql)
        result=mysql.query(sql)
        for i in range(len(result)):
                sql_total="select max_pow from test where sta_num='{}' and sb_type='kt'".format(result[i][1])
                msg_kt_list=mysql.query(sql_total)
                total=len(msg_kt_list)
                power=0
                for x in range(len(msg_kt_list)):
                    power=power+float(msg_kt_list[x][0])
                list=[result[i][-1],result[i][-2]+'_'+result[i][1],total,power]
                if list not in basic_list:
                   basic_list.append(list)

    else:
        sql = "SELECT * FROM test WHERE sb_type='kt'"
        print('sql-----', sql)
        result = mysql.query(sql)
        for i in range(len(result)):
                sql_total = "select max_pow from test where sta_num='{}' and sb_type='kt'".format(result[i][1])
                msg_kt_list = mysql.query(sql_total)
                total = len(msg_kt_list)
                power = 0
                for x in range(len(msg_kt_list)):
                    power = power + float(msg_kt_list[x][0])
                list = [result[i][-1], result[i][-2] + '_' + result[i][1], total, power]
                if list not in basic_list:
                    basic_list.append(list)

    basic_list=sorted(basic_list, key=itemgetter(3), reverse=True)
    show_tz = com.paging(basic_list, everyPage_count=10, PageIndex=PageIndex)
    page_resultList=show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]

    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
#机房管理详情页面表单-------接口（空调）
def table_device_desc(sta_name='',type=''):
    mysql=MySQL(2)
    mysql.mysql_connect()
    if type=='空调':
        result = []
        old_sta_name=sta_name
        sta_name = sta_name.split('_')[-1]
        if sta_name.find('-') != -1:
            new_sta_name = sta_name.replace('-', '')
        if '-' not in sta_name:
            new_sta_name = sta_name.replace('XG', 'XG-')
        print(new_sta_name)
        sql = "select kt_xinghao from xgyd_gh_kt where sta_num='{}'".format(sta_name)
        print(sql)
        result_kt = mysql.query(sql)
        print(result_kt)
        if result_kt == ():
            sql_new = "select kt_xinghao from xgyd_gh_kt where sta_num='{}'".format(new_sta_name)
            result_kt = mysql.query(sql_new)
            print(result_kt)
        # type_list查询的型号列表和查询结果列表
        type_list = []
        msg_list = []
        if result_kt != ():
            for i in range(len(result_kt)):
                type_list.append(result_kt[i][0])
            for x in range(len(type_list)):
                sql_max_pow = "select `max_pow`,`produce` from xgyd_gh_kt_sb where xinghao='{}'".format(type_list[x])
                print(sql_max_pow)
                msg_list = mysql.query(sql_max_pow)
                print(msg_list)
                result.append([old_sta_name, type_list[x], msg_list[0][0], msg_list[0][1], '空调'])
        print(result)
        resultdict = {}
        resultdict['result'] = result
        resultdict['title'] = ['基站名', '型号', '实际功率', '生产厂家', '设备类型', '操作']
        reps = jsonify(resultdict)
        reps.headers['Access-Control-Allow-Origin'] = '*'
        return reps





#（机房设备详情接口）（机房）
def table_device_desc_sb(sta_name='',PageIndex=1):
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_name=sta_name.split('_')[1]
    sql = "select * from test where sta_num='{}'".format(sta_name)
    resultdict = {}
    resultlist = []
    resultdict['title'] = ['基站名', '设备型号', '实际功率', '生产厂家', '设备类型','操作']
    result = mysql.query(sql)
    for i in range(len(result)):
            sta_name = result[i][6] + '_' + result[i][1]
            device_type = result[i][5]
            max_pow = result[i][3]
            produce = result[i][2]
            type = result[i][4]
            resultlist.append([sta_name, device_type,max_pow, produce, type])
    show_tz = com.paging(resultlist, everyPage_count=10, PageIndex=PageIndex)
    table_list = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]
    resultdict['resultlist'] = table_list
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount
    reps = jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin'] = '*'
    return reps
#机房管理(基站)页面表单-------接口
def room_device_table_list(choose_city='全部',PageIndex=1):
    """
    机房载波设备的管理
    :param choose_city:
    :return:
    """
    resultdict={}
    resultdict['title']=['地区','基站名称','基站载波功率','2G设备数量','4G设备数量','操作']
    table_list=[]
    mysql=MySQL(2)
    mysql.mysql_connect()
    if choose_city=='全部':

        sql1 = "select * from jifang_guanli"
        result = mysql.query(sql1)
        for i in range(len(result)):
            table_list.append([result[i][0],result[i][1],result[i][2],result[i][3],result[i][4]])

    if choose_city!='全部':
        sql1 = "select * from jifang_guanli where area='{}' ".format(choose_city)
        print('sql2g-----', sql1)
        result = mysql.query(sql1)
        for i in range(len(result)):
            table_list.append([result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]])
    table_list=sorted(table_list,key=itemgetter(2),reverse=True)
    show_tz = com.paging(table_list, everyPage_count=10, PageIndex=PageIndex)
    table_list = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]
    resultdict['table_list'] = table_list
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps





#设备删除接口
def device_remove(choose_sta,device_type,device_pow,sb_type,produce):
    mysql=MySQL(2)
    if sb_type=='空调':
        sb_type='kt'
    try:
        mysql.mysql_connect()
        sql = "select ID from test where sta_num='{}' and type='{}' and max_pow='{}' and sb_type='{}' and produce='{}'".format(choose_sta.split('_')[-1], device_type, device_pow, sb_type,produce)
        print(sql)
        ID = mysql.query(sql)
        print('ID----------',ID[0][0])
        sql_delete = "delete from test where ID={}".format(ID[0][0])
        print(sql_delete)
        reps = jsonify({'status_code': '1'})
    except:
        reps = jsonify({'status_code': '0'})
    reps.headers['Access-Control-Allow-Origin'] = '*'
    mysql.mysql_close()
    return reps







#sb选择的下拉接口（更新之后没有使用的接口）
def choose_sb():
    resultdict={}
    resultdict['type_list']=['2G','4G','空调']
    reps=jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps
#批量导入接口
def write_sb(city_list,area_list,sta_list,type_list,pow_list,produce_list,sb_type=''):
    mysql=MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    city_list=city_list.split(',')
    area_list=area_list.split(',')
    sta_list=sta_list.split(',')
    type_list=type_list.split(',')
    pow_list=pow_list.split(',')
    produce_list=produce_list.split(',')
    print(city_list, area_list, sta_list, type_list, pow_list, produce_list)

    try:
        if city_list!=[]:
            if sb_type=='2G':
                print ('-----2G--------')
                for i in range(len(city_list)):
                    sql_id="select id from piliang_import"
                    print (sql_id)
                    max_id=mysql.query(sql_id)
                    print (max_id[-1][0])
                    new_id=int(max_id[-1][0])+1
                    sql="insert into  piliang_import (id,city,sta_num,type,pow,produce,sb_type,data_time) VALUES ({},'{}','{}','{}','{}','{}','{}','{}')".format(new_id,city_list[i],sta_list[i],type_list[i],pow_list[i],produce_list[i],'2G',time.strftime('%Y-%m-%d',time.localtime(time.time())))
                    print(sql)
                    mysql.Insert(sql)
                    resultdict['status_code'] = 1
            if sb_type=='4G':
                print ('-----4G--------')
                for i in range(len(city_list)):
                    sql_id = "select id from piliang_import"
                    print (sql_id)
                    max_id = mysql.query(sql_id)
                    print (max_id[-1][0])
                    new_id = int(max_id[-1][0]) + 1
                    sql="insert into  piliang_import (id,city,sta_num,type,pow,produce,sb_type,data_time) VALUES ({},'{}','{}','{}','{}','{}','{}','{}')".format(new_id,city_list[i],sta_list[i],type_list[i],pow_list[i],produce_list[i],'4G',time.strftime('%Y-%m-%d',time.localtime(time.time())))
                    print(sql)
                    mysql.Insert(sql)
                    resultdict['status_code'] = 1
            if sb_type=='空调':
                print ('-----空调--------')
                for i in range(len(city_list)):
                    sql_id = "select id from piliang_import"
                    print (sql_id)
                    max_id = mysql.query(sql_id)
                    print (max_id[-1][0])
                    new_id = int(max_id[-1][0]) + 1
                    sql="insert into  piliang_import (id,city,sta_num,type,pow,produce,sb_type,data_time) VALUES ({},'{}','{}','{}','{}','{}','{}','{}')".format(new_id,city_list[i],sta_list[i],type_list[i],pow_list[i],produce_list[i],'空调',time.strftime('%Y-%m-%d',time.localtime(time.time())))

                    print(sql)
                    mysql.Insert(sql)
                    resultdict['status_code'] = 1


    except:
        resultdict['status_code'] = '0'
    reps=jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps
def write_show():
    result_list=[]
    resultdict={}
    mysql=MySQL(2)
    mysql.mysql_connect()
    sql="select * from piliang_import"
    result=mysql.query(sql)
    for i in range(len(result)):

        list=['yes',str(result[i][0]),result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7]]
        result_list.append(list)
    resultdict['result']=result_list
    print (result_list)
    reps=jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps
def del_write(id=''):
    print (id)
    resultdict={}
    mysql=MySQL(2)
    mysql.mysql_connect()
    try:
        sql="DELETE  from piliang_import where id ={}".format(int(id))
        print (sql)
        mysql.Remove(sql)
        mysql.mysql_close()
        resultdict['status_code']='1'
    except:
        resultdict['status_code'] = '0'
    reps=jsonify(resultdict)
    reps.headers['Access-Control-Allow-Origin']='*'
    return reps















