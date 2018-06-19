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
#                  同类站对比页面                #
#                                              #
# ##############################################

# 0. 高压、低压
def get_high_low_vol():
    resultdict = {}
    resultdict['title'] = '高低压'
    resultdict['way_of_cmp'] = ['高压', '低压']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.同类站对比方式
def way_of_cmp():
    resultdict = {}

    resultdict['title'] = '同类站对比方式'
    resultdict['way_of_cmp'] = ['基站分布', '基站类别', '客户名称']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 2.同类划分
def child_way_cmp(way_of_cmp='',high_low_vol=''):
    print('---way_of_cmp-', way_of_cmp)
    print('---high_low_vol-', high_low_vol)
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    chile_way = []
    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
    elif high_low_vol == '高压':
        table = 'xgdl_high_voltage_user'
    else:
        print('--high_low_vol err!-')
    if way_of_cmp == '基站分布':
        sql = "select layout from {} GROUP BY layout".format(table)
        print('--sql--1--', sql)
    elif way_of_cmp == '基站类别':
        sql = "select sta_type from {} GROUP BY sta_type".format(table)
        print('--sql--2--', sql)
    elif way_of_cmp == '客户名称':
        sql = "select user_name from {} GROUP BY user_name".format(table)
        print('--sql--3--', sql)
    else:
        print('--way_of_cmp err!--')

    result = mysql.query(sql)
    if len(result) > 0:
        for i in range(len(result)):
            chile_way.append(result[i][0])
    else:
        print('没有同类分类后的子类')
    chile_way.reverse()
    print('----chile_way-', chile_way)
    resultdict['title'] = '同类划分子类'
    resultdict['chile_way'] = chile_way

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 3.时间选择
def time_choose(high_low_vol=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
    elif high_low_vol == '高压':
        table = 'xgdl_high_voltage_user'
    else:
        print('--high_low_vol err!-')

    sql = "select min(`date`) as minday,max(`date`) as maxday from {}".format(table)
    print('--sql--1--', sql)
    result = mysql.query(sql)
    minday = str(result[0][0])
    maxday = str(result[0][1])

    print('--minday----', minday)
    print('--maxday----', maxday)

    # 找出某段日期内的所有的日期列表
    data_list = com.get_days_list(minday, maxday)
    print('--data_list----', data_list)
    resultdict['title'] = '时间'
    resultdict['date_list'] = data_list

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 4. 同类对比柱图展示
# 1.选择的子类型--》基站列表
# 2.基站列表和时间--》找到基站、用电量
def same_kind_chart(way_of_cmp='',child_way_cmp='', date_choose='', high_low_vol='', choose_city=''):
    resultdict = {}
    print('--date_choose--', date_choose)
    next_day = com.get_y_t_date(date_choose, '1', count=1)
    next_day = str(next_day).split(' ')[0]
    print('--next_day--', next_day)

    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_name_list = []
    total_power = []

    if way_of_cmp == '基站分布':
        row = 'layout'
    elif way_of_cmp == '基站类别':
        row = 'sta_type'
    elif way_of_cmp == '客户名称':
        row = 'user_name'
    else:
        print('--way_of_cmp err!--')

    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
        if choose_city == 'all':
            sql_base = "select sta_no,sta_name,active_ele,`date`,total_ratio,met_address FROM xgdl_low_voltage_user WHERE {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(row, child_way_cmp, date_choose, next_day)
        else:
            sql_base = "select sta_no,sta_name,active_ele,`date`,total_ratio,met_address FROM xgdl_low_voltage_user WHERE city = '{}' AND {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(choose_city ,row, child_way_cmp, date_choose, next_day)

        print('--sql_base--1--', sql_base)
        result_base = mysql.query(sql_base)
        print('--result_base--1--', result_base)
        result_list = []
        for i in range(len(result_base)):
            m = 0
            result_single = []
            for j in range(len(result_base)):
                if result_base[i][0] == result_base[j][0] and result_base[i][5] == result_base[j][5] and result_base[i][2] > result_base[j][2]:
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(str(result_base[j][1]) + '_' + str(result_base[j][0]) + '_' + result_base[j][5])
                        print('---result_base[i][3]--',result_base[i][3])
                        print('---result_base[i][2]--',result_base[i][2])
                        print('---result_base[j][2]--',result_base[j][2])
                        print('---result_base[i][4]--',result_base[i][4])
                        result_single.append(float('%.3f' % float((float(result_base[i][2]) - float(result_base[j][2]))* float(result_base[i][4]))))
                        result_list.append(result_single)
        print('-result_list--', result_list)
        new_result_list = []
        for id in result_list:
            if id not in new_result_list:
                new_result_list.append(id)
        new_result_list.sort(key=lambda x: x[1])
        new_result_list.reverse()
        for k in range(len(new_result_list)):
            sta_name_list.append(new_result_list[k][0])
            total_power.append(new_result_list[k][1])

    elif high_low_vol == '高压':
        table = 'xgdl_high_voltage_user'
        if choose_city == 'all':
            sql_base = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(row, child_way_cmp, date_choose, next_day)
            sql_base_1 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                row, child_way_cmp, date_choose, next_day)
            sql_base_2 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                row, child_way_cmp, date_choose, next_day)
        else:
            sql_base = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                choose_city, row, child_way_cmp, date_choose, next_day)
            sql_base_1 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                choose_city,
                row, child_way_cmp, date_choose, next_day)
            sql_base_2 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                choose_city,
                row, child_way_cmp, date_choose, next_day)

        print('--sql_base----', sql_base)
        print('--sql_base_1----', sql_base_1)
        print('--sql_base_2----', sql_base_2)
        result_base = mysql.query(sql_base)
        result_base_1 = mysql.query(sql_base_1)
        result_base_2 = mysql.query(sql_base_2)
        print('--result_base----', result_base)
        print('--result_base--1--', result_base_1)
        print('--result_base--2--', result_base_2)
        result_list = []
        result_list_0 = []
        result_list_1 = []
        result_list_2 = []
        for i in range(len(result_base)):
            m = 0
            x = 0
            y = 0
            result_single = []
            result_single_1 = []
            result_single_2 = []
            for j in range(len(result_base)):
                if result_base[i][0] == result_base[j][0] and result_base[i][3] > result_base[j][3] and result_base[i][2] != '' and result_base[j][2] != '':
                    if m > 1:
                        break
                    else:
                        m += 1
                        if result_base[i][4] == '':
                            not_active_ele_1 = '%.3f' % float(0)
                        else:
                            not_active_ele_1 = '%.3f' % float(result_base[i][4])
                        if result_base[j][4] == '':
                            not_active_ele_2 = '%.3f' % float(0)
                        else:
                            not_active_ele_2 = '%.3f' % float(result_base[j][4])
                        result_single.append(str(result_base[j][1]) + '_' + str(result_base[j][0]))
                        print('result_base[i][2]: ',result_base[i][2])
                        print('not_active_ele_1: ',not_active_ele_1)
                        print('result_base[j][2]: ',result_base[j][2])
                        print('not_active_ele_2: ',not_active_ele_2)
                        print('result_base[i][5]: ',result_base[i][5])
                        result_single.append('%.3f' % float((float(result_base[i][2]) + float(not_active_ele_1) - float(result_base[j][2]) - float(not_active_ele_2)) * float(result_base[i][5])))
                        result_list_0.append(result_single)
                if result_base_1[i][0] == result_base_1[j][0] and result_base_1[i][3] > result_base_1[j][3] and result_base_1[i][2] != '' and result_base_1[j][2] != '':
                    if x > 1:
                        break
                    else:
                        x += 1
                        if result_base_1[i][4] == '':
                            not_active_ele_1 = '%.3f' % float(0)
                        else:
                            not_active_ele_1 = '%.3f' % float(result_base_1[i][4])
                        if result_base_1[j][4] == '':
                            not_active_ele_2 = '%.3f' % float(0)
                        else:
                            not_active_ele_2 = '%.3f' % float(result_base_1[j][4])
                        result_single_1.append(str(result_base_1[i][1]) + '_' + str(result_base_1[i][0]))
                        result_single_1.append(str('%.3f' % float((float(result_base_1[i][2]) + float(not_active_ele_1) - float(result_base_1[j][2]) - float(not_active_ele_2)) * int(result_base[i][5]))))
                        result_list_1.append(result_single_1)
                if result_base_2[i][0] == result_base_2[j][0] and result_base_2[i][3] > result_base_2[j][3] and result_base_2[i][2] != '' and result_base_2[j][2] != '':
                    if y > 1:
                        break
                    else:
                        y += 1
                        if result_base_2[i][4] == '':
                            not_active_ele_1 = '%.3f' % float(0)
                        else:
                            not_active_ele_1 = '%.3f' % float(result_base_2[i][4])
                        if result_base_2[j][4] == '':
                            not_active_ele_2 = '%.3f' % float(0)
                        else:
                            not_active_ele_2 = '%.3f' % float(result_base_2[j][4])
                        result_single_2.append(str(result_base_2[i][1]) + '_' + str(result_base_2[i][0]))
                        result_single_2.append(str('%.3f' % float((float(result_base_2[i][2]) + float(not_active_ele_1) - float(result_base_2[j][2]) - float(not_active_ele_2)) * int(result_base[i][5]))))
                        result_list_2.append(result_single_2)
        print('-result_list_0--', result_list_0)
        print('-result_list_1--', result_list_1)
        print('-result_list_2--', result_list_2)
        for i in range(len(result_list_0)):
            result_list_single = []
            result_list_single.append(result_list_0[i][0])
            print('---result_list_0[0][1]--', result_list_0[0][1])
            print('---result_list_1[0][1]--', result_list_1[0][1])
            print('---result_list_2[0][1]--', result_list_2[0][1])
            result_list_single.append(float('%.3f' % float(float(result_list_0[i][1]) + float(result_list_1[i][1]) + float(result_list_2[i][1]))))
            result_list.append(result_list_single)
        print('-result_list-66-', result_list)
        new_result_list = []
        for id in result_list:
            if id not in new_result_list:
                new_result_list.append(id)
        new_result_list.sort(key=lambda x: x[1])
        new_result_list.reverse()
        print('-result_list--', new_result_list)
        for k in range(len(new_result_list)):
            sta_name_list.append(new_result_list[k][0])
            total_power.append(new_result_list[k][1])

    else:
        print('--high_low_vol err!-')

    resultdict['sta_name_list'] = sta_name_list
    resultdict['total_power'] = total_power

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 结果集展示:
def details_show_tz(way_of_cmp='',child_way_cmp='', date_choose='', high_low_vol='', sta_name='', PageIndex=1, choose_city=''):
    print('--way_of_cmp--', way_of_cmp)
    print('--child_way_cmp--', child_way_cmp)
    print('--date_choose--', date_choose)
    print('--high_low_vol--', high_low_vol)
    print('--sta_name--', sta_name)
    print('--PageIndex--', PageIndex)
    print('--------------------------------------------------------')

    print('--date_choose--', date_choose)
    next_day = com.get_y_t_date(date_choose, '1', count=1)
    next_day = str(next_day).split(' ')[0]
    print('--next_day--', next_day)

    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_name_list = []
    total_power = []

    if way_of_cmp == '基站分布':
        row = 'layout'
    elif way_of_cmp == '基站类别':
        row = 'sta_type'
    elif way_of_cmp == '客户名称':
        row = 'user_name'
    else:
        print('--way_of_cmp err!--')

    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
        # 1. 获取工单标题
        title = ['id', '县市', '基站编号', '基站名称', '客户编号', '基站类型', '分布', '客户名称', '供电单位', '电表地址', '数据日期', '正向有功电能示值', '综合倍率']

        # sql_base = "select sta_no,sta_name,active_ele,`date` FROM xgdl_low_voltage_user WHERE {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(
        #     row, child_way_cmp, date_choose, next_day)
        # sta_no, sta_name, active_ele, `date`
        # 2 、 3、11 、10 、12
        if choose_city == 'all':
            if sta_name == '' or sta_name == '全部':
                sql_base = "select * FROM xgdl_low_voltage_user WHERE {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(row, child_way_cmp, date_choose, next_day)
            else:
                sql_base = "select * FROM xgdl_low_voltage_user WHERE sta_no='{}' and  {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(sta_name.split('_')[1],
                    row, child_way_cmp, date_choose, next_day)
        else:
            if sta_name == '' or sta_name == '全部':
                sql_base = "select * FROM xgdl_low_voltage_user WHERE city = '{}' AND {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(choose_city, row, child_way_cmp, date_choose, next_day)
            else:
                sql_base = "select * FROM xgdl_low_voltage_user WHERE city = '{}' AND sta_no='{}' and  {}='{}' AND `date` BETWEEN '{}' AND '{}'  order BY sta_name desc".format(choose_city, sta_name.split('_')[1],
                    row, child_way_cmp, date_choose, next_day)

        print('--sql_base--1--', sql_base)
        result_base = mysql.query(sql_base)
        print('--result_base--1--', result_base)
        result_list = []
        for i in range(len(result_base)):
            m = 0
            result_single = []
            for j in range(len(result_base)):
                if result_base[i][2] == result_base[j][2] and result_base[i][9] == result_base[j][9] and result_base[i][11] > result_base[j][11]:
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(list(result_base[j]))
                        print('---result_base[i])---', result_base[i])
                        print('---result_base[j])---', result_base[j])
                        print('---result_base[j][11])---', result_base[j][11])
                        print('---result_base[i][11])---', result_base[i][11])
                        print('---result_base[j][11]---', result_base[j][11])
                        print('---result_base[i][12]---', result_base[i][12])
                        result_single[0][11] = float('%.3f' % float((float(result_base[i][11]) - float(result_base[j][11]))))
                        print('---result_single[0][11]---', result_single[0][11])
                        print('---result_single[0]---', result_single[0])
                        # result_single.append(str(result_base[i][1]) + '_' + str(result_base[i][0]))
                        # result_single.append(float('%.3f' % float(float(result_base[i][2]) - float(result_base[j][2]))))
                        result_list.append(result_single[0])
        print('-result_list--', result_list)
        new_result_list = []
        for id in result_list:
            if id not in new_result_list:
                new_result_list.append(id)
        new_result_list.sort(key=lambda x: x[11])
        new_result_list.reverse()
        show_tz = com.paging(new_result_list,everyPage_count=10,PageIndex=PageIndex)
        page_resultList = show_tz[0]
        rowCount = show_tz[1]
        pageCount = show_tz[2]

        # for k in range(len(result_list)):
        #     sta_name_list.append(result_list[k][0])
        #     total_power.append(result_list[k][1])

    elif high_low_vol == '高压':
        title = ['id', '县市', '基站编号', '基站名称', '客户编号', '基站类型', '分布', '客户名称', '供电单位', '数据日期', '三相正向有功总电能示值', '三相正向无功总电能示值', '综合倍率', '电流曲线相序']

        table = 'xgdl_high_voltage_user'
        # sql_base = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
        #     row, child_way_cmp, date_choose, next_day)
        # sql_base_1 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
        #     row, child_way_cmp, date_choose, next_day)
        # sql_base_2 = "select sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
        #     row, child_way_cmp, date_choose, next_day)
        # sta_no,sta_name,3_active_ele,`date`,3_not_active_ele,total_ratio
        # 2 、 3、10 、9 、11、12
        if choose_city == 'all':
            if sta_name == '' or sta_name == '全部':
                sql_base = "select * FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                    row, child_way_cmp, date_choose, next_day)
                sql_base_1 = "select * FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                    row, child_way_cmp, date_choose, next_day)
                sql_base_2 = "select * FROM xgdl_high_voltage_user WHERE {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(
                    row, child_way_cmp, date_choose, next_day)
            else:
                sql_base = "select * FROM xgdl_high_voltage_user WHERE sta_no='{}' and {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)
                sql_base_1 = "select * FROM xgdl_high_voltage_user WHERE sta_no='{}' and {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)
                sql_base_2 = "select * FROM xgdl_high_voltage_user WHERE sta_no='{}' and {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)
        else:
            if sta_name == '' or sta_name == '全部':
                sql_base = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city,
                    row, child_way_cmp, date_choose, next_day)
                sql_base_1 = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city,
                    row, child_way_cmp, date_choose, next_day)
                sql_base_2 = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city,
                    row, child_way_cmp, date_choose, next_day)
            else:
                sql_base = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND sta_no='{}' and {}='{}' and ele_curve= 'A相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city, sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)
                sql_base_1 = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND sta_no='{}' and {}='{}' and ele_curve= 'B相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city, sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)
                sql_base_2 = "select * FROM xgdl_high_voltage_user WHERE city = '{}' AND sta_no='{}' and {}='{}' and ele_curve= 'C相' AND(`date` BETWEEN '{}' AND '{}') order BY sta_name desc".format(choose_city, sta_name.split('_')[1],row, child_way_cmp, date_choose, next_day)

        print('--sql_base----', sql_base)
        print('--sql_base_1----', sql_base_1)
        print('--sql_base_2----', sql_base_2)
        result_base = mysql.query(sql_base)
        result_base_1 = mysql.query(sql_base_1)
        result_base_2 = mysql.query(sql_base_2)
        print('--result_base----', result_base)
        print('--result_base--1--', result_base_1)
        print('--result_base--2--', result_base_2)
        result_list = []
        result_list_0 = []
        result_list_1 = []
        result_list_2 = []
        for i in range(len(result_base)):
            m = 0
            x = 0
            y = 0
            result_single = []
            result_single_1 = []
            result_single_2 = []
            for j in range(len(result_base)):
                if result_base[i][2] == result_base[j][2] and result_base[i][9] > result_base[j][9] and result_base[i][10] != '' and result_base[j][10] != '':
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(list(result_base[j]))

                        result_single[0][10] = float('%.3f' % float(float(result_base[i][10]) - float(result_base[j][10])))
                        if result_base[i][11] == '':
                            base_1 = '%.3f' % float(0)
                        else:
                            base_1 = '%.3f' % float(float(result_base[i][11]))
                        if result_base[j][11] == '':
                            base_2 = '%.3f' % float(0)
                        else:
                            base_2 = '%.3f' % float(float(result_base[j][11]))
                        print('---result_single[0]----', result_single[0])
                        print('---result_single[0][11]----', result_single[0][11])
                        result_single[0][11] = str('%.3f' % float(float(base_1) - float(base_2)))
                        # result_single.append(str(result_base[i][3]) + '_' + str(result_base[i][2]))
                        # result_single.append(str('%.3f' % float(float(result_base[i][2]) - float(result_base[j][2]))))
                        result_list_0.append(result_single[0])
                if result_base_1[i][2] == result_base_1[j][2] and result_base_1[i][9] > result_base_1[j][9] and \
                                result_base_1[i][10] != '' and result_base_1[j][10] != '':
                    if x > 1:
                        break
                    else:
                        x += 1
                        result_single_1.append(list(result_base_1[j]))
                        print('result_base_1[i]: ', result_base_1[i])
                        print('result_base_1[j]: ', result_base_1[j])
                        result_single_1[0][10] = float('%.3f' % float(float(result_base_1[i][10]) - float(result_base_1[j][10])))
                        if result_base_1[i][11] == '':
                            base_1 = '%.3f' % float(float(0))
                        else:
                            base_1 = '%.3f' % float(float(result_base_1[i][11]))
                        if result_base_1[j][11] == '':
                            base_2 = '%.3f' % float(float(0))
                        else:
                            base_2 = '%.3f' % float(float(result_base_1[j][11]))
                            result_single_1[0][11] = str(float('%.3f' % float(float(base_1) - float(base_2))))
                        # result_single_1[0][11] = str(float('%.3f' % float(float(result_single_1[i][11]) - float(result_single_1[j][11]))))
                        # result_single_1.append(str(result_base_1[i][3]) + '_' + str(result_base_1[i][2]))
                        # result_single_1.append(str('%.3f' % float(float(result_base_1[i][2]) - float(result_base_1[j][2]))))
                        result_list_1.append(result_single_1[0])
                if result_base_2[i][2] == result_base_2[j][2] and result_base_2[i][9] > result_base_2[j][9] and \
                                result_base_2[i][10] != '' and result_base_2[j][10] != '':
                    if y > 1:
                        break
                    else:
                        y += 1
                        result_single_2.append(list(result_base_2[j]))
                        result_single_2[0][10] = float('%.3f' % float(float(result_base_2[i][10]) - float(result_base_2[j][10])))
                        if result_base_2[i][11] == '':
                            base_1 = '%.3f' % float(float(0))
                        else:
                            base_1 = '%.3f' % float(float(result_base_2[i][11]))
                        if result_base_2[j][11] == '':
                            base_2 = '%.3f' % float(float(0))
                        else:
                            base_2 = '%.3f' % float(float(result_base_2[j][11]))
                            result_single_2[0][11] = str(float('%.3f' % float(float(base_1) - float(base_2))))
                        # result_single_2[0][11] = str(float('%.3f' % float(float(result_single_2[i][11]) - float(result_single_2[j][11]))))
                        # result_single_2.append(str(result_base_2[i][3]) + '_' + str(result_base_2[i][2]))
                        # result_single_2.append(str('%.3f' % float(float(result_base_2[i][2]) - float(result_base_2[j][2]))))
                        result_list_2.append(result_single_2[0])
        print('-result_list_0--', result_list_0)
        print('-result_list_1--', result_list_1)
        print('-result_list_2--', result_list_2)
        for i in range(len(result_list_0)):
            result_list.append(result_list_0[i])
            result_list.append(result_list_1[i])
            result_list.append(result_list_2[i])
            # result_list_single = []
            # result_list_single.append(result_list_0[i][0])
            # result_list_single.append(float('%.3f' % float(
            #     float(result_list_0[i][1]) + float(result_list_1[i][1]) + float(result_list_2[i][1]) / 3)))
            # result_list.append(result_list_single)
        print('-result_list-66-', result_list)
        new_result_list = []
        for dd in result_list:
            print('--dd--', dd)
            if dd not in new_result_list:
                new_result_list.append(dd)
        print('-new_result_list-66-', new_result_list)
        new_result_list.sort(key=lambda x: x[11])
        new_result_list.reverse()
        show_tz = com.paging(new_result_list, everyPage_count=10, PageIndex=PageIndex)
        # show_tz = com.paging(result_list, everyPage_count=10, PageIndex=PageIndex)
        page_resultList = show_tz[0]
        rowCount = show_tz[1]
        pageCount = show_tz[2]
        print('-result_list--', result_list)
        # for k in range(len(result_list)):
        #     sta_name_list.append(result_list[k][0])
        #     total_power.append(result_list[k][1])

    else:
        title = []
        page_resultList = []
        rowCount = 0
        pageCount = 0
        print('--high_low_vol err!-')

    resultdict['title'] = title
    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps