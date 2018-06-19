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
import time


# ##############################################
#                                              #
#                  首页                        #
#                                              #
# ##############################################

# 1. 地图上首先显示所有正常、异常、警告状态
# 2. 异常跳变 top 10展示
# 3.

# 1. 正常、异常、告警
def count_warning():
    resultdict = {}
    count_warning = [['异常'], ['正常'], ['告警']]
    mysql = MySQL(2)
    mysql.mysql_connect()

    sql_0 = "select count(id) from xgld_load_abnormal WHERE `type` = '正常'"
    sql_1 = "select count(id) from xgld_load_abnormal WHERE `type` = '基站未工作' or  `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常'"
    sql_2 = "select count(id) from xgld_load_abnormal WHERE `type` = '负荷过高' or `type` = '反季节变化'"
    sql_3 = "select count(id) from xgld_load_abnormal"

    result_0 = mysql.query(sql_0)
    result_1 = mysql.query(sql_1)
    result_2 = mysql.query(sql_2)
    result_3 = mysql.query(sql_3)

    count_warning[0].append(result_1[0][0])
    count_warning[0].append('%.2f' % float(int(result_1[0][0]) / int(result_3[0][0]) * 100) + '%')
    count_warning[1].append(result_0[0][0])
    count_warning[1].append('%.2f' % float(int(result_0[0][0]) / int(result_3[0][0]) * 100) + '%')
    count_warning[2].append(result_2[0][0])
    count_warning[2].append('%.2f' % float(int(result_2[0][0]) / int(result_3[0][0]) * 100) + '%')

    print('-count_warning---', count_warning)
    resultdict['count_warning'] = count_warning

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 正常： 正常
# 警告：反季节变化
# 异常：基站未工作、负荷过高、负荷曲线连续三个月以上基本无变化、跳变异常

# 第二版
# 1.获取首页地图坐标
def get_xy(colour='', sta_no='', choose_city=''):
    print('colour: ', colour)
    print('sta_no: ', sta_no)
    print('choose_city: ', choose_city)

    # choose_city = 'all'
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    x_y_colour = []
    x_y_colour_1 = []
    back_xy = []
    sta_id_list = []
    sta_id_list_1 = []
    result_2 = []
    result_0_sta = []
    result_1_sta = []
    print('time_1: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if choose_city == 'all':
        sql_0 = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE  sta_num in (SELECT sta_no FROM basic_city_list))"
    else:
        sql_0 = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE  sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}'))".format(choose_city)
    sql_1 = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_num from xgld_load_abnormal))"
    print('--sql----', sql_0)
    result_0 = mysql.query(sql_0)
    result_1 = mysql.query(sql_1)
    for i in range(len(result_0)):
        # result_2.append(list(result_0[i]))
        result_0_sta.append(result_0[i][0])
    for i in range(len(result_1)):
        result_1_sta.append(result_1[i][0])
    for i in range(len(result_1)):
        if result_1[i][0] in result_0_sta:
            result_2.append(list(result_1[i]))
    print('--result_2----', result_2)
    print('--result_2----', len(result_2))
    print('time_2: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if len(result_2) > 0:
        for i in range(len(result_2)):
            x_y_colour.append(list(result_2[i])[1:])
            sta_id_list.append(result_2[i][0])
        print('--x_y_colour--0--', x_y_colour)
        print('--x_y_colour--len--', len(x_y_colour))
        type_list = []
        colour_list = []
        if len(sta_id_list) > 0:
            print('--sta_id_list--len--', len(sta_id_list))
            if len(sta_id_list) == 1:
                sql_type = "select `type`,mean from xgld_load_abnormal WHERE  sta_num =(select sta_num FROM basic_sta_list WHERE id='{}')".format(sta_id_list[0])
            else:
                sql_type = "select `type`,mean from xgld_load_abnormal WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in {})".format(tuple(sta_id_list))
            result_type = mysql.query(sql_type)
            print('--sql_type-2---', sql_type)
            print('--result_type-2---', result_type)
            print('--result_type-2---', len(result_type))
            print('time_3: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

            for i in range(len(sta_id_list)):
                type_list.append(result_type[i][0])
            print('--type_list----', type_list)
            print('--type_list--len--', len(type_list))
            for i in range(len(type_list)):
                # if '正常' in str(type_list[i]):
                if str(type_list[i]) == '正常':
                    colour_list.append('green')
                elif str(type_list[i]) == '负荷过高' or str(type_list[i]) == '反季节变化':
                    colour_list.append('red')
                elif str(type_list[i]) == '基站未工作' or str(type_list[i]) == '负荷曲线连续三个月以上基本无变化' or str(type_list[i]) == '跳变异常':
                    colour_list.append('yellow')
                else:
                    print('--i:', i)
                    print('type_list[i]:', type_list[i])
            print('--colour_list-1---', colour_list)
            print('--colour_list-1---', len(colour_list))
            if len(colour_list) > 0:
                for i in range(len(x_y_colour)):
                    x_y_colour[i].append(colour_list[i])
                    x_y_colour[i].append(result_type[i][1])
            print('--x_y_colour-2---', x_y_colour)
            print('time_4: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        else:
            print('没找到坐标id!')
    else:
        print('没找到坐标!')


    for i in range(len(x_y_colour)):
        # if x_y_colour[i][3] > 300:
        #     print('-x_y_colour[i][3]---', x_y_colour[i][3])
        if x_y_colour[i][3] > 300 and x_y_colour[i][3] < 2000:
            x_y_colour[i][3] = 300
        if x_y_colour[i][3] > 2000:
            x_y_colour[i][3] = 320

    if sta_no != '' and sta_no != '全部':
        sql = "select lat,lng from basic_sta_type WHERE sta_id =(select id FROM basic_sta_list WHERE sta_num='{}')".format(sta_no.split('_')[0])
        print('--sql-2---', sql)
        result = mysql.query(sql)
        back_xy.append(result[0][0])
        back_xy.append(result[0][1])
        x_y_colour = [[result[0][0], result[0][1], 'red', 300]]
    print('time_5: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    for i in range(len(x_y_colour)):
        if x_y_colour[i][2] == 'red':
            x_y_colour_1.append(x_y_colour[i])
    print('--x_y_colour--', x_y_colour)
    # 测试：
    x_y_colour = x_y_colour[:100]
    print('--x_y_colour--', x_y_colour)

    resultdict['x_y_colour'] = x_y_colour
    resultdict['x_y_colour_1'] = x_y_colour_1
    resultdict['back_xy'] = back_xy



    print('完')
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第一版
# 1.获取首页地图坐标
def get_xy_old(colour='', sta_no=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    x_y_colour = []
    back_xy = []
    sta_id_list = []

    if colour == '' or colour == '全部':
        sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_num from xgld_load_abnormal))"
    elif colour == '红':
        sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_num from xgld_load_abnormal " \
              "AND (`type` = '基站未工作' or `type` = '负荷过高' or `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常')))"
    elif colour == '黄':
        sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_num from xgld_load_abnormal " \
              "AND `type` = '反季节变化'))"
    elif colour == '绿':
        sql = "select sta_id,lat,lng FROM basic_sta_type WHERE sta_id in (select id FROM basic_sta_list WHERE sta_num in(select sta_num from xgld_load_abnormal " \
              "AND `type` = '正常'))"
    else:
        print('colour err!')
    print('--sql----', sql)

    result = mysql.query(sql)
    print('--result----', result)
    if len(result) > 0:
        for i in range(len(result)):
            x_y_colour.append(list(result[i])[1:])
            sta_id_list.append(result[i][0])
        print('--x_y_colour--0--', x_y_colour)
        print('--x_y_colour--len--', len(x_y_colour))
        type_list = []
        colour_list = []
        if len(sta_id_list) > 0:
            print('--sta_id_list--len--', len(sta_id_list))
            if len(sta_id_list) == 1:
                sql_type = "select `type`,jump from xgld_load_abnormal WHERE sta_num =(select sta_num FROM basic_sta_list WHERE id='{}')".format(sta_id_list[0])
            else:
                sql_type = "select `type`,jump from xgld_load_abnormal WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in {})".format(tuple(sta_id_list))
            result_type = mysql.query(sql_type)
            print('--sql_type-2---', sql_type)
            print('--result_type-2---', result_type)
            print('--result_type-2---', len(result_type))

            for i in range(len(sta_id_list)):
                type_list.append(result_type[i][0])
            print('--type_list----', type_list)
            print('--type_list--len--', len(type_list))
            for i in range(len(type_list)):
                # if '正常' in str(type_list[i]):
                if str(type_list[i]) == '正常':
                    colour_list.append('green')
                elif str(type_list[i]) == '反季节变化':
                    colour_list.append('yellow')
                elif str(type_list[i]) == '基站未工作' or str(type_list[i]) == '负荷过高' or str(type_list[i]) == '负荷曲线连续三个月以上基本无变化' or str(type_list[i]) == '跳变异常':
                    colour_list.append('red')
                else:
                    print('--i:', i)
                    print('type_list[i]:', type_list[i])
            print('--colour_list-1---', colour_list)
            print('--colour_list-1---', len(colour_list))
            if len(colour_list) > 0:
                for i in range(len(x_y_colour)):
                    x_y_colour[i].append(colour_list[i])
                    x_y_colour[i].append(result_type[i][1])
            print('--x_y_colour-2---', x_y_colour)
        else:
            print('没找到坐标id!')
    else:
        print('没找到坐标!')

    if sta_no != '':
        sql = "select lat,lng from basic_sta_type WHERE sta_id =(select id FROM basic_sta_list WHERE sta_num='{}')".format(sta_no)
        print('--sql-2---', sql)
        result = mysql.query(sql)
        back_xy.append(result[0][0])
        back_xy.append(result[0][1])

    resultdict['x_y_colour'] = x_y_colour
    resultdict['back_xy'] = back_xy

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def sta_name_list(x=0, y=0, choose_city=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_list = []
    print('choose_city: ', choose_city)
    # choose_city = 'all'
    if choose_city == 'all':
        sql = "select sta_num,sta_name from basic_sta_list WHERE id IN (SELECT sta_id FROM basic_sta_type WHERE lat LIKE '{}' AND lng LIKE '{}')".format(x + '%', y + '%')
    else:
        sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id IN (SELECT sta_id FROM basic_sta_type WHERE lat like '{}' AND lng LIKE '{}')".format(
            choose_city, x + '%', y + '%')

    print('--sql----', sql)
    result = mysql.query(sql)

    for i in range(len(result)):
        sta_list.append(str(result[i][0]) + '_' + str(result[i][1]))

    resultdict['sta_list'] = sta_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第二版
# 基站展示列表
def sta_list_top10(more='',choose_city=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    print('choose_city: ', choose_city)
    # choose_city = 'all'
    print('--choose_city----', choose_city)
    colour = '红'
    sta_list = []
    if colour == '' or colour == '全部':
        sql = "select sta_num,`type`,mean from xgld_load_abnormal ORDER BY mean desc"
        print('--sql--1--', sql)
    elif colour == '红':
        if choose_city == 'all':
            sql = "select sta_num,`type`,mean from xgld_load_abnormal WHERE (`type` = '基站未工作' or `type` = '负荷过高' or `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常' or `type` = '反季节变化') ORDER BY mean desc"
        else:
            sql = "select sta_num,`type`,mean from xgld_load_abnormal WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND (`type` = '基站未工作' or `type` = '负荷过高' or `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常' or `type` = '反季节变化') ORDER BY mean desc".format(
                choose_city)

        print('--sql--2--', sql)
    elif colour == '黄':
        sql = "select sta_num,`type`,mean from xgld_load_abnormal WHERE `type` = '反季节变化' ORDER BY mean desc"
        print('--sql-3---', sql)
    elif colour == '绿':
        sql = "select sta_num,`type`,mean from xgld_load_abnormal WHERE `type` = '正常' ORDER BY mean desc"
        print('--sql--4--', sql)
    else:
        print('colour err!')

    # 正常： 正常
    # 警告：反季节变化
    # 异常：基站未工作、负荷过高、负荷曲线连续三个月以上基本无变化、跳变异常

    result = mysql.query(sql)
    print('sql:80 ', sql)
    print('result:80 ', result)
    result_sta_num = []
    for i in range(len(result)):
        result_sta_num.append(result[i][0])
    print('result_sta_num:80 ', result_sta_num)
    if len(result) > 0:
        if len(result) == 1:
            sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num='{}'".format(result_sta_num[0][0])
        else:
            sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num in {}".format(tuple(result_sta_num))

        result_1 = mysql.query(sql)
        print('--sql--9--', sql)
        print('--result_1--9--', result_1)
    for i in range(len(result)):
        sta_list.append(list(result[i]))
        if result[i][1] == '正常':
            sta_list[i].append('green')
        elif result[i][1] == '反季节变化':
            sta_list[i].append('yellow')
        elif result[i][1] == '基站未工作' or result[i][1] == '负荷过高' or result[i][1] == '负荷曲线连续三个月以上基本无变化' or result[i][1] == '跳变异常' or result[i][1] == '反季节变化':
            sta_list[i].append('red')
    for i in range(len(sta_list)):
        for j in range(len(result)):
            if sta_list[i][0] == result_1[j][0]:
                sta_list[i][0] = str(result_1[j][0]) + '_' + str(result_1[j][1])

    if more != '1':
        sta_list = sta_list[:10]

    sta_list.insert(0, ['基站', '异常类型', '负荷', '颜色'])
    print('--sta_list--9--', sta_list)

    resultdict['sta_list'] = sta_list
    print('完')
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第一版
# 基站展示列表
def sta_list_top10_old(colour='', x=0, y=0, more=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sta_list = []
    if (x == 0 or x == '') and (y == 0 or y == ''):
        if colour == '' or colour == '全部':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal ORDER BY jump desc"
            print('--sql--1--', sql)
        elif colour == '红':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE (`type` = '基站未工作' or `type` = '负荷过高' or `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常') ORDER BY jump desc"
            print('--sql--2--', sql)
        elif colour == '黄':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE `type` = '反季节变化' ORDER BY jump desc"
            print('--sql-3---', sql)
        elif colour == '绿':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE `type` = '正常' ORDER BY jump desc"
            print('--sql--4--', sql)
        else:
            print('colour err!')

    elif (x != 0 and x != '') or (y != 0 and y != ''):
        if colour == '' or colour == '全部':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE sta_num in (SELECT sta_num FROM basic_sta_list WHERE id IN (SELECT sta_id FROM basic_sta_type WHERE lat='{}' AND lng='{}')) ORDER BY jump desc".format(x, y)
            print('--sql--5--', sql)
        elif colour == '红':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE sta_num in (SELECT sta_num FROM basic_sta_list WHERE id IN (SELECT sta_id FROM basic_sta_type WHERE lat='{}' AND lng='{}')) AND (`type` = '基站未工作' or `type` = '负荷过高' or `type` = '负荷曲线连续三个月以上基本无变化' or `type` = '跳变异常') ORDER BY jump desc".format(x, y)
            print('--sql--6--', sql)
        elif colour == '黄':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE sta_num in (SELECT sta_num FROM basic_sta_list WHERE id IN (SELECT sta_id FROM basic_sta_type WHERE lat='{}' AND lng='{}')) AND `type` = '反季节变化' ORDER BY jump desc".format(x, y)
            print('--sql-7---', sql)
        elif colour == '绿':
            sql = "select sta_num,`type`,jump from xgld_load_abnormal WHERE sta_num in (SELECT sta_num FROM basic_sta_list WHERE id IN (SELECT sta_id FROM basic_sta_type WHERE lat='{}' AND lng='{}')) AND `type` = '正常' ORDER BY jump desc".format(x, y)
            print('--sql--8--', sql)
        else:
            print('colour err!')

    # 正常： 正常
    # 警告：反季节变化
    # 异常：基站未工作、负荷过高、负荷曲线连续三个月以上基本无变化、跳变异常

    result = mysql.query(sql)
    print('sql:80 ', sql)
    print('result:80 ', result)
    result_sta_num = []
    for i in range(len(result)):
        result_sta_num.append(result[i][0])
    print('result_sta_num:80 ', result_sta_num)
    if len(result) > 0:
        if len(result) == 1:
            # sql_type = "select `type`,jump from xgld_load_abnormal WHERE sta_num =(select sta_num FROM basic_sta_list WHERE id='{}')".format(sta_id_list[0])
            sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num='{}'".format(result_sta_num[0][0])
        else:
            # sql_type = "select `type`,jump from xgld_load_abnormal WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in {})".format(tuple(sta_id_list))
            sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num in {}".format(tuple(result_sta_num))

        result_1 = mysql.query(sql)
        print('--sql--9--', sql)
        print('--result_1--9--', result_1)
    for i in range(len(result)):
        # sql = "select sta_num,sta_name from basic_sta_list WHERE sta_num='{}'".format(result[i][0])
        # print('--sql--9--', sql)
        # result_1 = mysql.query(sql)
        sta_list.append(list(result[i]))
        if result[i][1] == '正常':
            sta_list[i].append('green')
        elif result[i][1] == '反季节变化':
            sta_list[i].append('yellow')
        elif result[i][1] == '基站未工作' or result[i][1] == '负荷过高' or result[i][1] == '负荷曲线连续三个月以上基本无变化' or result[i][1] == '跳变异常':
            sta_list[i].append('red')
    for i in range(len(sta_list)):
        for j in range(len(result)):
            if sta_list[i][0] == result_1[j][0]:
                sta_list[i][0] = str(result_1[j][0]) + '_' + str(result_1[j][1])

    if more != '1':
        sta_list = sta_list[:10]

    print('--sta_list--9--', sta_list)
    resultdict['sta_list'] = sta_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 基站展示详情
def sta_details(sta_no='', err_type=''):
    print('comming')
    print('--sta_no--', sta_no)
    print('--err_type--', err_type)
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    date_list = []
    load_list = []
    sta_details = []

    title = ['id', '基站编号', '异常类型', '负荷均值', '低值负荷覆盖率', '跳变次数', '热季负荷', '其他季负荷']
    if sta_no != '' and err_type != '':
        sql = "select met_reader FROM basic_reader_list where sta_no='{}'".format(sta_no.split('_')[-1])
        print('---sql:----', sql)
        result = mysql.query(sql)
        print('---result:----', result)
        name = sta_no + '_' + str(result[0][0])

        sql = "select * FROM xgld_load_abnormal where sta_num='{}'".format(sta_no.split('_')[-1])
        result = mysql.query(sql)
        for i in range(len(result[0])):
            sta_details.append(result[0][i])

        sql = "select `date`,`load` FROM Xgdl_Basic_Load where sta_no='{}' order by `date`".format(sta_no.split('_')[-1])
        result = mysql.query(sql)
        for i in range(len(result)):
            date_list.append(result[i][0])
            load_list.append(result[i][1])
        sql_advice="select `advice` from xgld_load_abnormal where sta_num='{}'".format(sta_no.split('_')[-1])
        print(sql_advice)
        advice=mysql.query(sql_advice)
        print(advice)
        resultdict['date_list'] = date_list
        resultdict['load_list'] = load_list
        resultdict['name'] = name
        resultdict['err_type'] = '建议处理方法：' + advice[0][0]
        resultdict['title'] = title
        resultdict['sta_details'] = sta_details
    else:
        resultdict['date_list'] = []
        resultdict['load_list'] = []
        resultdict['name'] = []
        resultdict['err_type'] = []
        resultdict['title'] = title
        resultdict['sta_details'] = []

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def sta_data_show(sta_name=''):
    print('---sta_name:--', sta_name)
    '''
    基站设备数据展示
    :param sta_name:
    :return:
    '''
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sta_data_list = []
    title = ['id', '设备名称', '数量', '功率']
    if sta_name != '':
        sql = "select id,dev_name,`count`,power FROM xgdl_dev_data where sta_no = '{}' ORDER BY id DESC ".format(sta_name.split('_')[-1])
        print('---sql:--', sql)
        result = mysql.query(sql)
        print('---result:--', result)

        for i in range(len(result)):
            sta_data_list.append(list(result[i]))

        resultdict['title'] = title
        resultdict['sta_data_list'] = sta_data_list
    else:
        resultdict['title'] = title
        resultdict['sta_data_list'] = []

    print('---sta_data_list:--', sta_data_list)

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def dev_data_insert_old(array=''):
    '''
    设备数据插入
    :param array:
    :return:
    '''
    print('--array:--', array)
    array = eval(array)
    print('--array:-1-', array)
    flag = 0
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    #
    # try:
    #     sql = """insert into xgdl_dev_data(sta_no, dev_name,`count`,power)VALUES('{0}','{1}','{2}','{3}')""".format(sta_name.split('_')[0], dev_name, count, power)
    #     print('====sql:==', sql)
    #     mysql.executesql(sql)
    #     mysql.commitdata()
    #     flag = 1
    # except:
    #     flag = 0

    resultdict['flag'] = flag
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def dev_data_insert(sta_name='', dev_name='', count='', power=''):
    print('--sta_name---', sta_name)
    print('--sta_name---', type(sta_name))
    print('--dev_name---', dev_name)
    print('--count---', count)
    print('--power---', power)
    '''
    基站设备数据插入
    :param sta_name:
    :param dev_name:
    :param count:
    :param power:
    :return:
    '''
    sta_name = sta_name
    print('--sta_name---', sta_name)
    dev_name = dev_name.split(',')
    print('--dev_name---', dev_name)
    count = count.split(',')
    print('--count---', count)
    power = power.split(',')
    print('--power---', power)



    flag_1 = 0
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    for i in range(len(dev_name)):
        try:
            sql = """insert into xgdl_dev_data(sta_no, dev_name,`count`,power)VALUES('{0}','{1}','{2}','{3}')""".format(sta_name.split('_')[-1], dev_name[i], count[i], power[i])
            print('====sql:==', sql)
            mysql.executesql(sql)
            mysql.commitdata()
            flag_1 += 1
        except:
            flag_1 += 0

    if flag_1 == len(dev_name):
        flag = 1
    else:
        flag = 0
    resultdict['flag'] = flag
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 设备删除
def del_device(id =''):
    flag = 0
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    try:
        import_record = "DELETE FROM xgdl_dev_data WHERE id= {}".format(id)
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


# 设备编辑
def edit_devices(id='', sta_name='', dev_name='', count='', power=''):
    flag = 0
    flag_1 = 0
    flag_2 = 0
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    try:
        sql = """insert into xgdl_dev_data(sta_no, dev_name,`count`,power)VALUES('{0}','{1}','{2}','{3}')""".format(sta_name.split('_')[0], dev_name, count, power)
        print('====sql:==', sql)
        mysql.executesql(sql)
        mysql.commitdata()
        flag_1 = 1
    except:
        flag_1 = 0

    try:
        import_record = "DELETE FROM xgdl_dev_data WHERE id= {}".format(id)
        mysql.executesql(import_record)
        mysql.commitdata()
        flag_2 = 1
    except:
        flag_2 = 0

    if flag_1 == 1 and flag_2 == 1:
        flag = 1

    resultdict['flag'] = flag
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps