#Author: laolang
#Version: 1.0.0
#Time:17-9-18下午6:18
#用途
'''
xgdl_improt 代替品

'''
# -*- coding: UTF-8 -*-
import connexion
from datetime import date
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from flask import json, jsonify
from flask import Response
import datetime
import calendar
import math
import xlwt
import pymysql
import os
import csv


# ##############################################
#                                              #
#                  自动导入页面                #
#                                              #
# ##############################################



# 1.导入的文件类型
def import_file_type():
    resultdict = {}
    resultdict['import_file_type'] = ['基站清单', '抄表记录', '供电局缴费表号', '基站电表信息', '基站机房的用电相关资料', '客户用电信息']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
# 2. 导入前端文件到本地
def FileImport(arg='', description=''):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    if request.method == 'POST':
        abpath = os.path.abspath('./upload/') + '/'

        f = request.files["file"]
        random_string = str(random.randint(100000000, 10000000000))

        file_name_path = ''
        if arg == '基站清单':
            file_name_path = abpath + 'station_list/' + random_string + '_station_list.xls'
            f.save(abpath + 'station_list/' + random_string + '_station_list.xls')
        elif arg == '抄表记录':
            file_name_path = abpath + 'meter_reading/' + random_string + '_meter_reading.xls'
            f.save(abpath + 'meter_reading/' + random_string + '_meter_reading.xls')
        elif arg == '供电局缴费表号':
            file_name_path = abpath + 'pay_records/' + random_string + '_pay_records.xls'
            f.save(abpath + 'pay_records/' + random_string + '_pay_records.xls')
        elif arg == '基站电表信息':
            file_name_path = abpath + 'electric_info/' + random_string + '_electric_info.xls'
            f.save(abpath + 'electric_info/' + random_string + '_electric_info.xls')
        elif arg == '基站机房的用电相关资料':
            file_name_path = abpath + 'computer_relate/' + random_string + '_computer_relate.xls'
            f.save(abpath + 'computer_relate/' + random_string + '_computer_relate.xls')
        elif arg == '客户用电信息':
            file_name_path = abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls'
            f.save(abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls')
        else:
            print('-arg-err!--')

        # -------------------录入记录表格----------------
        # 名称、大小、时间、描述
        # 1. f、
        for upload in request.files.getlist("file"):
            filename = upload.filename
        # 2. 大小
        filesize = getDocSize(file_name_path)
        # 3.时间
        currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mysql = MySQL(2)
        mysql.mysql_connect()
        sql = " insert into xgdl_uploadfile_information (filename,filesize,description,uploadtime) value ('{}','{}','{}','{}') ".format(
            str(filename), filesize, description, currenttime)
        mysql.executesql(sql)

        mysql.commitdata()
        mysql.mysql_close()
        # -------------------录入记录表格----------------
        reps = jsonify(1)
    else:
        reps = jsonify(-1)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 3.展示导入结果
def showimport(PageIndex=1):
    resultdict = {}
    show = []
    # 1.标题：
    title_name = ['id', '文件名', '文件大小', '文件描述', '时间']
    resultdict["title_name"] = title_name
    # 2.获取录入结果
    mysql = MySQL(2)
    mysql.mysql_connect()
    import_record = "select id,filename,filesize,description,uploadtime from xgdl_uploadfile_information where 1=1 "
    result = mysql.query(import_record)
    mysql.mysql_close()
    resultList = []
    for i in range(len(result)):
        resultList.append(list(result[i]))
    resultList.reverse()

    # ---------分页---------
    rowCount = len(resultList)
    pageCount = 0
    if rowCount % 10 == 0:
        pageCount = rowCount / 10
    else:
        # 向下取整
        pageCount = math.floor(rowCount / 10) + 1

    page_resultList = []
    if len(resultList) < 10:
        endindex = len(resultList)
    else:
        if len(resultList) >= PageIndex * 10:
            endindex = PageIndex * 10
        else:
            endindex = len(resultList)
    if resultList != []:
        for i in range((PageIndex * 10 - 10), endindex):
            page_resultList.append(resultList[i])
        resultdict["page_resultList"] = page_resultList
        resultdict["rowCount"] = rowCount
        resultdict["pageCount"] = pageCount
        # ------------------
    else:
        resultdict["page_resultList"] = []
        resultdict["rowCount"] = 0
        resultdict["pageCount"] = 0

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def show_delete(file_id=0):
    mysql = MySQL(2)
    mysql.mysql_connect()
    import_record = "DELETE FROM xgdl_uploadfile_information WHERE id= {}".format(file_id)
    try:
        mysql.executesql(import_record)
        mysql.commitdata()
        mysql.mysql_close()
        reps = jsonify(1)
    except:
        reps = jsonify(-1)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps

# 5.分片测试
def file_split():
    if request.method == 'POST':
        f = request.files["file"]
        for upload in request.files.getlist("file"):
            filename = upload.filename.rsplit("/")[0]
            f.save("C:/Users/flyminer/Desktop/split_test/" + filename)

    reps = jsonify("ok!")
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps