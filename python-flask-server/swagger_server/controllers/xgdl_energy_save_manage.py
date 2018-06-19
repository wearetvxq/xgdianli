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


# ##############################################
#                                              #
#                  节能页面                    #
#                                              #
# ##############################################

# 节能基站列表
def jn_get_all_sta():
    # 1、找到用电量大于3000的基站
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}


    jn_sta_list = []
    jn_sta_use = []
    sql = "select sta_name,sta_num FROM basic_sta_list WHERE id in(select sta_id from basic_met_list WHERE met_num IN (SELECT user_id FROM source_elec_info WHERE total_power > 2500)) GROUP BY sta_num"
    result = mysql.query(sql)
    if len(result) > 0 :
        for i in range(len(result)):
            jn_sta_list.append(str(result[i][0]) + '_' + str(result[i][1]))
    else:
        print('没有找到基站!')

    resultdict['jn_sta_list'] = jn_sta_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 电容数量
def set_count():
    resultdict = {}
    resultdict['set_count'] = [3, 4, 5, 6, 7, 8, 9, 10]
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 电容方案
def cap_method(sta_name='', cap_count=3):
    resultdict = {}
    cap_method = []

    failure_rate = 1500.25

    # 默认无功功率值为1500.25
    resultdict['title'] = ['基站名称', '无功功率', '固定电容', '可变电容', '微调电容', '描述', '其他']
    cap_method.append(sta_name)   #基站名称
    cap_method.append(failure_rate)  #无功功率
    cap_1 = int(int(failure_rate / (cap_count-2)) / 10^len(str(int(failure_rate / (cap_count-2))))) * 10^len(str(int(failure_rate / (cap_count-2))))
    cap_1_count = cap_count-2
    cap_method.append(str(cap_1_count) + ' 个' + str(cap_1) + '容量（F）')  #固定电容

    cap_2 = int(failure_rate - cap_1 * (cap_count-2))
    cap_method.append(str(1) + ' 个' + str(cap_2) + '容量（F）')  #可变电容
    cap_method.append(str(1) + ' 个' + str(failure_rate - int(failure_rate)) + '容量（F）')   #微调电容
    cap_method.append('这是基础方案，可更加实际情况微调')  #描述
    cap_method.append('test')   #其他


    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# ###########################方案二##########################
# 基站区域
def dr_area():
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict['title'] = '区域'

    area_list = ['全部']
    sql = "select cou_city FROM source_sta_list GROUP BY cou_city"
    print('sql:', sql)
    result = mysql.query(sql)
    for i in range(len(result)):
        area_list.append(result[i][0])

    resultdict['area_list'] = area_list
    # resultdict['area_list'] = ['安陆']
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 基站和功率因素列表
# 有功、无功--》确认基站 和功率因素
# 区域、功率因素--》基站
# 基站名--》基站 和功率因素
def dr_sta_list(power_fac=0, sta_area='', sta_name=''):
    resultdict = {}
    mysql = MySQL(2)
    mysql.mysql_connect()
    sta_list_old = []
    sta_list_new = []
    sta_num_all = []
    if power_fac == '' or power_fac == 0:
        power_fac = 1
    # 有功、无功 - -》基站编号
    sql_base = "select sta_no,sta_name FROM xgdl_high_voltage_user  WHERE 3_active_ele !='' AND 3_not_active_ele !='' AND 3_not_active_ele !='0' GROUP BY sta_no"
    result_base = mysql.query(sql_base)  # 有无用、有功数据的 基站编号

    if len(result_base) > 0:
        for i in range(len(result_base)):
            sta_list_single_old = []
            sta_name_old = result_base[i][0] + '_' + result_base[i][1]
            sql = "select min(`date`) as minday, max(`date`) as maxday from xgdl_high_voltage_user WHERE sta_no = '{}' AND 3_active_ele !='' AND 3_not_active_ele !='' AND 3_not_active_ele !='0'".format(result_base[i][0])
            result = mysql.query(sql)   # 单个基站 有数据的 最大、最小时间
            # 天数:
            days = com.days_apart(result[0][0], result[0][1])
            if days == 0:
                print('最大最小天，是同一天')
            sql_max = "select SUM(3_active_ele), SUM(3_not_active_ele) from xgdl_high_voltage_user WHERE sta_no = '{}' AND `date`='{}'".format(result_base[0][0], result[0][1])
            result_max = mysql.query(sql_max)  # 单个基站 有数据的 最大和

            sql_min = "select SUM(3_active_ele), SUM(3_not_active_ele) from xgdl_high_voltage_user WHERE sta_no = '{}' AND `date`='{}'".format(result_base[0][0], result[0][0])
            result_min = mysql.query(sql_min)  # 单个基站 有数据的 最小和

            active_avg= (float(result_max[0][0]) - float(result_min[0][0])) / days  # 有功平均值
            not_active_avg= (float(result_max[0][1]) - float(result_min[0][1])) / days  # 无功平均值
            power_fac_avg_old = active_avg / (active_avg + not_active_avg)  # 平均功率因素
            sta_list_single_old.append(sta_name_old)
            # sta_list_single_old.append(power_fac_avg_old)
            sta_list_single_old.append('%.3f' % float(power_fac_avg_old))
            sta_list_old.append(sta_list_single_old)  # 所有基站、原功率因数列表

    else:
        print('--获取基站编号和名称错误!---')
    # 先通过区域--》所有的基站
    if sta_area != '全部':
        sql = "select sta_no FROM Xgdl_Basic_Stalist  WHERE city ='{}' AND sta_no != '' GROUP BY sta_no".format(sta_area)
        result = mysql.query(sql)  # 某个区域的所有基站编号
        for i in range(len(result)):
            sta_num_all.append(result[i][0])
        if sta_name != '':
            for i in range(len(sta_list_old)):
                if sta_name == sta_list_old[i][0].split('_')[1]:
                    sta_list_new.append(sta_list_old[i])
                    # sta_list_new.append('%.3f' % float(sta_list_old[i][1]))
        else:
            ss = 'HCZF08'
            if float(sta_list_old[0][1]) <= float(power_fac) and ss in sta_num_all:
                print('-11')
            for j in range(len(sta_list_old)):
                if str(sta_list_old[j][0].split('_')[0]) in sta_num_all and float(sta_list_old[j][1]) <= float(power_fac):
                    sta_list_new.append(sta_list_old[j])
                    # sta_list_new.append('%.3f' % float(sta_list_old[j][1]))
    else:
        # sql = "select sta_num FROM source_sta_list  WHERE cou_city ='{}' AND sta_num != '' GROUP BY sta_num".format(sta_area)
        # print('sql1:', sql)
        # result = mysql.query(sql)  # 某个区域的所有基站编号
        # for i in range(len(result)):
        #     sta_num_all.append(result[i][0])
        # print('sta_num_all1:', sta_num_all)
        if sta_name != '':
            for i in range(len(sta_list_old)):
                if sta_name == sta_list_old[i][0].split('_')[1]:
                    sta_list_new.append(sta_list_old[i])
                    # sta_list_new.append('%.3f' % float(sta_list_old[i][1]))
        else:
            for j in range(len(sta_list_old)):
                if float(sta_list_old[j][1]) <= float(power_fac):
                    sta_list_new.append(sta_list_old[j])
                    # sta_list_new.append('%.3f' % float(sta_list_old[j][1]))

    print('sta_list_new:', sta_list_new)

    if sta_list_new == []:
        sta_list_new = ['']

    resultdict['title'] = ['基站名称', '平均功率因素']
    resultdict['sta_list'] = sta_list_new

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 无功能率折线图
def dr_reactive_pow_chart(sta_name=''):
    resultdict = {}
    date_list = []
    no_power_list = []
    mysql = MySQL(2)
    mysql.mysql_connect()


    # 1.基站--》最小最大时间--》所有时间--》实际时间列表
    # 2.所有的后一天 - 前一天

    if sta_name != '':

        sql = "select `date` from xgdl_high_voltage_user WHERE sta_no = '{}' AND 3_not_active_ele !='' AND 3_not_active_ele !='0' GROUP BY `date` ORDER BY `date`".format(sta_name.split('_')[0])
        sql_1 = "select avg(3_not_active_ele) from xgdl_high_voltage_user WHERE sta_no = '{}' AND 3_not_active_ele !='' AND 3_not_active_ele !='0' GROUP BY `date` ORDER BY `date`".format(sta_name.split('_')[0])

        result = mysql.query(sql)  # 选中的单个基站  最大、最小时间
        result_1 = mysql.query(sql_1)  # 选中的单个基站  最大、最小时间

        for i in range(1,len(result)):
            date_list.append(result[i][0])
            if result_1[i][0] != '':
                # no_power_list.append(float(result_1[i][0]) - float(result_1[i-1][0]))
                no_power_list.append('%.3f' % (float('%.3f' % float(result_1[i][0])) - float('%.3f' % float(result_1[i-1][0]))))
            else:
                no_power_list.append('%.3f' % float(0))

    resultdict['title'] = ['无功功率']
    resultdict['pow_list'] = no_power_list
    resultdict['date_list'] = date_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 基站详情
def get_sta_details(sta_name=''):
    resultdict = {}
    sta_details = []
    sta_title = ['名称', '空调设备', '灯', '电池']
    if sta_name != '':
        sta_details.append(sta_name)
        sta_details.append('999kw 1台')
        sta_details.append('500')
        sta_details.append('200')

    resultdict['sta_title'] = sta_title
    resultdict['sta_details'] = sta_details
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 电容方案
def capacitance_scheme(sta_name='', power_fac_old='', power_fac_new=''):
    resultdict = {}
    details = []
    mysql = MySQL(2)
    mysql.mysql_connect()

    if sta_name != '' and power_fac_old != '' and power_fac_new != '':

        no_power_list = []
        sql_1 = "select avg(3_not_active_ele),total_ratio from xgdl_high_voltage_user WHERE sta_no = '{}' AND 3_not_active_ele !='' AND 3_not_active_ele !='0' GROUP BY `date` ORDER BY `date`".format(
            sta_name.split('_')[0])

        result_1 = mysql.query(sql_1)  # 选中的单个基站  最大、最小时间

        for i in range(1, len(result_1)):
            if result_1[i][0] != '':
                # no_power_list.append(float(result_1[i][0]) - float(result_1[i-1][0]))
                no_power_list.append(
                    float('%.3f' % (float('%.3f' % float(result_1[i][0])) - float('%.3f' % float(result_1[i - 1][0])))))
        no_power_avg = sum(no_power_list) / len(no_power_list) * 3 * int(result_1[i][1])

        # 1.电容补偿值 （实际补偿无功功率）
        sql = "select avg(3_not_active_ele) from xgdl_high_voltage_user WHERE sta_no = '{}' AND 3_not_active_ele !='' AND 3_not_active_ele !='0' ORDER BY `date`".format(sta_name.split('_')[0])
        result = mysql.query(sql)  #
        # 1. 算出有功
        active_power = float(no_power_avg) / (1-float(power_fac_old)) - float(no_power_avg)
        change_save = float(active_power) / float(power_fac_old) - float(active_power) / float(power_fac_new)  # 节省功率
        change_save_year = change_save * 365  # 节省功率
        change_cost = change_save * 0.8
        change_cost_yaer = change_save * 0.8 * 365

        put_into = 20000
        details.append(sta_name)
        details.append('%.3f' % float(no_power_avg))
        details.append(power_fac_old)
        details.append(power_fac_new)
        details.append('%.3f' % float(change_save))
        details.append('%.3f' % float(change_cost))
        details.append('%.3f' % float(change_save_year))
        details.append('%.3f' % float(change_cost_yaer))
        details.append('预计投入 ' + str(put_into) + ' 元')

        describe = '预计 ' + str(int(float(put_into) / float(change_cost))) + '天左右 收回成本'
        details.append(describe)

    resultdict['details'] = details
    resultdict['title'] = ['电容方案']
    resultdict['title_list'] = ['基站名称', '平均电容补偿值', '原功率因素', '期望功率因素', '日平均省电量', '日平均省电费(单价：0.8元/度)', '年省电量(365天)',
                                '年省电费(365天)', '投入', '成本回收周期']

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 电容节能，节省电量计算：
# 参数：
#     原功率因素
#     期望功率因素
#     有功功率
def dr_change_save(power_fac_0='', power_fac_1='', active_power=''):
    # 算出节省电量
    active_power = ('%.3f' % float(active_power))
    power_fac_0 = ('%.3f' % float(power_fac_0))
    power_fac_1 = ('%.3f' % float(power_fac_1))
    change_save= active_power / power_fac_0 - active_power / power_fac_1    # 节省功率


    pass