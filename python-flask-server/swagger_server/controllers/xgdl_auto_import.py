# -*- coding: UTF-8 -*-
import connexion
from datetime import date
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from swagger_server.utitl.common import com
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


# 1.数据展示：
def show_data(PageIndex=1):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    result_list = []

    sql = "select * from xgdl_sta_read order by id desc"
    result = mysql.query(sql)
    for i in range(len(result)):
        result_list.append(list(result[i]))

    # ----------分页-------------
    resultList = result_list
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
    result_list = page_resultList

    resultdict["rowCount"] = rowCount
    resultdict["pageCount"] = pageCount
    resultdict['result_list'] = result_list
    resultdict['title'] = ['id', '基站编号', '基站名称', '电表户号', '起码', '止码', '耗电量', '单价', '电费金额', '换表止码', '上次抄表时间', '抄表时间',
                           '是否转码', '是否含有农网维护费', '备注']



    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def data_export():
    # mysql = MySQL(2)
    # mysql.mysql_connect()
    resultdict = {}
    path = os.path.abspath('./../../download/')
    delete_result = com.delete_all_file(path)
    flag = 0
    abpath = os.path.abspath('./../../download/456.xls')
    out_path = abpath
    # sql = 'select * from xgdl_sta_read'
    # count = mysql.executesql(sql)
    # print(count)
    #
    # # cursor.scroll(0, mode='absolute')
    # mysql.excle_scroll()
    # # results = cursor.fetchall()
    # results = mysql.excle_fetchall()
    # # fields = cursor.description
    # fields = mysql.excle_description()
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
    # for field in range(0, len(fields)):
    #     sheet.write(0, field, fields[field][0])
    #
    # row = 1
    # col = 0
    # for row in range(1, len(results) + 1):
    #     for col in range(0, len(fields)):
    #         sheet.write(row, col, u'%s' % results[row - 1][col])
    #
    # workbook.save(out_path)
    # ------------------------------------

    try:
        # host = '192.168.1.112'
        # user = 'root'
        # pwd = '123456'
        # db = 'xgdl'

        sql = 'select * from xgdl_sta_read'
        # conn = pymysql.connect(host, user, pwd, db, charset='utf8')
        mysql = MySQL(2)
        conn = mysql.mysql_connect()
        cursor = conn.cursor()
        count = cursor.execute(sql)

        cursor.scroll(0, mode='absolute')
        results = cursor.fetchall()
        fields = cursor.description
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)

        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])

        workbook.save(out_path)
        flag = 1
    except:
        flag = 0
        print('--导出失败!-')
    resultdict['flag'] = flag
    # ------------------------------------

    # conn.close()
    mysql.mysql_close()
    reps = jsonify(out_path)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def xls_export():
    pass


# 0.删除指定目录下的所有文件
def delete_file():
    path = os.path.abspath('./../../download/')
    for f in os.listdir(path):
        destination = "/".join([path, f])
        os.remove(destination)
    reps = jsonify("删除完成!")
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 删除需要导入的数据：
def delete_data(read_id=''):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    flag = 0
    try:
        import_record = "DELETE FROM xgdl_sta_read WHERE id= {}".format(read_id)
        print(import_record)
        mysql.executesql(import_record)
        mysql.commitdata()
        flag = 1
    except:
        flag = 0
    resultdict['flag'] = flag
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def data_export_1():
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    with open('C:/Users/flyminer/Desktop/excle_export/123123.xls', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(result)):
            tempdict = []
            for j in range(len(columnresult)):
                tempdict.append(str(result[i][int(columnresult[j][0]) - 1]).replace(",", ""))
            spamwriter.writerow(tempdict)
    return './static/images/Warn.csv'

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps