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
import numpy


# ##############################################
#                                              #
#                  同站对比页面                #
#                                              #
# ##############################################

# 1.获取自留和三方共有的基站。
def get_com_sta(choose_city=''):
    resultdict = {}
    station_list = []
    mysql = MySQL(2)
    mysql.mysql_connect()
    if choose_city == 'all':
        sql = "select sta_name,sta_no FROM Xgdl_Basic_Stalist WHERE sta_no in( select sta_num from basic_sta_list where id in(select sta_id from orig_sta_yd GROUP BY sta_id) GROUP BY sta_id)"
    else:
        sql = "select sta_name,sta_no FROM Xgdl_Basic_Stalist WHERE `city` ='{}' AND sta_no in( select sta_num from basic_sta_list where id in(select sta_id from orig_sta_yd GROUP BY sta_id) GROUP BY sta_id)".format(choose_city)

    result = mysql.query(sql)
    if len(result) > 0:
        for i in range(len(result)):
            station_list.append(str(result[i][0]) + '_' + str(result[i][1]))
    else:
        print('没有找到自留和三方共同的基站!')

    print('-----station_list:-', station_list)
    print('-----station_list:-', len(station_list))
    resultdict['title'] = '基站列表'
    resultdict['station_list'] = station_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 2.根据基站获取开始时间和结束时间。
def get_sta_end(station_name=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    station_name = str(station_name).split('_')[1]
    sql_1 = "select min(`date`) as minday,max(`date`) as maxday from Xgdl_Basic_Load WHERE sta_no='{}'".format(station_name)
    sql_2 = "select min(`date`) as minday,max(`date`) as maxday from orig_sta_yd WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(station_name)
    result_1 = mysql.query(sql_1)
    result_2 = mysql.query(sql_2)
    minday = min(str(result_1[0][0]), str(result_2[0][0]))
    maxday = max(str(result_1[0][1]), str(result_2[0][1]))
    if minday != 'None' and maxday != 'None':
        resultdict['minday'] = str(minday)
        resultdict['maxday'] = str(maxday)
    else:
        resultdict['minday'] = []
        resultdict['maxday'] = []

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 3.划出三方和自留的用电折线图
def get_elc_line_chart(sta='', StartDate='', EndDate=''):
    resultdict = {}
    result_list_dl = []
    result_list_yd = []
    y_dl = []
    y_yd = []
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta = str(sta).split('_')[1]
    date_list = com.get_month_list(StartDate,EndDate)
    resultdict['date_list'] = date_list

    # 查询月数据平均值放到类表中
    for i in range(len(date_list)):
        day_pre_list_dl = []
        day_pre_list_yd = []
        day_pre_list_dl.append(date_list[i])
        day_pre_list_yd.append(date_list[i])

        sql_dl = "SELECT `load` FROM Xgdl_Basic_Load where sta_no='{}' and `date` like '{}'".format(sta, str(day_pre_list_dl[0]) + '%')
        sql_yd = "SELECT total_power FROM orig_sta_yd where sta_id=(select id from basic_sta_list WHERE sta_num='{}') and `date` like '{}'".format(sta, str(day_pre_list_yd[0]) + '%')
        result_dl = mysql.query(sql_dl)
        result_yd = mysql.query(sql_yd)


        # 2.算出 dl 平均值
        if len(result_dl) != 0:
            predict_value = 0
            for i in range(len(result_dl)):
                avg_test = result_dl[i][0]
                predict_value += avg_test
            predict_value_time_avg_dl = predict_value / len(result_dl)
        else:
            predict_value = 0
            predict_value_time_avg_dl = 0
        # day_pre_list_dl.append(predict_value_time_avg_dl)
        day_pre_list_dl.append(predict_value)
        result_list_dl.append(day_pre_list_dl)

        # 3.算出 yd 平均值
        if len(result_yd) != 0:
            predict_value = 0
            for i in range(len(result_yd)):
                avg_test = result_yd[i][0]
                predict_value += avg_test
            predict_value_time_avg_yd = predict_value / len(result_yd)
        else:
            predict_value_time_avg_yd = 0
        # print('--predict_value_time_avg_yd--', predict_value_time_avg_yd)
        # day_pre_list_yd.append(predict_value_time_avg_yd)
        day_pre_list_yd.append(predict_value)
        result_list_yd.append(day_pre_list_yd)

    resultdict['result_list_dl'] = result_list_dl
    resultdict['result_list_yd'] = result_list_yd

    for i in range(len(result_list_dl)):
        if result_list_dl[i][1] == 0:
            y_dl.append('')
        else:
            y_dl.append(result_list_dl[i][1])

    for i in range(len(result_list_yd)):
        if result_list_yd[i][1] == 0:
            y_yd.append('')
        else:
            y_yd.append(result_list_yd[i][1])

    resultdict['y_dl'] = y_dl
    resultdict['y_yd'] = y_yd

    # 4.算出相似度
    count = 0
    all_date_list = []
    for i in range(len(result_list_dl)):
        for j in range(len(result_list_yd)):
            if result_list_dl[i][1] != 0 and result_list_yd[j][1] != 0 and result_list_dl[i] == result_list_yd[j]:
                count += 1

    for i in range(len(result_list_dl)):
        if result_list_dl[i][1] != 0:
            all_date_list.append(result_list_dl[i][0])
    for j in range(len(result_list_yd)):
        if result_list_yd[j][1] != 0:
            all_date_list.append(result_list_dl[j][0])
    all_count = len(set(all_date_list))

    resultdict['count'] = count
    resultdict['all_count'] = all_count

    # 5.找出最大、最小用电量
    # 分自留、三方
    result_list_dl.sort(key=lambda x: x[1])
    max_dl = result_list_dl[-1]
    for i in range(len(result_list_dl)):
        if result_list_dl[i][1] != 0:
            min_dl = result_list_dl[i]
            break
        else:
            min_dl = 0
    max_dl[1] = float('%.3f' % float(max_dl[1]))
    min_dl[1] = float('%.3f' % float(min_dl[1]))
    resultdict['max_dl'] = max_dl
    resultdict['min_dl'] = min_dl

    result_list_yd.sort(key=lambda x: x[1])
    max_yd = result_list_yd[-1]
    for i in range(len(result_list_yd)):
        if result_list_yd[i][1] != 0:
            min_yd = result_list_yd[i]
            break
        else:
            min_yd = 0

    max_yd[1] = float('%.3f' % float(max_yd[1]))
    min_yd[1] = float('%.3f' % float(min_yd[1]))
    resultdict['max_yd'] = max_yd
    resultdict['min_yd'] = min_yd


    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps

