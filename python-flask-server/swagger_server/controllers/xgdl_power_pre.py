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
#                  能耗预测                    #
#                                              #
# ##############################################


def pre_city(choose_city=''):
    '''
    预警页面city 列表
    :return:
    '''
    print('---choose_city:-', choose_city)
    # choose_city = 'all'
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    if choose_city == 'all':
        city_list = ['全部']

        sql = "select city FROM xgdl_high_voltage_user WHERE sta_no IN (SELECT sta_num FROM basic_sta_list WHERE id IN (select sta_id from pred_sta_dl GROUP BY sta_id)) GROUP BY city"
        sql_1 = "select city FROM xgdl_low_voltage_user WHERE sta_no IN (SELECT sta_num FROM basic_sta_list WHERE id IN (select sta_id from pred_sta_dl GROUP BY sta_id)) GROUP BY city"
        result = mysql.query(sql)
        result_1 = mysql.query(sql_1)
        for i in range(len(result)):
            city_list.append(result[0][0])
        for i in range(len(result_1)):
            if result_1[i][0] not in city_list:
                city_list.append(result_1[i][0])
    else:
        city_list = [choose_city]
    resultdict['city_list'] = city_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def pre_sta_list(city=''):
    '''
    预测页面sta 列表
    :param city:
    :return:
    '''
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sta_list = []
    no_list = []
    sql_base = "SELECT sta_num FROM Predict_sta_load GROUP BY sta_num"
    result_base = mysql.query(sql_base)
    for i in range(len(result_base)):
        no_list.append(result_base[i][0])
    if city == '' or city == '全部':
        sql = "select sta_num,sta_name FROM basic_sta_list WHERE sta_num IN {}".format(tuple(no_list))
    else:
        sql = "select sta_num,sta_name FROM basic_sta_list WHERE sta_num in {} AND sta_num IN (select sta_no FROM basic_city_list WHERE city ='{}')".format(tuple(no_list), city)

    result = mysql.query(sql)
    for i in range(len(result)):
        sta_list.append(str(result[i][0]) + '_' + str(result[i][1]))

    resultdict['sta_list'] = sta_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def pre_time_list(sta_name=''):
    '''
    预警页面time 列表
    :param sta_name:
    :return:
    '''
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sql = "select min(`date`) as minday,max(`date`) as maxday from Predict_sta_load WHERE sta_num='{}'".format(sta_name.split('_')[0])
    print('--sql:-', sql)
    result = mysql.query(sql)

    minday = str(result[0][0])
    maxday = str(result[0][1])
    if minday != 'None' and maxday != 'None':
        resultdict['minday'] = minday
        resultdict['maxday'] = maxday
    else:
        resultdict['minday'] = []
        resultdict['maxday'] = []

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def pre_chart(sta_name='', StartDate='', EndDate=''):
    '''
    预测页面 图表
    :param sta_name:
    :param StartDate:
    :param EndDate:
    :return:
    '''
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    date_list = []
    power_list = []

    sql = "select `date`,`load` from Predict_sta_load WHERE sta_num='{}' AND `date` BETWEEN '{}' AND '{}' group by `date` order by `date`".format(sta_name.split('_')[0], StartDate,EndDate)
    print('---sql:--', sql)
    result = mysql.query(sql)

    for i in range(len(result)):
        date_list.append(result[i][0])
        power_list.append(result[i][1])

    resultdict['date_list'] = date_list
    resultdict['power_list'] = power_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps