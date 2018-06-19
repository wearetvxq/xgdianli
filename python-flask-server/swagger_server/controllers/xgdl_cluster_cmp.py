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
from dateutil import rrule
import time

# ##############################################
#                                              #
#                  聚类对比页面                #
#                                              #
# ##############################################

# 1. 所有电表--》所有基站--》所有聚类列表
# 2.单个聚类--》所有基站基站--》所有电表--》所有最大最小中的共同时间-1个月
# 3.列表展示：单个聚类--》所有基站，做电表读数累加，按月取平均值。


# 0. 高压、低压
def get_high_low_vol_1():
    resultdict = {}
    resultdict['title'] = '高低压'
    resultdict['way_of_cmp'] = ['低压', '高压']

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第二版
# 1.获取所有聚类列表：
def cluster_list(high_low_vol='', choose_city=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    list_cluster = []

    if high_low_vol == '低压':
        # table = 'xgdl_low_voltage_user'
        table = 'xgdl_low_valtage_user_sta_no'
    elif high_low_vol == '高压':
        # table = 'xgdl_high_voltage_user'
        table = 'xgdl_high_voltage_user_sta_no'
    else:
        print('--high_low_vol err!-')
    sql = "SELECT sta_no FROM {} GROUP BY sta_no".format(table)
    result = mysql.query(sql)
    if len(result) > 0:
        if choose_city == 'all':
            sql_0 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            print('-sql_0:---', sql_0)
            result_0 = mysql.query(sql_0)
            sql_1 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            print('-sql_1:---', sql_1)
            result_1 = mysql.query(sql_1)
            sql_2 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_2 = mysql.query(sql_2)
            sql_3 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_3 = mysql.query(sql_3)
            sql_4 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_4 = mysql.query(sql_4)
            sql_5 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_5 = mysql.query(sql_5)
            sql_6 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_6 = mysql.query(sql_6)
            sql_7 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_7 = mysql.query(sql_7)
            sql_8 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_8 = mysql.query(sql_8)
            sql_9 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(table)
            result_9 = mysql.query(sql_9)
        else:
            sql_0 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            print('-sql_0:--1-', sql_0)
            result_0 = mysql.query(sql_0)
            sql_1 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            print('-sql_1:---', sql_1)
            result_1 = mysql.query(sql_1)
            sql_2 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '公司%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_2 = mysql.query(sql_2)
            sql_3 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_3 = mysql.query(sql_3)
            sql_4 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_4 = mysql.query(sql_4)
            sql_5 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '金融%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_5 = mysql.query(sql_5)
            sql_6 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_6 = mysql.query(sql_6)
            sql_7 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '医疗%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_7 = mysql.query(sql_7)
            sql_8 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_8 = mysql.query(sql_8)
            sql_9 = "select sta_num FROM basic_sta_list WHERE sta_num in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND id in(select sta_id from basic_sta_type WHERE `type` like '购物%') AND sta_num in(SELECT sta_no FROM {} GROUP BY sta_no) limit 1".format(choose_city,
                table)
            result_9 = mysql.query(sql_9)

        if len(result_0) > 0:
            list_cluster.append('交通相关区')
        if len(result_1) > 0:
            list_cluster.append('住宿区')
        if len(result_2) > 0:
            list_cluster.append('公司企业')
        if len(result_3) > 0:
            list_cluster.append('政府及社团')
        if len(result_4) > 0:
            list_cluster.append('科教区')
        if len(result_5) > 0:
            list_cluster.append('金融机构')
        if len(result_6) > 0:
            list_cluster.append('餐饮店')
        if len(result_7) > 0:
            list_cluster.append('医疗院')
        if len(result_8) > 0:
            list_cluster.append('风景区')
        if len(result_9) > 0:
            list_cluster.append('购物市场')
    else:
        print('--电表没找到基站--')
    resultdict['title'] = '聚类列表'
    resultdict['list_cluster'] = list_cluster

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# # 方案一
# # 1.获取所有聚类列表：
# def cluster_list_old():
#     resultdict = {}
#     mysql = MySQL(2)
#     mysql.mysql_connect()
#     list_cluster = []
#
#     sql = "select sta_num FROM basic_sta_list WHERE id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#     result = mysql.query(sql)
#     if len(result) > 0:
#         sql_0 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_0 = mysql.query(sql_0)
#         sql_1 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_1 = mysql.query(sql_1)
#         sql_2 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_2 = mysql.query(sql_2)
#         sql_3 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_3 = mysql.query(sql_3)
#         sql_4 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_4 = mysql.query(sql_4)
#         sql_5 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_5 = mysql.query(sql_5)
#         sql_6 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_6 = mysql.query(sql_6)
#         sql_7 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_7 = mysql.query(sql_7)
#         sql_8 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_8 = mysql.query(sql_8)
#         sql_9 = "select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%') AND id in(select sta_id FROM basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) group BY sta_id )"
#         result_9 = mysql.query(sql_9)
#
#         if len(result_0) > 0:
#             list_cluster.append('交通相关区')
#         if len(result_1) > 0:
#             list_cluster.append('住宿区')
#         if len(result_2) > 0:
#             list_cluster.append('公司企业')
#         if len(result_3) > 0:
#             list_cluster.append('政府及社团')
#         if len(result_4) > 0:
#             list_cluster.append('科教区')
#         if len(result_5) > 0:
#             list_cluster.append('金融机构')
#         if len(result_6) > 0:
#             list_cluster.append('餐饮店')
#         if len(result_7) > 0:
#             list_cluster.append('医疗院')
#         if len(result_8) > 0:
#             list_cluster.append('风景区')
#         if len(result_9) > 0:
#             list_cluster.append('购物市场')
#     else:
#         print('--电表没找到基站--')
#
#     resultdict['title'] = '聚类列表'
#     resultdict['list_cluster'] = list_cluster
#
#     mysql.mysql_close()
#     reps = jsonify(resultdict)
#     reps.headers["Access-Control-Allow-Origin"] = "*"
#     return reps


# 方案二
# 2.获取所有的时间列表
def get_time_by_cluster(cluster_name='', high_low_vol='', choose_city=''):
    # 1.通过聚类--》基站编号--》电表
    # 2.找到电表所有的时间，找出共同时间
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
        table_1 = 'xgdl_low_valtage_user_sta_no'
    elif high_low_vol == '高压':
        table = 'xgdl_high_voltage_user'
        table_1 = 'xgdl_high_voltage_user_sta_no'
    else:
        print('--high_low_vol err!-')

    # if high_low_vol == '低压':
    #     table = 'xgdl_low_voltage_user'
    #     table = 'xgdl_low_valtage_user_sta_no'
    # elif high_low_vol == '高压':
    #     table = 'xgdl_high_voltage_user'
    #     table = 'xgdl_high_voltage_user'
    # else:
    #     print('--high_low_vol err!-')
    if choose_city == 'all':
        if cluster_name == '交通相关区':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '住宿区':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '公司企业':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '政府及社团':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '科教区':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '金融机构':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '餐饮店':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '医疗院':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '风景区':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) GROUP BY sta_no".format(table_1)
        elif cluster_name == '购物市场':
            sql = "select sta_no from {} WHERE sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) GROUP BY sta_no".format(table_1)
        else:
            print('--聚类名称错误---')
    else:
        if cluster_name == '交通相关区':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '住宿区':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '公司企业':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '政府及社团':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '科教区':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '金融机构':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '餐饮店':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '医疗院':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '风景区':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) GROUP BY sta_no".format(table_1, choose_city)
        elif cluster_name == '购物市场':
            sql = "select sta_no from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list group BY sta_num) AND sta_no in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) GROUP BY sta_no".format(table_1, choose_city)
        else:
            print('--聚类名称错误---')

    result = mysql.query(sql)

    if len(result) > 0:
        min_date_list = []
        max_date_list = []
        if len(result) == 1:
            sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE sta_no='{}'".format(table, result[0][0])
            result_1 = mysql.query(sql)
            min_date_list.append(result_1[0][0])
            max_date_list.append(result_1[0][1])
        else:

            for i in range(len(result)):
                sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE sta_no='{}'".format(table, result[i][0])
                result_1 = mysql.query(sql)
                min_date_list.append(result_1[0][0])
                max_date_list.append(result_1[0][1])

        min_sta_day = min(min_date_list)
        max_end_day = max(max_date_list)
        sta_day = min_sta_day
        end_day = max_end_day
        # end_day = com.minus_months(str(max_end_day)[:7]) + '-' + str(max_end_day).split('-')[2]
    else:
        print('--没有找到聚类后的id-')
        sta_day = ''
        end_day = ''


    # date_list = com.get_month_list(sta_day,end_day)
    # 找出某段日期内的所有的日期列表

    if sta_day == '':
        flag = 0
        date_list = []
    else:
        flag = 1
        date_list = com.get_days_list(str(sta_day), str(end_day))
    resultdict['flag'] = flag
    resultdict['date_list'] = date_list
    resultdict['title'] = '时间'
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# # 方案一
# # 2.获取所有的时间列表
# def get_time_by_cluster_old(cluster_name=''):
#     # 1.通过聚类--》基站编号--》电表
#     # 2.找到电表所有的时间，找出共同时间
#     resultdict = {}
#     mysql = MySQL(2)
#     mysql.mysql_connect()
#
#     if cluster_name == '交通相关区':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')))"
#     elif cluster_name == '住宿区':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')))"
#     elif cluster_name == '公司企业':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')))"
#     elif cluster_name == '政府及社团':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')))"
#     elif cluster_name == '科教区':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')))"
#     elif cluster_name == '金融机构':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')))"
#     elif cluster_name == '餐饮店':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')))"
#     elif cluster_name == '医疗院':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')))"
#     elif cluster_name == '风景区':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')))"
#     elif cluster_name == '购物市场':
#         sql = "select id from basic_met_list WHERE id in(select met_id from orig_met_check group BY met_id) AND sta_id IN (select id from basic_sta_list WHERE sta_num in(select sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')))"
#     else:
#         print('--聚类名称错误---')
#
#     result = mysql.query(sql)
#
#     if len(result) > 0:
#         min_date_list = []
#         max_date_list = []
#         if len(result) == 1:
#             sql = "select min(`date`) as minday,max(`date`) as maxday from orig_sta_dl WHERE sta_id=(SELECT sta_id FROM basic_met_list WHERE id={})".format(result[0][0])
#             result_1 = mysql.query(sql)
#             min_date_list.append(result_1[0][0])
#             max_date_list.append(result_1[0][1])
#         else:
#
#             for i in range(len(result)):
#                 sql = "select min(`date`) as minday,max(`date`) as maxday from orig_sta_dl WHERE  sta_id=(SELECT sta_id FROM basic_met_list WHERE id={})".format(result[i][0])
#                 result_1 = mysql.query(sql)
#                 min_date_list.append(result_1[0][0])
#                 max_date_list.append(result_1[0][1])
#
#         min_sta_day = min(min_date_list)
#         max_end_day = max(max_date_list)
#         sta_day = min_sta_day
#         end_day = max_end_day
#         # end_day = com.minus_months(str(max_end_day)[:7]) + '-' + str(max_end_day).split('-')[2]
#     else:
#         print('--没有找到聚类后的id-')
#         sta_day = ''
#         end_day = ''
#
#
#     # date_list = com.get_month_list(sta_day,end_day)
#     # 找出某段日期内的所有的日期列表
#
#     if sta_day == '':
#         flag = 0
#         date_list = []
#     else:
#         flag = 1
#         date_list = com.get_days_list(str(sta_day), str(end_day))
#     resultdict['flag'] = flag
#     resultdict['date_list'] = date_list
#     resultdict['title'] = '时间'
#     mysql.mysql_close()
#     reps = jsonify(resultdict)
#     reps.headers["Access-Control-Allow-Origin"] = "*"
#     return reps


# 方案二
# 聚类展示：
def cluster_show(cluster_name='', select_month='', high_low_vol='', choose_city=''):
    # 1、展示内容：基站、用电量
    # 2、按照 基站，找出基站对的电表
    # 步骤1：电表--》找到所有的基站
    # 步骤2: 基站--》找到所有的电表取值，如果等于0 ，不算在内，取平均值。
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_list = []
    sta_list_1 = []
    sta_list_2 = []
    ele_list = []
    ele_list_1 = []
    ele_list_2 = []
    result_list = []

    next_day = com.get_y_t_date(select_month, '1', count=1)
    next_day = str(next_day).split(' ')[0]
    sta_name_list = []
    total_power = []
    if high_low_vol == '低压':
        table = 'xgdl_low_voltage_user'
        table_1 = 'xgdl_low_valtage_user_sta_no'
        if choose_city == 'all':
            if cluster_name == '交通相关区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
            elif cluster_name == '住宿区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '公司企业':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
            elif cluster_name == '政府及社团':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '科教区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '金融机构':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '餐饮店':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '医疗院':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '风景区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '购物市场':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            else:
                print('--聚类名称错误---')
        else:
            if cluster_name == '交通相关区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '住宿区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '公司企业':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '政府及社团':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '科教区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '金融机构':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '餐饮店':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '医疗院':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '风景区':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '购物市场':
                sql = "select sta_no,sta_name,`date`,total_ratio,active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            else:
                print('--聚类名称错误---')
        print('--sql:---', sql)
        result_base = mysql.query(sql)
        print('--result_base:---', result_base)

        result_list = []
        for i in range(len(result_base)):
            m = 0
            result_single = []
            for j in range(len(result_base)):
                if result_base[i][0] == result_base[j][0] and result_base[i][2] > result_base[j][2]:
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(str(result_base[i][1]) + '_' + str(result_base[i][0]))
                        # result_single.append(float('%.3f' % float(float(result_base[i][4]) - float(result_base[j][4]))))
                        result_single.append(float('%.3f' % float((float(result_base[i][4]) - float(result_base[j][4])) * float(result_base[i][3]))))
                        result_list.append(result_single)
        result_list.sort(key=lambda x: x[1])
        result_list.reverse()
        for k in range(len(result_list)):
            sta_name_list.append(result_list[k][0])
            total_power.append(result_list[k][1])

    elif high_low_vol == '高压':
        table = 'xgdl_high_voltage_user'
        table_1 = 'xgdl_high_voltage_user_sta_no'
        if choose_city == 'all':
            if cluster_name == '交通相关区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
            elif cluster_name == '住宿区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '公司企业':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
            elif cluster_name == '政府及社团':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '科教区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '金融机构':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '餐饮店':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '医疗院':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '风景区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            elif cluster_name == '购物市场':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(table,select_month,next_day)

            else:
                print('--聚类名称错误---')
        else:
            if cluster_name == '交通相关区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '住宿区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '公司企业':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
            elif cluster_name == '政府及社团':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '科教区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '金融机构':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '餐饮店':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '医疗院':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '风景区':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            elif cluster_name == '购物市场':
                sql = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_1 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)
                sql_2 = "select sta_no,sta_name,`date`,total_ratio,3_active_ele,3_not_active_ele from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                    table, choose_city, select_month, next_day)

            else:
                print('--聚类名称错误---')

        result_base = mysql.query(sql)
        result_base_1 = mysql.query(sql_1)
        result_base_2 = mysql.query(sql_2)

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
                if result_base[i][0] == result_base[j][0] and result_base[i][2] > result_base[j][2] and \
                                result_base[i][4] != '' and result_base[j][4] != '':
                    if m > 1:
                        break
                    else:
                        m += 1
                        if result_base[i][5] == '':
                            not_active_ele_1 = '%.3f' % float(0)
                        else:
                            not_active_ele_1 = '%.3f' % float(result_base[i][5])
                        if result_base[j][5] == '':
                            not_active_ele_2 = '%.3f' % float(0)
                        else:
                            not_active_ele_2 = '%.3f' % float(result_base[j][5])
                        result_single.append(str(result_base[i][1]) + '_' + str(result_base[i][0]))
                        # result_single.append(str('%.3f' % float(float(result_base[i][4]) - float(result_base[j][4]))))
                        result_single.append('%.3f' % float((float(result_base[i][4]) + float(not_active_ele_1) - float(result_base[j][4]) - float(not_active_ele_2)) * float(result_base[i][3])))
                        result_list_0.append(result_single)
                if result_base_1[i][0] == result_base_1[j][0] and result_base_1[i][2] > result_base_1[j][2] and \
                                result_base_1[i][4] != '' and result_base_1[j][4] != '':
                    if x > 1:
                        break
                    else:
                        x += 1
                        result_single_1.append(str(result_base_1[i][1]) + '_' + str(result_base_1[i][0]))
                        # result_single_1.append(str('%.3f' % float(float(result_base_1[i][4]) - float(result_base_1[j][4]))))
                        result_single_1.append('%.3f' % float((float(result_base_1[i][4]) + float(not_active_ele_1) - float(
                            result_base_1[j][4]) - float(not_active_ele_2)) * float(result_base_1[i][3])))
                        result_list_1.append(result_single_1)
                if result_base_2[i][0] == result_base_2[j][0] and result_base_2[i][2] > result_base_2[j][2] and \
                                result_base_2[i][4] != '' and result_base_2[j][4] != '':
                    if y > 1:
                        break
                    else:
                        y += 1
                        result_single_2.append(str(result_base_2[i][1]) + '_' + str(result_base_2[i][0]))
                        # result_single_2.append(str('%.3f' % float(float(result_base_2[i][4]) - float(result_base_2[j][4]))))
                        result_single_2.append('%.3f' % float((float(result_base_2[i][4]) + float(not_active_ele_1) - float(
                            result_base_2[j][4]) - float(not_active_ele_2)) * float(result_base_2[i][3])))
                        result_list_2.append(result_single_2)
        for i in range(len(result_list_0)):
            result_list_single = []
            result_list_single.append(result_list_0[i][0])
            result_list_single.append(float('%.3f' % float(float(result_list_0[i][1]) + float(result_list_1[i][1]) + float(result_list_2[i][1]))))
            result_list.append(result_list_single)
        result_list.sort(key=lambda x: x[1])
        result_list.reverse()
        for k in range(len(result_list)):
            sta_name_list.append(result_list[k][0])
            total_power.append(result_list[k][1])

    else:
        print('--high_low_vol err!-')

    resultdict['sta_list'] = sta_name_list
    resultdict['ele_list'] = total_power
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# # 方案一
# # 聚类展示：
# def cluster_show_old(cluster_name='', select_month=''):
#     # 1、展示内容：基站、用电量
#     # 2、按照 基站，找出基站对的电表
#     # 步骤1：电表--》找到所有的基站
#     # 步骤2: 基站--》找到所有的电表取值，如果等于0 ，不算在内，取平均值。
#     resultdict = {}
#     mysql = MySQL(2)
#     mysql.mysql_connect()
#     sta_list = []
#     sta_list_1 = []
#     sta_list_2 = []
#     ele_list = []
#     ele_list_1 = []
#     ele_list_2 = []
#     result_list = []
#
#     if cluster_name == '交通相关区':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '住宿区':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '公司企业':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '政府及社团':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '科教区':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '金融机构':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '餐饮店':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '医疗院':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '风景区':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     elif cluster_name == '购物市场':
#         sql = "select sta_num,sta_name from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%') AND id IN (select sta_id from basic_met_list WHERE id in(select met_id from orig_met_check GROUP BY met_id))"
#     else:
#         print('--聚类名称错误---')
#
#     result = mysql.query(sql)
#     for i in range(len(result)):
#         sta_list.append(str(result[i][1]) + '_' + str(result[i][0]))
#         sta_list_1.append(result[i][0])
#
#
#     # 2.通过基站名找到所有这个月和下个月的电表度数
#     # 找到下个月的时间
#     # select_month = str(select_month)[:7]
#     # # select_month = datetime.datetime.strptime(str(select_month)[:7], "%Y-%m")
#     # print('--select_month----', select_month)
#     # next_month = str(com.add_months(datetime.datetime.strptime(str(select_month)[:7], "%Y-%m"), 1))[:7]
#     # print('--next_month----', next_month)
#
#     select_day = select_month
#     next_day = com.get_y_t_date(select_day, '1', 1)
#     for i in range(len(sta_list_1)):
#         sta_ele_list = []
#         first_month_list = []
#         met_list = []
#         # 1.找到所有的电表
#         sql = "select total_power from orig_sta_dl WHERE sta_id =(SELECT id FROM basic_sta_list WHERE sta_num ='{}') AND `date` like '{}'".format(sta_list_1[i], select_day)
#         result_base = mysql.query(sql)
#         if len(result_base) == 0:
#             ele_list_1.append(float('0'))
#         else:
#             ele_list_1.append(float(result_base[0][0]))
#
#     for i in range(len(sta_list)):
#         result_list.append([sta_list[i],ele_list_1[i]])
#     if len(result_list) > 0:
#         result_list_r = com.list_sort(result_list)
#         for i in range(len(result_list_r)):
#             sta_list_2.append(result_list_r[i][0])
#             ele_list_2.append(result_list_r[i][1])
#
#     resultdict['ele_list'] = ele_list_2
#     resultdict['sta_list'] = sta_list_2
#     mysql.mysql_close()
#     reps = jsonify(resultdict)
#     reps.headers["Access-Control-Allow-Origin"] = "*"
#     return reps


def cluster_details(cluster_name='', select_month='', high_low_vol='', sta_name='', PageIndex=1, choose_city=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()

    next_day = com.get_y_t_date(select_month, '1', count=1)
    next_day = str(next_day).split(' ')[0]
    sta_name_list = []
    total_power = []
    if high_low_vol == '低压':
        title = ['id', '县市', '基站编号', '基站名称', '客户编号', '基站类型', '分布', '客户名称', '供电单位', '电表地址', '数据日期', '正向有功电能示值', '综合倍率']

        table = 'xgdl_low_voltage_user'
        if choose_city == 'all':
            if sta_name == '' or sta_name == '全部':
                if cluster_name == '交通相关区':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                elif cluster_name == '住宿区':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '公司企业':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                elif cluster_name == '政府及社团':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '科教区':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '金融机构':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '餐饮店':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '医疗院':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '风景区':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '购物市场':
                    sql = "select * from {} WHERE sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                else:
                    print('--聚类名称错误---')
            else:
                sql = "select * from {} WHERE sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(table,sta_name.split('_')[1], select_month, next_day)
        else:
            if sta_name == '' or sta_name == '全部':
                if cluster_name == '交通相关区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                elif cluster_name == '住宿区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '公司企业':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                elif cluster_name == '政府及社团':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '科教区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '金融机构':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '餐饮店':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '医疗院':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '风景区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '购物市场':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                else:
                    print('--聚类名称错误---')
            else:
                sql = "select * from {} WHERE sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(table, sta_name.split('_')[1], select_month, next_day)

        result_base = mysql.query(sql)
        # sta_no, sta_name, `date`, total_ratio, active_ele
        # 0、1、2 、3 、4
        # 2、3、10、12、11
        result_list = []
        for i in range(len(result_base)):
            m = 0
            result_single = []
            for j in range(len(result_base)):
                if result_base[i][2] == result_base[j][2] and result_base[i][9] == result_base[j][9] and result_base[i][10] > result_base[j][10]:
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(list(result_base[j]))
                        result_single[0][11] = float('%.3f' % float((float(result_base[i][11]) - float(result_base[j][11]))))
                        result_list.append(result_single[0])
                        # result_single.append(str(result_base[i][3]) + '_' + str(result_base[i][2]))
                        # result_single.append(float('%.3f' % float(float(result_base[i][11]) - float(result_base[j][11]))))
                        # result_list.append(result_single)

        new_result_list = []
        for id in result_list:
            if id not in new_result_list:
                new_result_list.append(id)
        new_result_list.sort(key=lambda x: x[11])
        new_result_list.reverse()
        show_tz = com.paging(new_result_list, everyPage_count=10, PageIndex=PageIndex)
        page_resultList = show_tz[0]
        rowCount = show_tz[1]
        pageCount = show_tz[2]

        # result_list.sort(key=lambda x: x[3])
        # result_list.reverse()
        # for k in range(len(result_list)):
        #     sta_name_list.append(result_list[k][0])
        #     total_power.append(result_list[k][1])

    elif high_low_vol == '高压':
        title = ['id', '县市', '基站编号', '基站名称', '客户编号', '基站类型', '分布', '客户名称', '供电单位', '数据日期', '三相正向有功总电能示值', '三相正向无功总电能示值',
                 '综合倍率', '电流曲线相序']

        table = 'xgdl_high_voltage_user'
        if choose_city == 'all':
            if sta_name == '' or sta_name == '全部':
                if cluster_name == '交通相关区':
                    sql = "select * from {} WHERE ele_curve= 'A相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                elif cluster_name == '住宿区':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '公司企业':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                elif cluster_name == '政府及社团':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '科教区':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '金融机构':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '餐饮店':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '医疗院':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                elif cluster_name == '风景区':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                elif cluster_name == '购物市场':
                    sql = "select * from {} WHERE ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)
                    sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, select_month, next_day)

                else:
                    print('--聚类名称错误---')
            else:
                sql = "select * from {} WHERE ele_curve= 'A相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(table,sta_name.split('_')[1], select_month, next_day)
                sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(table,sta_name.split('_')[1], select_month, next_day)
                sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(table,sta_name.split('_')[1], select_month, next_day)
        else:
            if sta_name == '' or sta_name == '全部':
                if cluster_name == '交通相关区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND  ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '交通%' or `type` like '交通设施%' or `type` like '摩托车%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                elif cluster_name == '住宿区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '住宿%' or `type` like '商务住宅%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '公司企业':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '公司%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                elif cluster_name == '政府及社团':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '政府机构%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '科教区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '科教%' or `type` like '体育%' or `type` like '公共设施%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '金融机构':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '金融%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '餐饮店':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相'and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '餐饮%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '医疗院':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '医疗%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                elif cluster_name == '风景区':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '地名地址信息%' or `type` like '未知地点%' or `type` like '风景名胜%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                elif cluster_name == '购物市场':
                    sql = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'A相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_1 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'B相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)
                    sql_2 = "select * from {} WHERE sta_no in (SELECT sta_no FROM basic_city_list WHERE city='{}') AND ele_curve= 'C相' and sta_no in(select sta_num from basic_sta_list WHERE id in(select sta_id from basic_sta_type WHERE `type` like '购物%')) AND `date` BETWEEN '{}' AND '{}'".format(
                        table, choose_city, select_month, next_day)

                else:
                    print('--聚类名称错误---')
            else:
                sql = "select * from {} WHERE ele_curve= 'A相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(
                    table, sta_name.split('_')[1], select_month, next_day)
                sql_1 = "select * from {} WHERE ele_curve= 'B相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(
                    table, sta_name.split('_')[1], select_month, next_day)
                sql_2 = "select * from {} WHERE ele_curve= 'C相' and sta_no='{}' AND `date` BETWEEN '{}' AND '{}'".format(
                    table, sta_name.split('_')[1], select_month, next_day)

        result_base = mysql.query(sql)
        result_base_1 = mysql.query(sql_1)
        result_base_2 = mysql.query(sql_2)

        result_list = []
        result_list_0 = []
        result_list_1 = []
        result_list_2 = []
        # sta_no, sta_name, `date`, total_ratio, 3_active_ele
        # 0、1、2、3 、4
        # 2、3、9、12、10
        for i in range(len(result_base)):
            m = 0
            x = 0
            y = 0
            result_single = []
            result_single_1 = []
            result_single_2 = []
            for j in range(len(result_base)):
                if result_base[i][2] == result_base[j][2] and result_base[i][9] > result_base[j][9] and \
                                result_base[i][10] != '' and result_base[j][10] != '':
                    if m > 1:
                        break
                    else:
                        m += 1
                        result_single.append(list(result_base[j]))

                        result_single[0][10] = float(
                            '%.3f' % float(float(result_base[i][10]) - float(result_base[j][10])))
                        if result_base[i][11] == '':
                            base_1 = '%.3f' % float(0)
                        else:
                            base_1 = '%.3f' % float(float(result_base[i][11]))
                        if result_base[j][11] == '':
                            base_2 = '%.3f' % float(0)
                        else:
                            base_2 = '%.3f' % float(float(result_base[j][11]))
                        result_single[0][11] = str('%.3f' % float(float(base_1) - float(base_2)))
                        result_list_0.append(result_single[0])
                        # result_single.append(str(result_base[i][3]) + '_' + str(result_base[i][2]))
                        # result_single.append(str('%.3f' % float(float(result_base[i][10]) - float(result_base[j][10]))))
                        # result_list_0.append(result_single)
                if result_base_1[i][2] == result_base_1[j][2] and result_base_1[i][9] > result_base_1[j][9] and \
                                result_base_1[i][10] != '' and result_base_1[j][10] != '':
                    if x > 1:
                        break
                    else:
                        x += 1
                        result_single_1.append(list(result_base_1[j]))
                        result_single_1[0][10] = float(
                            '%.3f' % float(float(result_base_1[i][10]) - float(result_base_1[j][10])))
                        if result_base_1[i][11] == '':
                            base_1 = '%.3f' % float(float(0))
                        else:
                            base_1 = '%.3f' % float(float(result_base_1[i][11]))
                        if result_base_1[j][11] == '':
                            base_2 = '%.3f' % float(float(0))
                        else:
                            base_2 = '%.3f' % float(float(result_base_1[j][11]))
                            result_single_1[0][11] = str(float('%.3f' % float(float(base_1) - float(base_2))))
                        result_list_1.append(result_single_1[0])
                if result_base_2[i][2] == result_base_2[j][2] and result_base_2[i][9] > result_base_2[j][9] and \
                                result_base_2[i][10] != '' and result_base_2[j][10] != '':
                    if y > 1:
                        break
                    else:
                        y += 1
                        result_single_2.append(list(result_base_2[j]))
                        result_single_2[0][10] = float(
                            '%.3f' % float(float(result_base_2[i][10]) - float(result_base_2[j][10])))
                        if result_base_2[i][11] == '':
                            base_1 = '%.3f' % float(float(0))
                        else:
                            base_1 = '%.3f' % float(float(result_base_2[i][11]))
                        if result_base_2[j][11] == '':
                            base_2 = '%.3f' % float(float(0))
                        else:
                            base_2 = '%.3f' % float(float(result_base_2[j][11]))
                            result_single_2[0][11] = str(float('%.3f' % float(float(base_1) - float(base_2))))
                        result_list_2.append(result_single_2[0])
        for i in range(len(result_list_0)):
            result_list.append(result_list_0[i])
            result_list.append(result_list_1[i])
            result_list.append(result_list_2[i])
            # result_list_single = []
            # result_list_single.append(result_list_0[i][0])
            # result_list_single.append(float('%.3f' % float(
            #     float(result_list_0[i][1]) + float(result_list_1[i][1]) + float(result_list_2[i][1]) / 3)))
            # result_list.append(result_list_single)
        new_result_list = []
        for dd in result_list:
            if dd not in new_result_list:
                new_result_list.append(dd)
        new_result_list.sort(key=lambda x: x[11])
        new_result_list.reverse()
        show_tz = com.paging(new_result_list, everyPage_count=10, PageIndex=PageIndex)
        # show_tz = com.paging(result_list, everyPage_count=10, PageIndex=PageIndex)
        page_resultList = show_tz[0]
        rowCount = show_tz[1]
        pageCount = show_tz[2]
        # for k in range(len(result_list)):
        #     sta_name_list.append(result_list[k][0])
        #     total_power.append(result_list[k][1])

    else:
        print('--high_low_vol err!-')

    resultdict['title'] = title
    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
