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


# ##############################################
#                                              #
#                  能耗预警页面                #
#                                              #
# ##############################################


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day*i


# # 找到所有基站
# def get_all_sta(veidoo=''):
#     mysql = MySQL(2)
#     mysql.mysql_connect()
#     resultdict = {}
#
#     if veidoo == '三方':
#         table_name = 'pre_warn_dl_sta'
#         sql = "select sta_name,sta_num FROM basic_sta_list WHERE sta_num in(select sta_id from {} WHERE color != 'green' GROUP BY sta_id)".format(table_name)
#
#     elif veidoo == '自留':
#         table_name = 'pre_warn_yd_sta'
#         sql = "select sta_name,sta_num FROM basic_sta_list WHERE id in(select sta_id from {} WHERE color != 'green' GROUP BY sta_id)".format(
#             table_name)
#     else:
#         print('--veidoo err!----')
#
#     result = mysql.query(sql)
#     data = []
#     for i in range(len(result)):
#         data.append(result[i][0])
#     resultdict['data'] = data
#
#     mysql.mysql_close()
#     reps = jsonify(resultdict)
#     reps.headers["Access-Control-Allow-Origin"] = "*"
#     return reps

# 1. 时间段
def data_list(veidoo=''):
    print('---veidoo---', veidoo)
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    if veidoo == '三方':
        table_name = 'pre_warn_dl_sta'

    elif veidoo == '自留':
        table_name = 'pre_warn_yd_sta'
    else:
        print('--veidoo err!----')

    resultdict['title'] = '时间'

    sql = "select min(`date`) as minday,max(`date`) as maxday from {}".format(table_name)
    result = mysql.query(sql)
    print('--result---', result)
    minday = str(result[0][0]).split(' ')[0]
    maxday = str(result[0][1]).split(' ')[0]

    resultdict['minday'] = minday
    resultdict['maxday'] = maxday

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.1 获取所有的电表
def get_ammeter():
    pass


# 2. 获取基站坐标
def get_x_y(veidoo='', StartDate='',EndDate=''):
    print('veidoo: ', veidoo)
    print('StartDate: ', StartDate)
    print('EndDate: ', EndDate)

    # 1.找到当天 基站颜色  、坐标
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    x_y_colour = []
    sta_id_list = []
    table_name = ''
    if StartDate != ''and EndDate != '':
        if veidoo == '三方':
            table_name = 'pre_warn_dl_sta'
            sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_id from {} WHERE color != 'green' and `date` BETWEEN '{}' and '{}'  GROUP BY sta_id))".format(
                table_name, StartDate, EndDate)
            print('--sql-0---', sql)
        elif veidoo == '自留':
            table_name = 'pre_warn_yd_sta'
            sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select sta_id from {} WHERE color != 'green' and `date` BETWEEN '{}' and '{}'  GROUP BY sta_id)".format(
                table_name, StartDate, EndDate)
            print('--sql--1--', sql)
        else:
            print('--veidoo err!----')

        result = mysql.query(sql)
        print('--result----', result)
        if len(result) > 0:
            for i in range(len(result)):
                x_y_colour.append(list(result[i])[1:])
                sta_id_list.append(result[i][0])
            print('--x_y_colour--0--', x_y_colour)
            print('--x_y_colour--len--', len(x_y_colour))
            if len(sta_id_list) > 0:
                if  veidoo == '三方':
                    if len(sta_id_list) == 1:
                        sql_color = "select color from {} WHERE 1=1 AND (`date` BETWEEN '{}' and '{}') and color != 'green' AND sta_id =(select sta_num FROM basic_sta_list WHERE id='{}')".format(table_name, StartDate, EndDate, result[i][0])
                        print('--sql-2---', sql_color)
                    else:
                        sql_color = "select color from {} WHERE 1=1 AND (`date` BETWEEN '{}' and '{}') and color != 'green' AND sta_id IN (select sta_num FROM basic_sta_list WHERE id in {})".format(table_name, StartDate, EndDate, tuple(sta_id_list))
                        print('--sql-3---', sql_color)
                elif  veidoo == '自留':
                    if len(sta_id_list) == 1:
                        sql_color = "select color from {} WHERE 1=1 AND (`date` BETWEEN '{}' and '{}') and color != 'green' AND sta_id ={}".format(table_name, StartDate, EndDate, result[i][0])
                        print('--sql-4---', sql_color)
                    else:
                        sql_color = "select color from {} WHERE 1=1 AND (`date` BETWEEN '{}' and '{}') and color != 'green' AND sta_id IN {}".format(table_name, StartDate, EndDate, tuple(sta_id_list))
                        print('--sql-5---', sql_color)
                result_color = mysql.query(sql_color)
                print('--result-1---', result_color)
                if len(result_color) > 0:
                    for i in range(len(x_y_colour)):
                        # x_y_colour[i].append(result_color[i][0])
                        x_y_colour[i].append('red')  # 直接用红色标注异常
                print('--result-2---', result_color)
                print('--x_y_colour-2---', x_y_colour)
            else:
                print('没找到坐标id!')
        else:
            print('没找到坐标!')
    else:
        print('--data err!----')
    resultdict['x_y_colour'] = x_y_colour
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 3. 获取详细信息
def get_xy_detile(x=0, y=0, veidoo='', StartDate='', EndDate=''):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    get_xy_detile = []
    get_detile = []
    table_name = ''

    if veidoo == '三方':
        table_name = 'pre_warn_dl_sta'

    elif veidoo == '自留':
        table_name = 'pre_warn_yd_sta'
    else:
        print('--veidoo err!----')

    resultdict['title'] = ['基站名', '负荷高低', '负荷比', '日期']
    if (x == 0 or x == '') and (y == 0 or y == ''):
        sta_id_list = []
        sql = "select sta_id,color,load_cap_ratio,`date` from {} WHERE color != 'green' AND `date` BETWEEN '{}' and '{}'".format(table_name, StartDate, EndDate)
        print('---sql-11-', sql)
        result_base = mysql.query(sql)
        print('---result_base-11-', result_base)
        for i in range(len(result_base)):
            sta_id_list.append(result_base[i][0])
            get_xy_detile.append(list(result_base[i]))
        result_list = []
        if len(sta_id_list) > 0:
            if veidoo == '三方':
                table_name = 'pre_warn_dl_sta'
                for i in range(len(sta_id_list)):
                    sql = "select sta_name from basic_sta_list WHERE sta_num ='{}'".format(sta_id_list[i])
                    result = mysql.query(sql)
                    result_list.append(result[0][0])
                # if len(sta_id_list) == 1:
                #     sql = "select sta_name from basic_sta_list WHERE sta_num ='{}'".format(sta_id_list[0])
                #     print('--sql--1----', sql)
                #     result = mysql.query(sql)
                # else:
                #     sta_id_list = tuple(sta_id_list)
                #     sql = "select sta_name from basic_sta_list WHERE sta_num in {}".format(sta_id_list)
                #     print('--sql--2----', sql)
                #     result = mysql.query(sql)

            elif veidoo == '自留':
                table_name = 'pre_warn_yd_sta'
                for i in range(len(sta_id_list)):
                    sql = "select sta_name from basic_sta_list WHERE sta_num =(select sta_num FROM basic_sta_list WHERE id='{}')".format(sta_id_list[i])
                    result = mysql.query(sql)
                    result_list.append(result[0][0])
                # if len(sta_id_list) == 1:
                #     sql = "select sta_name from basic_sta_list WHERE sta_num =(select sta_num FROM basic_sta_list WHERE id='{}')".format(sta_id_list[0])
                #     print('--sql--3----', sql)
                #     result = mysql.query(sql)
                # else:
                #     sta_id_list = tuple(sta_id_list)
                #     sql = "select sta_name from basic_sta_list WHERE sta_num in (select sta_num FROM basic_sta_list WHERE id in {})".format(sta_id_list)
                #     print('--sql--4----', sql)
                #     result = mysql.query(sql)
            else:
                print('--veidoo err!----')


        for i in range(len(get_xy_detile)):
            get_xy_detile[i][0] = result_list[i]
    elif (x != 0 and x != '') or (y != 0 and y != ''):
        # 1.通过xy 找到基站id 和基站名字
        # 2.通过基站id、时间、找到对应的detile
        # 3.合并基站和detile

        sql = "select id,sta_name FROM basic_sta_list WHERE id in (select sta_id from basic_sta_type WHERE lat LIKE '{}' AND lng LIKE '{}')".format(str(x)+'%',str(y)+'%',table_name)
        # sql = "select id,sta_name FROM basic_sta_list WHERE id in (select sta_id from basic_sta_type WHERE lat = '{}' AND lng = '{}')".format(str(x),str(y),table_name)
        print('----sql-12---', sql)
        result_base = mysql.query(sql)
        print('----result_base-12---', result_base)
        result_list = []
        if len(result_base) > 0:
            if len(result_base) == 1:
                if veidoo == '三方':
                    sql = "select sta_id,color,load_cap_ratio,`date` from {} WHERE color != 'green' AND (`date` BETWEEN '{}' and '{}') AND sta_id=(SELECT sta_num FROM basic_sta_list WHERE id={})".format(table_name, StartDate, EndDate, result_base[0][0])
                    print('---sql-13---', sql)
                elif veidoo == '自留':
                    sql = "select sta_id,color,load_cap_ratio,`date` from {} WHERE color != 'green' AND (`date` BETWEEN '{}' and '{}') AND sta_id={}".format(
                        table_name, StartDate, EndDate, result_base[0][0])
                    print('---sql-14---', sql)
                else:
                    print('--veidoo err!----')

                result = mysql.query(sql)
                print('---result-14---', result)
                for i in range(len(result)):
                    get_xy_detile.append(list(result[i]))
                    get_xy_detile[i][0] = result_base[0][1]
                print('---get_xy_detile-11---', get_xy_detile)
            else:
                result_base_list = []
                id_list = []
                for i in range(len(result_base)):
                    result_base_list.append(result_base[i][0])
                if veidoo == '三方':
                    sql = "select sta_id,color,load_cap_ratio,`date` from {} WHERE color != 'green' AND (`date` BETWEEN '{}' and '{}') AND sta_id in (SELECT sta_num FROM basic_sta_list WHERE id in {})".format(
                        table_name, StartDate, EndDate, tuple(result_base_list))
                    print('---sql-15---', sql)
                elif veidoo == '自留':
                    sql = "select sta_id,color,load_cap_ratio,`date` from {} WHERE color != 'green' AND (`date` BETWEEN '{}' and '{}') AND sta_id in {}".format(
                        table_name, StartDate, EndDate, tuple(result_base_list))
                    print('---sql-16---', sql)
                else:
                    print('--veidoo err!----')


                result = mysql.query(sql)
                print('---result-16---', result)
                for i in range(len(result)):
                    get_xy_detile.append(list(result[i]))
                    id_list.append(result[i][0])
                print('--id_list-1-', id_list)
                if len(id_list) > 0:
                    if veidoo == '三方':
                        table_name = 'pre_warn_dl_sta'
                        for i in range(len(id_list)):
                            sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id =(SELECT id FROM basic_sta_list WHERE sta_num='{}'))".format(
                                id_list[i])
                            print('--sql-17-', sql)
                            result = mysql.query(sql)
                            print('--result-17-', result)
                            result_list.append(result[0][0])
                            print('--result_list-17-', result_list)
                        # if len(id_list) == 1:
                        #     print('--comming----')
                        #     sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id =(SELECT id FROM basic_sta_list WHERE sta_num='{}'))".format(
                        #         id_list[0])
                        #     print('--sql--=1----', sql)
                        # else:
                        #     sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id in (SELECT id FROM basic_sta_list WHERE sta_num in {}))".format(
                        #         tuple(id_list))
                        #     print('--sql--=qita----', sql)

                    elif veidoo == '自留':
                        table_name = 'pre_warn_yd_sta'
                        for i in range(len(id_list)):
                            sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id ='{}')".format(id_list[i])
                            result = mysql.query(sql)
                            print('--sql-18-', sql)
                            result_list.append(result[0][0])
                            print('--result_list-18-', result_list)

                        # if len(id_list) == 1:
                        #     print('--comming----')
                        #     sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id ='{}')".format(
                        #         id_list[0])
                        #     print('--sql--=1----', sql)
                        # else:
                        #     sql = "select sta_name FROM basic_sta_list where sta_num in(select sta_num FROM basic_sta_list WHERE id in {})".format(
                        #         tuple(id_list))
                        #     print('--sql--=qita----', sql)
                    else:
                        print('--veidoo err!----')


                else:
                    print('-id_list为空!--')
                # print('--sql--6----', sql)
                # result_base = mysql.query(sql)
                # print('--result_base--6----', result_base)
                for i in range(len(result_list)):
                    get_xy_detile[i][0] = result_list[i]
                print('--get_xy_detile-18-', get_xy_detile)


    for i in range(len(get_xy_detile)):
        get_xy_detile[i][2] = str('%.3f' % float(get_xy_detile[i][2]))
        if get_xy_detile[i][1] == 'green':
            get_xy_detile[i][1] = '正常'
        if get_xy_detile[i][1] == 'red':
            get_xy_detile[i][1] = '过高'
        if get_xy_detile[i][1] == 'yellow':
            get_xy_detile[i][1] = '过低'

    resultdict['get_xy_detile'] = get_xy_detile
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 4, 电费预警：
def electrical_warning(PageIndex=1):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    resultdict['title'] = ['用户', '实际电费', '收取电费', '是否预警']
    resultdict['electrical_warning'] = [['zzz', '123', '234', '是'], ['yyy', '100', '100', '否']]
    resultdict["rowCount"] = 2
    resultdict["pageCount"] = 1
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
