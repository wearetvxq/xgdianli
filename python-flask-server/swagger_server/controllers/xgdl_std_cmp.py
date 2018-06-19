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
#                  稳态对比页面                #
#                                              #
# ##############################################


# 1.对比时间间隔：
def time_lag():
    resultdict = {}

    resultdict['title'] = '时间间隔'
    resultdict['date_list'] = ['月', '周']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 2.基站列表
def get_sta_list(time_lag='', choose_city=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_list = []

    if time_lag == '周':
        table_name = 'orig_static_sta_dl_month'
    elif time_lag == '月':
        table_name = 'orig_static_sta_dl_week'
    else:
        table_name = ''

    if choose_city == 'all':
        # sql = "select sta_num,sta_name FROM basic_sta_list WHERE sta_num in(select sta_id from {} GROUP BY sta_id)".format(table_name)
        sql = "select sta_no,sta_name FROM Xgdl_Basic_Stalist WHERE sta_no in(select sta_id from {} GROUP BY sta_id)".format(table_name)
    else:
        sql = "select sta_no,sta_name FROM Xgdl_Basic_Stalist WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_id from {} GROUP BY sta_id)".format(choose_city, table_name)
    result = mysql.query(sql)

    if len(result) > 0:
        for i in range(len(result)):
            sta_list.append(str(result[i][1]) + '_' + str(result[i][0]))
    else:
        print('没有找到基站编号和名称!')

    print('--sta_list:-0--', sta_list)
    print('--sta_list:-0--', len(sta_list))
    resultdict['title'] = '基站列表'
    resultdict['sta_list'] = sta_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 开始时间和结束时间
def get_time(time_lag='', sta_name=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    date_list = []

    if time_lag == '月':
        table_name = 'orig_static_sta_dl_month'
        row = 'month'
    elif time_lag == '周':
        table_name = 'orig_static_sta_dl_week'
        row = 'week'
    else:
        table_name = ''
        row = ''

    sql = "select {} from {} WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(row,table_name, sta_name.split('_')[1])
    result = mysql.query(sql)
    for i in range(len(result)):
        if len((result[i][0]).split('-')[1]) == 1:
            date_list.append(str(result[i][0].split('-')[0]) + '-0' + str(result[i][0].split('-')[1]))
        else:
            date_list.append(str(result[i][0]))
    minday = min(date_list)
    maxday = max(date_list)


    if time_lag == '月':
        day_min = str(minday) + '-01'
        day_max = str(maxday) + '-28'
    elif time_lag == '周':
        weekday = []
        weekday_all = []
        a = []
        # ------------方案三--------
        # 根据年，找到所有的周；放到列表中
        if minday.split('-')[0] == maxday.split('-')[0]:
            d1 = minday.split('-')[0] + '-01-01'
            d2 = minday.split('-')[0] + '-12-30'
            date1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
            date2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
            delta = date2 - date1

            per_day_seconds = 24 * 60 * 60
            per_week_seconds = 7 * per_day_seconds
            total_seconds = delta.total_seconds()
            weeks = total_seconds // per_week_seconds
            days = total_seconds // per_day_seconds
            if weeks * per_week_seconds < total_seconds:
                weeks += 1

            oneday = datetime.timedelta(days=1)
            WEEK = ["M", "T", "W", "R", "F", "S", "U"]

            d0 = date1
            weekdays = [d0, ]

            enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
            for i in range(int(days)):
                weekday_part = []
                d0 += oneday
                if d0.weekday() == 6:  # For Sunday
                    per_week = []
                    for d in weekdays:
                        per_week.append(d.strftime("%Y-%m-%d"))
                        weekday_all.append(per_week)
                        enday = d.strftime("%Y-%m-%d")
                        enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
                    weekday_all.append(per_week)
                    a.append(per_week)
                    # print('--weekday_all-5--', weekday_all)
                    weekdays = []
                weekdays.append(d0)
            if enday != date2:
                per_week = []
                enday += datetime.timedelta(days=1)
                while enday <= date2:
                    date_str = enday.strftime("%Y-%m-%d")
                    per_week.append(date_str)
                    enday += datetime.timedelta(days=1)
                weekday_all.append(per_week)
                a.append(per_week)
            weekday.append(a)
            day_min = weekday[0][int(minday.split('-')[1])][0]
            day_max = weekday[0][int(maxday.split('-')[1])][0]
        else:
            d1 = minday.split('-')[0] + '-01-01'
            d2 = minday.split('-')[0] + '-12-30'
            d3 = maxday.split('-')[0] + '-01-01'
            d4 = maxday.split('-')[0] + '-12-30'
            data_list = []
            weekday = []
            data_list.append([d1, d2])
            data_list.append([d3, d4])
            for i in range(len(data_list)):
                date1 = datetime.datetime.strptime(data_list[i][0], "%Y-%m-%d")
                date2 = datetime.datetime.strptime(data_list[i][1], "%Y-%m-%d")
                delta = date2 - date1

                per_day_seconds = 24 * 60 * 60
                per_week_seconds = 7 * per_day_seconds
                total_seconds = delta.total_seconds()
                weeks = total_seconds // per_week_seconds
                days = total_seconds // per_day_seconds
                if weeks * per_week_seconds < total_seconds:
                    weeks += 1

                oneday = datetime.timedelta(days=1)
                WEEK = ["M", "T", "W", "R", "F", "S", "U"]

                d0 = date1
                weekdays = [d0, ]

                enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
                for i in range(int(days)):
                    weekday_part = []
                    d0 += oneday
                    if d0.weekday() == 6:  # For Sunday
                        per_week = []
                        for d in weekdays:
                            per_week.append(d.strftime("%Y-%m-%d"))
                            weekday_all.append(per_week)
                            enday = d.strftime("%Y-%m-%d")
                            enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
                        weekday_all.append(per_week)
                        a.append(per_week)
                        # print('--weekday_all-5--', weekday_all)
                        weekdays = []
                    weekdays.append(d0)
                if enday != date2:
                    per_week = []
                    enday += datetime.timedelta(days=1)
                    while enday <= date2:
                        date_str = enday.strftime("%Y-%m-%d")
                        per_week.append(date_str)
                        enday += datetime.timedelta(days=1)
                    weekday_all.append(per_week)
                    a.append(per_week)
                weekday.append(a)
                a = []

            day_min = weekday[0][int(minday.split('-')[1])][0]
            day_max = weekday[1][int(maxday.split('-')[1])][0]




        # ----方案二--------
        # start_year = minday.split('-')[0]
        # if len(str(int(int(minday.split('-')[1]) / 4) + 1)) == 1:
        #     start_month = '0' + str(int(int(minday.split('-')[1]) / 4) + 1)
        # else:
        #     start_month = str(int(int(minday.split('-')[1]) / 4) + 1)
        # if len(str(int(int(minday.split('-')[1]) % 4) * 7)) == 1:
        #     start_day = '0' + str(int(int(minday.split('-')[1]) % 4) * 7)
        # else:
        #     start_day = str(int(int(minday.split('-')[1]) % 4) * 7)
        #
        # end_year = maxday.split('-')[0]
        # if len(str(int(int(maxday.split('-')[1]) / 4) + 1)) == 1:
        #     end_month = '0' + str(int(int(maxday.split('-')[1]) / 4) + 1)
        # else:
        #     end_month = str(int(int(maxday.split('-')[1]) / 4) +1)
        # if len(str(int(int(maxday.split('-')[1]) % 4) * 7)) == 1:
        #     end_day = '0' + str(int(int(maxday.split('-')[1]) % 4) * 7)
        # else:
        #     end_day = str(int(int(maxday.split('-')[1]) % 4) * 7)
        #
        # minday = start_year + '-' + start_month + '-' + start_day
        # maxday = end_year + '-' + end_month + '-' + end_day
        # ------------------
        # year_start = str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_year)
        # if len(str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mon)) == 1:
        #     month_start = '0' + str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mon)
        # else:
        #     month_start = str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mon)
        # print('--222----', len(str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mon)))
        # if len(str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mday)) == 1:
        #     day_start = '0' + str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mday)
        # else:
        #     day_start = str(time.strptime(str(minday) + '-0', '%Y-%U-%w').tm_mday)
        #
        # year_emd = str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_year)
        # if len(str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mon)) == 1:
        #     month_end = '0' + str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mon)
        # else:
        #     month_end = str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mon)
        # if len(str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mday)) == 1:
        #     day_end = '0' + str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mday)
        # else:
        #     day_end = str(time.strptime(str(maxday) + '-0', '%Y-%U-%w').tm_mday)
        #
        #
        # minday = year_start + '-' + month_start + '-' + day_start
        # maxday = year_emd + '-' + month_end + '-' + day_end
    else:
        day_min = ''
        day_max = ''

    resultdict['minday'] = day_min
    resultdict['maxday'] = day_max

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 获取时间列表
def get_time_list(time_lag='',sta_name=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    date_list = []

    if time_lag == '月':
        # sql = "select `month` FROM orig_static_sta_dl_month WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(sta_name.split('_')[1])
        sql = "select `month` FROM orig_static_sta_dl_month WHERE sta_id='{}'".format(sta_name.split('_')[1])
        result = mysql.query(sql)

    elif time_lag == '周':
        # sql = "select week FROM orig_static_sta_dl_week WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(sta_name.split('_')[1])
        sql = "select `week` FROM orig_static_sta_dl_week WHERE sta_id='{}'".format(sta_name.split('_')[1])
        result = mysql.query(sql)
    else:
        print('time_lag err!')
    for i in range(len(result)):
        if len(result[i][0].split('-')[1]) == 1:
            date_list.append(result[i][0].split('-')[0] + '-0' + result[i][0].split('-')[1])
        else:
            date_list.append(result[i][0])
    date_list.sort()
    resultdict['date_list'] = date_list
    resultdict['title'] = '时间列表'
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第二版----稳态图表
def get_sta_chart(time_lag='', sta_name='', get_time=''):
    get_time_1 = get_time
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    if time_lag == '月':
        print('get_time: ', get_time)
        # if get_time.split('-')[1][0] == '0':
        #     get_time = get_time.split('-')[0] + '-' + get_time.split('-')[1][1] + '%'
        if get_time_1.split('-')[1][0] == '0':
            get_time_1 = get_time_1.split('-')[0] + '-' + get_time_1.split('-')[1][1]
        # if len(get_time) == 6:
        #     get_time = get_time.split('-')[0] + '-0' + get_time.split('-')[1] + '%'

        print('get_time: ', get_time)
        print('get_time_1: ', get_time_1)
        # sql = "select total_power,`date` FROM source_elec_info WHERE user_id in (select met_num from basic_met_list WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')) AND `date` BETWEEN '{}' AND '{}'".format(
        #     sta_name.split('_')[1], s_date, e_date)

        # sql = "select total_power,`date` FROM source_elec_info WHERE user_id in (select met_num from basic_met_list WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')) AND `date` LIKE '{}'".format(sta_name.split('_')[1],get_time)
        sql = "select `load`,`date` FROM Xgdl_Basic_Load WHERE sta_no='{}' AND `date` LIKE '{}'".format(sta_name.split('_')[1],get_time+'%')
        result = mysql.query(sql)
        print('-sql--', sql)
        print('-result--', result)

        sql_1 = "select osc,steady FROM orig_static_sta_dl_month WHERE sta_id ='{}' and `month`='{}'".format(sta_name.split('_')[1], get_time_1)
        # sql_1 = "select osc,steady FROM orig_static_sta_dl_month WHERE sta_id =(SELECT id FROM basic_sta_list WHERE sta_num='{}') and `month`='{}'".format(sta_name.split('_')[1], get_time)
        print('-sql_1--', sql_1)
        result_1 = mysql.query(sql_1)
    elif time_lag == '周':
        if get_time.split('-')[1][0] == '0':
            get_time = get_time.split('-')[0] + '-' + get_time.split('-')[1][1]
        # 算出这周的具体日期
        d1 = get_time.split('-')[0] + '-01-01'
        d2 = get_time.split('-')[0] + '-12-30'
        d3 = get_time.split('-')[0] + '-01-01'
        d4 = get_time.split('-')[0] + '-12-30'
        data_list = []
        weekday = []
        weekday_all = []
        a = []
        data_list.append([d1, d2])
        data_list.append([d3, d4])
        for i in range(len(data_list)):
            date1 = datetime.datetime.strptime(data_list[i][0], "%Y-%m-%d")
            date2 = datetime.datetime.strptime(data_list[i][1], "%Y-%m-%d")
            delta = date2 - date1

            per_day_seconds = 24 * 60 * 60
            per_week_seconds = 7 * per_day_seconds
            total_seconds = delta.total_seconds()
            weeks = total_seconds // per_week_seconds
            days = total_seconds // per_day_seconds
            if weeks * per_week_seconds < total_seconds:
                weeks += 1

            oneday = datetime.timedelta(days=1)
            WEEK = ["M", "T", "W", "R", "F", "S", "U"]

            d0 = date1
            weekdays = [d0, ]

            enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
            for i in range(int(days)):
                weekday_part = []
                d0 += oneday
                if d0.weekday() == 6:  # For Sunday
                    per_week = []
                    for d in weekdays:
                        per_week.append(d.strftime("%Y-%m-%d"))
                        weekday_all.append(per_week)
                        enday = d.strftime("%Y-%m-%d")
                        enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
                    weekday_all.append(per_week)
                    a.append(per_week)
                    # print('--weekday_all-5--', weekday_all)
                    weekdays = []
                weekdays.append(d0)
            if enday != date2:
                per_week = []
                enday += datetime.timedelta(days=1)
                while enday <= date2:
                    date_str = enday.strftime("%Y-%m-%d")
                    per_week.append(date_str)
                    enday += datetime.timedelta(days=1)
                weekday_all.append(per_week)
                a.append(per_week)
            weekday.append(a)
            a = []

        s_date = weekday[0][int(get_time.split('-')[1]) - 1][0]
        e_date = weekday[0][int(get_time.split('-')[1]) - 1][-1]


        # sql = "select total_power,`date` FROM source_elec_info WHERE user_id in (select met_num from basic_met_list WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')) AND `date` BETWEEN '{}' AND '{}'".format(sta_name.split('_')[1], s_date, e_date)
        sql = "select `load`,`date` FROM Xgdl_Basic_Load WHERE sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(sta_name.split('_')[1], s_date, e_date)
        result = mysql.query(sql)

        sql_1 = "select osc,steady FROM orig_static_sta_dl_week WHERE sta_id ='{}' and week='{}'".format(sta_name.split('_')[1], get_time)
        result_1 = mysql.query(sql_1)
        print('--1--sql_1', sql_1)
        print('--1--result_1', result_1)
    else:
        print('--time_lag err!--')

    chart_x = []
    chart_y = []
    for i in range(len(result)):
        chart_x.append(result[i][1])
        chart_y.append(result[i][0])

    resultdict['chart_x'] = chart_x
    resultdict['chart_y'] = chart_y

    if len(result_1) > 0:
        if result_1[0][0] == 'Y':
            chart_err = '波动异常：负荷波动过大'
        elif result_1[0][1] == 'Y':
            chart_err = '平稳异常：负荷波动过小'
        else:
            chart_err = '正常'
    else:
        print('--result_1 err!--')
        chart_err = ''

    resultdict['chart_err'] = chart_err

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps



# 稳态图表
# 周月、基站、时间
def std_chart(time_lag='', sta_name='', StartDate='', EndDate=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    chart_x = []
    chart_y = []
    chart_err = []

    # 1. 根据开始时间结束时间找到周月
    if time_lag == '月':
        # 1. 找到所有的月
        month_1 = []
        all_month = com.get_month_list(StartDate, EndDate)
        for i in range(len(all_month)):
            if all_month[i].split('-')[1][:1] == '0':
                all_month[i] = all_month[i].split('-')[0] + '-' + all_month[i].split('-')[1][1:]
        sql_base = "select `month` FROM orig_static_sta_dl_month WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(sta_name.split('_')[1])
        result_base = mysql.query(sql_base)
        for i in range(len(result_base)):
            if result_base[i][0] in all_month:
                month_1.append(result_base[i][0])
        if len(month_1) > 0:
            if len(month_1) ==1:
                sql = "select `month`,mean,osc FROM orig_static_sta_dl_month WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}') AND `month` ='{}'".format(
                    sta_name.split('_')[1], month_1[0])
            else:
                sql = "select `month`,mean,osc FROM orig_static_sta_dl_month WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}') AND `month` in {}".format(
                    sta_name.split('_')[1], tuple(month_1))
        else:
            print('没有找到对应的月!')
        result = mysql.query(sql)

        for i in range(len(result)):
            chart_x.append(result[i][0])
            chart_y.append(result[i][1])

        for i in range(len(result)):
            chart_err_single = []
            if result[i][2] == 'Y':
                chart_err_single.append('波动异常')
            elif result[i][2] == 'N':
                chart_err_single.append('稳态异常')
            else:
                chart_err_single.append('')
            chart_err_single.append(result[i][0])
            chart_err.append(chart_err_single)

    elif time_lag == '周':
        # -----------方案三--------

        d1 = StartDate.split('-')[0] + '-01-01'
        d2 = StartDate.split('-')[0] + '-12-30'
        d3 = EndDate.split('-')[0] + '-01-01'
        d4 = EndDate.split('-')[0] + '-12-30'
        data_list = []
        weekday = []
        weekday_all = []
        a = []
        data_list.append([d1, d2])
        data_list.append([d3, d4])
        for i in range(len(data_list)):
            date1 = datetime.datetime.strptime(data_list[i][0], "%Y-%m-%d")
            date2 = datetime.datetime.strptime(data_list[i][1], "%Y-%m-%d")
            delta = date2 - date1

            per_day_seconds = 24 * 60 * 60
            per_week_seconds = 7 * per_day_seconds
            total_seconds = delta.total_seconds()
            weeks = total_seconds // per_week_seconds
            days = total_seconds // per_day_seconds
            if weeks * per_week_seconds < total_seconds:
                weeks += 1

            oneday = datetime.timedelta(days=1)
            WEEK = ["M", "T", "W", "R", "F", "S", "U"]

            d0 = date1
            weekdays = [d0, ]

            enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
            for i in range(int(days)):
                weekday_part = []
                d0 += oneday
                if d0.weekday() == 6:  # For Sunday
                    per_week = []
                    for d in weekdays:
                        per_week.append(d.strftime("%Y-%m-%d"))
                        weekday_all.append(per_week)
                        enday = d.strftime("%Y-%m-%d")
                        enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
                    weekday_all.append(per_week)
                    print('--per_week-5--', per_week)
                    a.append(per_week)
                    # print('--weekday_all-5--', weekday_all)
                    weekdays = []
                weekdays.append(d0)
            if enday != date2:
                per_week = []
                enday += datetime.timedelta(days=1)
                while enday <= date2:
                    date_str = enday.strftime("%Y-%m-%d")
                    per_week.append(date_str)
                    enday += datetime.timedelta(days=1)
                weekday_all.append(per_week)
                a.append(per_week)
            weekday.append(a)
            a = []
        for i in range(len(weekday[0])):
            if StartDate in weekday[0][i]:
                if len(str(i)) == 1:
                    start_week = StartDate.split('-')[0] + '-0' + str(i)
                else:
                    start_week = StartDate.split('-')[0] + '-' + str(i)
        for i in range(len(weekday[1])):
            if EndDate in weekday[1][i]:
                if len(str(i)) == 1:
                    end_week = EndDate.split('-')[0] + '-0' + str(i)
                else:
                    end_week = EndDate.split('-')[0] + '-' + str(i)

        # # ----------方案二---------------
        # if len(str((int(StartDate.split('-')[1]) - 1) * 4 + int(int(StartDate.split('-')[2]) / 7))) == 1:
        #     if int(StartDate.split('-')[2]) % 7 != 0:
        #         start_week = StartDate.split('-')[0] + '-0' + str((int(StartDate.split('-')[1])-1)*4 + int(int(StartDate.split('-')[2]) / 7) + 1)
        #     else:
        #         start_week = StartDate.split('-')[0] + '-0' + str((int(StartDate.split('-')[1])-1)*4 + int(StartDate.split('-')[2]) / 7)
        # else:
        #     start_week = StartDate.split('-')[0] + '-' + str((int(StartDate.split('-')[1])-1)*4 + int(StartDate.split('-')[2]) / 7)
        #
        # if len(str((int(EndDate.split('-')[1]) - 1) * 4 + int(int(EndDate.split('-')[2]) / 7))) == 1:
        #     if int(EndDate.split('-')[2]) % 7 != 0:
        #         end_week = EndDate.split('-')[0] + '-0' + str((int(EndDate.split('-')[1])-1)*4 + int(EndDate.split('-')[2]) / 7 +1)
        #     else:
        #         end_week = EndDate.split('-')[0] + '-0' + str((int(EndDate.split('-')[1])-1)*4 + int(EndDate.split('-')[2]) / 7)
        # else:
        #     end_week = EndDate.split('-')[0] + '-' + str((int(EndDate.split('-')[1])-1)*4 + int(EndDate.split('-')[2]) / 7)

        # 2. 在数据库中找到该基站所有的周，并作出处理
        sql_week_list = []
        week_list = []
        sql = "select week FROM orig_static_sta_dl_week WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(sta_name.split('_')[1])
        result = mysql.query(sql)
        for i in range(len(result)):
            if len(result[i][0]) == 6:
                sql_week_list.append(str(result[i][0]).split('-')[0] + '-0' + str(result[i][0]).split('-')[1])
            else:
                sql_week_list.append(str(result[i][0]))
        for i in range(len(sql_week_list)):
            if sql_week_list[i] >= start_week and sql_week_list[i] <= end_week:
                if (sql_week_list[i].split('-')[1])[:1] == '0':
                    week_list.append(sql_week_list[i].split('-')[0] + '-' + (sql_week_list[i].split('-')[1])[1:])
                else:
                    week_list.append(sql_week_list[i])

        if len(week_list) > 0:
            if len(week_list) ==1:
                sql_1 = "select week,mean,osc FROM orig_static_sta_dl_week WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}') AND week ='{}'".format(
                    sta_name.split('_')[1], week_list[0])
            else:
                sql_1 = "select week,mean,osc FROM orig_static_sta_dl_week WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}') AND week in {}".format(
                    sta_name.split('_')[1], tuple(week_list))
        result_1 = mysql.query(sql_1)
        re = []
        for i in range(len(result_1)):
            if len(result_1[i][0]) == 6:
                re.append([result_1[i][0].split('-')[0] + '-0' + result_1[i][0].split('-')[1], result_1[i][1]])
            else:
                re.append([result_1[i][0], result_1[i][1]])
        re.sort(key=lambda x: x[0])
        for i in range(len(re)):
            chart_x.append(re[i][0])
            chart_y.append(re[i][1])

        for i in range(len(result_1)):
            chart_err_single = []
            if result_1[i][2] == 'Y':
                chart_err_single.append('波动异常')
            elif result_1[i][2] == 'N':
                chart_err_single.append('稳态异常')
            else:
                chart_err_single.append('')
            chart_err_single.append(chart_x[i])
            chart_err.append(chart_err_single)

    else:
        print('time_lag err!')

    resultdict['chart_x'] = chart_x
    resultdict['chart_y'] = chart_y
    resultdict['chart_err'] = chart_err


    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 基站编号--》基站id--》电表编号--》时间和电量

# 1. 找出淡季、旺季对比
def get_month_cmp(sta_name=''):
    # 1.规定淡季为1--》6月
    # 2.规定旺季为7--》12月
    low_session = ['%-01-%', '%-02-%', '%-03-%', '%-04-%', '%-05-%', '%-06-%']
    high_session = ['%-07-%', '%-08-%', '%-09-%', '%-10-%', '%-11-%', '%-12-%']


    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sql = "select avg(`load`) FROM Xgdl_Basic_Load WHERE ( `date` LIKE '%-01-%' OR `date` LIKE '%-02-%' OR `date` LIKE '%-03-%' OR `date` LIKE '%-04-%' OR `date` LIKE '%-05-%' OR `date` LIKE '%-06-%') AND  sta_no='{}'".format(sta_name.split('_')[1])
    result = mysql.query(sql)
    if len(result) > 0:
        low_avg = result[0][0]
    else:
        low_avg = 0

    sql = "select avg(`load`) FROM Xgdl_Basic_Load WHERE ( `date` LIKE '%-07-%' OR `date` LIKE '%-08-%' OR `date` LIKE '%-09-%' OR `date` LIKE '%-10-%' OR `date` LIKE '%-11-%' OR `date` LIKE '%-12-%') AND  sta_no='{}'".format(
        sta_name.split('_')[1])
    result = mysql.query(sql)
    if len(result) > 0:
        high_avg = result[0][0]
    else:
        high_avg = 0

    resultdict['low_avg'] = str(float('%.2f' % float(low_avg)))
    resultdict['high_avg'] = str(float('%.2f' % float(high_avg)))
    # resultdict['low_avg'] = str(99)
    # resultdict['high_avg'] = str(150)
    resultdict['title'] = '淡季/旺季负荷比'
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 2. 找到平时、节假日对比
def get_weekend_cmp(sta_name=''):
    # 1.找到开始时间和结束时间
    # 2.依据开始时间和结束时间找到所有节假日
    # 3.找出节假日平均值、和 平时平均值
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    # sql = "select min(`date`) as minday,max(`date`) as maxday FROM source_elec_info WHERE  user_id in (select met_num from basic_met_list WHERE sta_id=(SELECT id FROM basic_sta_list WHERE sta_num='{}'))".format(
    sql = "select min(`date`) as minday,max(`date`) as maxday FROM Xgdl_Basic_Load WHERE sta_no='{}'".format(
        sta_name.split('_')[1])
    result = mysql.query(sql)

    d1 = str(result[0][0])
    d2 = str(result[0][1])

    date1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    delta = date2 - date1

    per_day_seconds = 24 * 60 * 60
    per_week_seconds = 7 * per_day_seconds
    total_seconds = delta.total_seconds()
    weeks = total_seconds // per_week_seconds
    days = total_seconds // per_day_seconds
    if weeks * per_week_seconds < total_seconds:
        weeks += 1

    oneday = datetime.timedelta(days=1)
    WEEK = ["M", "T", "W", "R", "F", "S", "U"]

    d0 = date1
    weekdays = [d0, ]
    weekday_all = []
    weekday_all_new = []
    enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
    for i in range(int(days)):
        weekday_part = []
        d0 += oneday
        if d0.weekday() == 6:  # For Sunday
            per_week = []
            for d in weekdays:
                per_week.append(d.strftime("%Y-%m-%d"))
                weekday_all.append(per_week)
                enday = d.strftime("%Y-%m-%d")
                enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
            weekdays = []
        weekdays.append(d0)
    if enday != date2:
        per_week = []
        enday += datetime.timedelta(days=1)
        while enday <= date2:
            date_str = enday.strftime("%Y-%m-%d")
            per_week.append(date_str)
            enday += datetime.timedelta(days=1)
        weekday_all.append(per_week)
    if len(weekday_all) > 0:
        for i in range(len(weekday_all)):
            for j in range(len(weekday_all[i])):
                data_list = [int(i) for i in (weekday_all[i][j].split('-'))]
                # print('--0_6---', datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime("%w"))
                # print('--0_6---', type(datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime("%w")))
                if datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime("%w") == '0' or datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime(
                        "%w") == '6':
                    weekday_all_new.append(weekday_all[i][j])

    # 找到节假日的平均值

    if len(weekday_all_new) > 0:
        if len(weekday_all_new) == 1:
            sql = "select avg(`laod`) FROM Xgdl_Basic_Load WHERE `date` = '{}' AND sta_no='{}'".format(
                weekday_all_new[0], sta_name.split('_')[1])
            sql_1 = "select avg(`load`) FROM Xgdl_Basic_Load WHERE `date` != '{}' AND sta_no='{}'".format(
                weekday_all_new[0], sta_name.split('_')[1])
        else:
            sql = "select avg(`load`) FROM Xgdl_Basic_Load WHERE `date` in {} AND sta_no='{}'".format(
                tuple(weekday_all_new), sta_name.split('_')[1])
            sql_1 = "select avg(`load`) FROM Xgdl_Basic_Load WHERE `date` NOT in {} AND sta_no='{}'".format(
                tuple(weekday_all_new), sta_name.split('_')[1])
    else:
        print('--节假日列表为空!-')
    result = mysql.query(sql)
    result_1 = mysql.query(sql_1)
    if len(result) > 0:
        weekday_avg = result[0][0]
    else:
        weekday_avg = 0
    if len(result_1) > 0:
        not_weekday_avg = result_1[0][0]
    else:
        not_weekday_avg = 0

    resultdict['weekday_avg'] = str(float('%.2f' % float(weekday_avg)))
    resultdict['not_weekday_avg'] = str(float('%.2f' % float(not_weekday_avg)))
    # resultdict['weekday_avg'] = str(110)
    # resultdict['not_weekday_avg'] = str(70)
    resultdict['title'] = '平时/周末负荷比'

    # mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 6. 峰/谷平均负荷比
def get_high_low_cmp(sta_name=''):
    # 1.找到开始时间和结束时间
    # 2.依据开始时间和结束时间找到所有节假日
    # 3.找出节假日平均值、和 平时平均值
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    sql = "select AVG(peak_power),AVG(flat_charge) FROM source_elec_info WHERE  user_id in (select met_num from basic_met_list WHERE sta_id=(SELECT id FROM basic_sta_list WHERE sta_num='{}'))".format(
        sta_name.split('_')[1])
    result = mysql.query(sql)

    if len(result) > 0:
        low_cmp = result[0][0]
        high_cmp = result[0][1]
    else:
        low_cmp = 0
        high_cmp = 0
        print('---没有找到峰谷平均值')

    # resultdict['low_cmp'] = str(float('%.2f' % float(low_cmp)))
    # resultdict['high_cmp'] = str(float('%.2f' % float(high_cmp)))
    resultdict['low_cmp'] = str(54)
    resultdict['high_cmp'] = str(88)
    resultdict['title'] = '峰/谷平均负荷比'

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
