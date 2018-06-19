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


# ##############################################
#                                              #
#                  能耗稽核页面                #
#                                              #
# ##############################################


# 接口目录：###################################


################################################

# 一、自留和三方：
# 二、纵向稽核、横向稽核
# 三、纵向稽核：
#     1.同站稽核
#         ①、时
#         ②、日
#         ③、周
#         ④、月
#         ⑤、节假日
#     2.同站稳态稽核
#         ①、暂时没做
# 四、横向稽核：
#     1.同类站稽核：
#         依据数据表中的字段对数据进行分类展示
#         ①、费用核算类型
#         ②、其他
#     2.聚类站稽核：
#         ①、按照学校、小区、商业....进行分类展示
#     3.直供站参考：
#         ①、暂时没做


# 1、稽核拆分
def ways_audit(energy_way=''):
    resultdict = {}
    if energy_way == '纵向稽核':
        resultdict['title'] = '纵向稽核方式'
        resultdict['ways_audit'] = ['同站稽核', '同站稳态稽核']
    elif energy_way == '横向稽核':
        resultdict['title'] = '横向稽核方式'
        resultdict['ways_audit'] = ['同类站稽核', '聚类站稽核', '直供站参考']
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.0 预测颗粒度
def ammeter_and_station_1():
    resultdict = {}
    resultdict['title'] = '稽核颗粒度'
    resultdict['ammeter_and_station'] = ['基站', '电表']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.1 获取所有基站列表：
def get_station_list(veidoo='',ways_audit=''):
    resultdict = {}
    station_list = []
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict['title'] = '基站列表'
    if ways_audit == '同站稽核':
        if veidoo == '三方':
            table_name = 'orig_sta_dl'
        elif veidoo == '自留':
            table_name = 'orig_sta_yd'
        else:
            table_name = ''
        # sql = "select sta_id from {} GROUP BY sta_id".format(table_name)
        sql = "select sta_name,sta_num FROM basic_sta_list WHERE id in(select sta_id from {} GROUP BY sta_id)".format(table_name)
        result = mysql.query(sql)
        if len(result) > 0:
            for i in range(len(result)):
                station_list.append(str(result[i][0]) + '_' + str(result[i][1]))
        else:
            print('费用核算类型err!')
    else:
        print('ways_audit err!')

    resultdict['station_list'] = station_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 2、不同稽核方式的子方式
def ways_audit_child(ways_audit=''):
    resultdict = {}
    if ways_audit == '同站稽核':
        resultdict['title'] = '时段'
        resultdict['ways_audit_child'] = ['日', '节假日',  '周', '月']
    elif ways_audit == '同站稳态稽核':
        resultdict['title'] = '稳态稽核方式'
        resultdict['ways_audit_child'] = ['稳态异常', '波动异常']
    elif ways_audit == '同类站稽核':
        resultdict['title'] = '同类站稽查方式'
        resultdict['ways_audit_child'] = ['费用核算类型', '基站设备', '是否移交铁塔', '县市']
    elif ways_audit == '聚类站稽核':
        resultdict['title'] = '聚类站稽核方式'
        resultdict['ways_audit_child'] = ['公司企业', '住宿区','交通相关区','政府机构及社会团体','科教区','金融机构','餐饮店','医疗院','风景区','购物市场']
    elif ways_audit == '直供站参考':
        resultdict['title'] = '待定3'
        resultdict['ways_audit_child'] = ['待定4', '待定5']
    else:
        resultdict['title'] = ''
        resultdict['ways_audit_child'] = []
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 根据基站获取开始时间和结束时间
def get_sta_end_time(veidoo='', station_name=''):
    resultdict = {}
    station_list = []
    mysql = MySQL(2)
    mysql.mysql_connect()

    station_name = str(station_name).split('_')[1]
    if veidoo == '三方':
        table_name = 'orig_sta_dl'
    elif veidoo == '自留':
        table_name = 'orig_sta_yd'
    else:
        table_name = ''

    sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}')".format(table_name, station_name)
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


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    return dt.replace(year=int(year), month=month)

# 3、图表数据
def get_data_energy_audit(veidoo='',station_name='',energy_way='',ways_audit='',ways_audit_child='',StartDate='',EndDate='',PageIndex=1):
    # veidoo:维度
    # station_name：基站名称
    # ammeter_and_station：电表或基站
    # energy_way：纵向、横向 稽核
    # ways_audit：同站稽核、同站稳态稽核
    # ways_audit_child：日、周、月
    resultdict = {}
    result_list = []
    mysql = MySQL(2)
    mysql.mysql_connect()

    if veidoo == '三方':
        # if ammeter_and_station == '基站':
        #     table_name = 'orig_sta_dl'
        # elif ammeter_and_station == '电表':
        #     table_name = 'orig_met_dl'
        # else:
        #     print('--ammeter_and_station err!---')
        table_name = 'orig_sta_dl'
        table_name_steady = 'orig_static_sta_dl'
    elif veidoo == '自留':
        # if ammeter_and_station == '基站':
        #     table_name = 'orig_sta_yd'
        # elif ammeter_and_station == '电表':
        #     table_name = 'orig_met_yd'
        # else:
        #     print('--ammeter_and_station err!---')
        table_name = 'orig_sta_yd'
        table_name_steady = 'orig_static_sta_yd'
    else:
        print('--veidoo err!---')

    if energy_way == '纵向稽核':
        if ways_audit == '同站稽核':
            station_name = station_name.split('_')[1]
            if ways_audit_child == '节假日':
                d1 = StartDate
                d2 = EndDate

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
                            if datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime("%w") == '0' or datetime.datetime(data_list[0], data_list[1], data_list[2]).strftime("%w") == '6':
                                weekday_all_new.append(weekday_all[i][j])

                sql = "select `date`,total_power FROM {} WHERE sta_id =(select id from basic_sta_list WHERE sta_num='{}')".format(table_name, station_name)
                sql += " and `date` in {}".format(tuple(weekday_all_new))
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('费用核算类型err!')

            elif ways_audit_child == '日':
                sql = "select `date`,total_power FROM {} WHERE sta_id =(select id from basic_sta_list WHERE sta_num='{}')".format(table_name,station_name)
                sql += " and `date` BETWEEN '" + StartDate + "' and '" + EndDate + "'"
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('费用核算类型err!')
            elif ways_audit_child == '周':
                d1 = StartDate
                d2 = EndDate

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
                        week_pre_list = []
                        week_name = str(weekday_all[i][0]) + '~~' + str(weekday_all[i][-1])
                        week_pre_list.append(week_name)
                        predict_value = 0
                        sql = "SELECT total_power FROM {} where 1=1 ".format(table_name)
                        sql += " and `date` BETWEEN '" + str(weekday_all[i][0]) + "' and '" + str(weekday_all[i][-1]) + "'"
                        result = mysql.query(sql)
                        # 2.算出平均值
                        if len(result) != 0:
                            for i in range(len(result)):
                                predict_value += result[i][0]
                            predict_value_time_avg = predict_value / len(result)
                        else:
                            predict_value_time_avg = 0
                        week_pre_list.append(predict_value_time_avg)
                        result_list.append(week_pre_list)
                else:
                    print('---per_week--err-')
            elif ways_audit_child == '月':
                begin_date = StartDate[:7]
                end_date = EndDate[:7]
                date_list = []
                begin_date = datetime.datetime.strptime(begin_date, "%Y-%m")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m")
                while begin_date <= end_date:
                    date_str = begin_date.strftime("%Y-%m")
                    date_list.append(date_str)
                    begin_date = add_months(begin_date, 1)

                # 查询月数据平均值放到类表中
                for i in range(len(date_list)):
                    day_pre_list = []
                    day_pre_list.append(date_list[i])
                    predict_value = 0
                    sql = "SELECT total_power FROM {} where sta_id=(select id from basic_sta_list WHERE sta_num='{}') ".format(table_name,station_name)
                    sql += " and `date` like '{}'".format(str(day_pre_list[0])+'%')
                    result = mysql.query(sql)
                    # 2.算出平均值
                    if len(result) != 0:
                        for i in range(len(result)):
                            avg_test = result[i][0]
                            predict_value += avg_test
                        predict_value_time_avg = predict_value / len(result)
                    else:
                        predict_value_time_avg = 0
                    day_pre_list.append(predict_value_time_avg)
                    result_list.append(day_pre_list)
            else:
                print('--ways_audit 同站稽核err---')
        elif ways_audit == '同站稳态稽核':
            if ways_audit_child == '稳态异常':
                station_id_list= []
                resultdict['title'] = ['基站名称', '方差', '平均值', '最大值', '最小值', '积分', '稳态异常']
                sql = "select sta_id,variance,mean,`max`,`min`,zscore,steady from {} WHERE steady='Y' ".format(table_name_steady)
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        station_id_list.append(result[i][0])
                        result_list.append(list(result[i]))
                else:
                    print('费用核算类型err!')
                sql_1 = "select sta_name from basic_sta_list WHERE id in {} ".format(tuple(station_id_list))
                result_1 = mysql.query(sql_1)
                for i in range(len(result_list)):
                    result_list[i][1] = result_1[i][0]

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

            elif ways_audit_child == '波动异常':
                station_id_list = []
                resultdict['title'] = ['基站名称', '方差', '平均值', '最大值', '最小值', '积分', '波动异常']
                sql = "select sta_id,variance,mean,`max`,`min`,zscore,osc from {} WHERE osc='Y' ".format(
                    table_name_steady)
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        station_id_list.append(result[i][0])
                        result_list.append(list(result[i]))
                else:
                    print('费用核算类型err!')
                sql_1 = "select sta_name from basic_sta_list WHERE id in {} ".format(tuple(station_id_list))
                result_1 = mysql.query(sql_1)
                for i in range(len(result_list)):
                    result_list[i][1] = result_1[i][0]

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

            else:
                print('--ways_audit 同站稳态稽核err---')
        else:
            print('--energy_way 纵向稽核err--')
    elif energy_way == '横向稽核':
        if ways_audit == '同类站稽核':
            if ways_audit_child == '费用核算类型':
                resultdict['title'] = '费用核算类型'
                sql = "select acco_type,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY acco_type"
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('费用核算类型err!')
            elif ways_audit_child == '基站设备':
                resultdict['title'] = '基站设备'
                sql = "select sta_deta,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY sta_deta"
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('基站设备err!')
            elif ways_audit_child == '是否移交铁塔':
                resultdict['title'] = '是否移交铁塔'
                sql = "select move_tower,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY move_tower"
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('基站设备err!')
            elif ways_audit_child == '县市':
                resultdict['title'] = '县市'
                sql = "select cou_city,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY cou_city"
                result = mysql.query(sql)
                if len(result) > 0:
                    for i in range(len(result)):
                        result_list.append(list(result[i]))
                else:
                    print('基站设备err!')
            else:
                print('--ways_audit 同类站稽核err---')
        elif ways_audit == '聚类站稽核':
            if ways_audit_child == '交通相关区':
                # 交通、交通设施、摩托车
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%'))"
            elif ways_audit_child == '住宿区':
                # 住宿、商务住宅
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%'))"
            elif ways_audit_child == '公司企业':
                # 公司
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%'))"
            elif ways_audit_child == '政府机构及社会团体':
                # 政府机构
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%'))"
            elif ways_audit_child == '科教区':
                # 科教、体育、公共设施
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%'))"
                print('-sql--', sql)
            elif ways_audit_child == '金融机构':
                # 金融
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%'))"
            elif ways_audit_child == '餐饮店':
                # 餐饮
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%'))"
            elif ways_audit_child == '医疗院':
                # 医疗
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%'))"
            elif ways_audit_child == '风景区':
                # 地名地址信息、未知地点、风景名胜
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%'))"
            elif ways_audit_child == '购物市场':
                # 购物
                sql = "select sta_name,degree from source_sta_list WHERE sta_num IN (select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%'))"
            else:
                print('--ways_audit 聚类站稽核err---')
            result = mysql.query(sql)
            if len(result) > 0:
                for i in range(len(result)):
                    result_list.append(list(result[i]))
            else:
                print('ways_audit_child err!')

        elif ways_audit == '直供站参考':
            pass
        else:
            print('--energy_way 横向稽核err--')
    else:
        print('--energy_way err1!--')


    # # 1.自留三方区分
    # if veidoo == '自留':
    #     # 2.横向纵向区分
    #     if energy_way == '纵向稽核':
    #         if ways_audit == '同站稽核':
    #             if ways_audit_child == '节假日':
    #                 pass
    #             elif ways_audit_child == '日':
    #                 pass
    #             elif ways_audit_child == '周':
    #                 pass
    #             elif ways_audit_child == '月':
    #                 pass
    #             else:
    #                 print('--ways_audit 同站稽核err---')
    #         elif ways_audit == '同站稳态稽核':
    #             if ways_audit == '待定0':
    #                 if ways_audit_child == '待定1':
    #                     pass
    #                 elif ways_audit_child == '待定2':
    #                     pass
    #                 else:
    #                     print('--ways_audit 同站稳态稽核err---')
    #         else:
    #             print('--energy_way 纵向稽核err--')
    #     elif energy_way == '横向稽核':
    #         if ways_audit == '同类站稽核':
    #             if ways_audit_child == '费用核算类型':
    #                 resultdict['title'] = '费用核算类型'
    #                 sql = "select acco_type,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY acco_type"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('费用核算类型err!')
    #             elif ways_audit_child == '基站设备':
    #                 resultdict['title'] = '基站设备'
    #                 sql = "select sta_deta,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY sta_deta"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             elif ways_audit_child == '是否移交铁塔':
    #                 resultdict['title'] = '是否移交铁塔'
    #                 sql = "select move_tower,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY move_tower"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             elif ways_audit_child == '县市':
    #                 resultdict['title'] = '县市'
    #                 sql = "select cou_city,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY cou_city"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             else:
    #                 print('--ways_audit 同类站稽核err---')
    #         elif ways_audit == '聚类站稽核':
    #             if ways_audit_child == '学校区域':
    #                 pass
    #             elif ways_audit_child == '小区':
    #                 pass
    #             elif ways_audit_child == '商业区':
    #                 pass
    #             else:
    #                 print('--ways_audit 聚类站稽核err---')
    #         elif ways_audit == '直供站参考':
    #             pass
    #         else:
    #             print('--energy_way 横向稽核err--')
    #     else:
    #         print('--energy_way err1!--')
    # elif veidoo == '三方':
    #     # 2.横向纵向区分
    #     if energy_way == '纵向稽核':
    #         if ways_audit == '同站稽核':
    #             if ways_audit_child == '节假日':
    #                 pass
    #             elif ways_audit_child == '日':
    #                 pass
    #             elif ways_audit_child == '周':
    #                 pass
    #             elif ways_audit_child == '月':
    #                 pass
    #             else:
    #                 print('--ways_audit 同站稽核err---')
    #         elif ways_audit == '同站稳态稽核':
    #             if ways_audit == '待定0':
    #                 if ways_audit_child == '待定1':
    #                     pass
    #                 elif ways_audit_child == '待定2':
    #                     pass
    #                 else:
    #                     print('--ways_audit 同站稳态稽核err---')
    #         else:
    #             print('--energy_way 纵向稽核err--')
    #     elif energy_way == '横向稽核':
    #         if ways_audit == '同类站稽核':
    #             if ways_audit_child == '费用核算类型':
    #                 resultdict['title'] = '费用核算类型'
    #                 sql = "select acco_type,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY acco_type"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('费用核算类型err!')
    #             elif ways_audit_child == '基站设备':
    #                 resultdict['title'] = '基站设备'
    #                 sql = "select sta_deta,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY sta_deta"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             elif ways_audit_child == '是否移交铁塔':
    #                 resultdict['title'] = '是否移交铁塔'
    #                 sql = "select move_tower,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY move_tower"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             elif ways_audit_child == '县市':
    #                 resultdict['title'] = '县市'
    #                 sql = "select cou_city,SUM(degree) from source_sta_list WHERE 1=1 GROUP BY cou_city"
    #                 result = mysql.query(sql)
    #                 if len(result) > 0:
    #                     for i in range(len(result)):
    #                         result_list.append(list(result[i]))
    #                 else:
    #                     print('基站设备err!')
    #             else:
    #                 print('--ways_audit 同类站稽核err---')
    #         elif ways_audit == '聚类站稽核':
    #             if ways_audit_child == '学校区域':
    #                 pass
    #             elif ways_audit_child == '小区':
    #                 pass
    #             elif ways_audit_child == '商业区':
    #                 pass
    #             else:
    #                 print('--ways_audit 聚类站稽核err---')
    #         elif ways_audit == '直供站参考':
    #             pass
    #         else:
    #             print('--energy_way 横向稽核err--')
    #     else:
    #         print('--energy_way err1!--')
    # else:
    #     print('--veidoo err!--')

    resultdict['result_list'] = result_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps