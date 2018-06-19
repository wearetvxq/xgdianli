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
#                  异常展示                     #
#                                              #
# ##############################################

# 异常基站详情
def err_sta_details(PageIndex=1):
    err_type = '跳变异常'
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_details = []
    title = ['基站编号', '基站编号', '异常类型', '负荷均值', '低值负荷覆盖率', '跳变次数', '热季负荷', '其他季负荷']
    resultdict['title'] = title

    sql = "select * FROM xgld_load_abnormal where `type`='{}'".format(err_type)
    result = mysql.query(sql)

    for i in range(len(result)):
        sta_details.append(result[i])

    show_tz = com.paging(sta_details, everyPage_count=10, PageIndex=PageIndex)
    page_resultList = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]
    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 异常图表展示
def err_chart_show(sta_no=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    date_list = []
    load_list = []
    sql = "select `date`,`load` FROM Xgdl_Basic_Load where sta_no='{}' order by `date`".format(sta_no)
    result = mysql.query(sql)

    for i in range(len(result)):
        date_list.append(result[i][0])
        load_list.append(result[i][1])

    resultdict['date_list'] = date_list
    resultdict['load_list'] = load_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps