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
#                  高压异常页面                  #
#                                              #
# ##############################################

def high_err_count(choose_city=''):
    '''
    高压异常数量
    :return:
    '''
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    if choose_city == 'all':
        sql = "select count(id) from xgld_load_abnormal WHERE `type` != '正常' AND sta_num IN (SELECT sta_no FROM xgdl_high_voltage_user GROUP BY sta_no)"
    else:
        sql = "select count(id) from xgld_load_abnormal WHERE sta_num in(select sta_no FROM xgdl_high_voltage_user_sta_no WHERE city='{}') AND `type` != '正常' AND sta_num IN (SELECT sta_no FROM xgdl_high_voltage_user GROUP BY sta_no)".format(choose_city)

    print('--sql-11-', sql)
    result = mysql.query(sql)
    print('--result-11-', result)
    resultdict['count'] = result[0][0]

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def city_voltage_high(choose_city=''):
    '''
    高压基站 对应的城市
    :return:
    '''
    # choose_city = 'all'
    print('---choose_city:-', choose_city)
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    if choose_city == 'all':
        city_list = ['全部']

        sql = "select city from xgdl_high_voltage_user GROUP BY city"
        print('--sql-1-', sql)
        result = mysql.query(sql)

        for i in range(len(result)):
            city_list.append(result[i][0])
    else:
        city_list = [choose_city]
    print('---city_list:-', city_list)
    resultdict['city_list'] = city_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def type_err():
    '''
    高压基站，异常类型
    :return:
    '''
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    type_list = ['全部']

    sql = "select `type` from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_high_voltage_user GROUP BY sta_no) GROUP BY `type`"
    print('--sql-2-', sql)
    result = mysql.query(sql)

    for i in range(len(result)):
        type_list.append(result[i][0])

    print('--type_list--', type_list)
    resultdict['type_list'] = type_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def table_high_err(city='', type_err='', PageIndex=1):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    type_list = []

    err_list = []
    sta_no_list = []
    sta_list = []
    met_reader_list = []

    if city != '' and city != '全部':
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE `type`='{}' AND sta_num in(select sta_no FROM xgdl_high_voltage_user WHERE city='{}')".format(type_err, city)
            print('--sql-3-', sql)
        else:
            sql = "select * from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_high_voltage_user WHERE city='{}')".format(city)
            print('--sql-4-', sql)
    else:
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE `type`='{}' AND sta_num in(select sta_no FROM xgdl_high_voltage_user)".format(type_err)
            print('--sql-3-', sql)
        else:
            sql = "select * from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_high_voltage_user)"
            print('--sql-4-', sql)
    result = mysql.query(sql)
    print('--result-4-', result)
    print('--result-4-', len(result))
    for i in range(len(result)):
        err_list.append(list(result[i]))
        sta_no_list.append(result[i][1])
    for i in range(len(err_list)):
        err_list[i] = err_list[i][1:]
        # del(err_list[i][0])
    print('--err_list-4-', err_list)
    if len(sta_no_list) > 0:
        if len(sta_no_list) == 1:
            sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num = '{}'".format(sta_no_list[0])
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[0])
            # sql_3 = "select city from xgdl_high_voltage_user WHERE sta_no = '{}' GROUP BY city".format(sta_no_list[0])
            print('--sql-5-', sql_1)
            print('--sql-6-', sql_2)
        if len(sta_no_list) > 1:
            # for i in range(len(sta_no_list)):
            #     sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num = '{}'".format(sta_no_list[i])
            #     sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[i])
            #     result_1 = mysql.query(sql_1)
            #     result_2 = mysql.query(sql_2)
            #     print('---------------------------')
            #     print('--result_1--', result_1)
            #     print('--result_1--', len(result_1))
            #     print('--result_2--', result_2)
            #     print('--result_2--', len(result_2))
            #     print('---------------------------')
            print('--len(sta_no_list):---', len(sta_no_list))
            sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num in {}".format(tuple(sta_no_list))
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no in {}".format(tuple(sta_no_list))
            print('--sql-7-', sql_1)
            print('--sql-8-', sql_2)
        result_1 = mysql.query(sql_1)
        result_2 = mysql.query(sql_2)
        print('--result_1--', result_1)
        print('--result_1--', len(result_1))
        print('--result_2--', result_2)
        print('--result_2--', len(result_2))
        for i in range(len(result_1)):
            err_list[i][0] = str(result_1[i][0]) + '_' + str(result_1[i][1])
        for i in range(len(result_2)):
            err_list[i].insert(1, result_2[i][0])

        for i in range(len(err_list)):
            sql_3 = "select city from xgdl_high_voltage_user WHERE sta_no = '{}' GROUP BY city".format(err_list[i][0].split('_')[0])
            result_3 = mysql.query(sql_3)
            err_list[i].insert(2, result_3[0][0])

    print('--err_list--', err_list)

    show_tz = com.paging(err_list, everyPage_count=10, PageIndex=PageIndex)
    page_resultList = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]

    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount
    title = ['基站编号', '责任人', '区域', '负荷均值','跳变次数', '操作']
    resultdict['title'] = title

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps

