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
#                  能耗预测页面                #
#                                              #
# ##############################################

# 1.三方、自留

# 2.电费预测
# 3.电表用电预测
# 4.基站窃电挖掘


# 1.预测内容
def predict_method(ammeter_or_station=''):
    resultdict = {}
    resultdict['title'] = '预测内容'
    if ammeter_or_station == '电表':
        resultdict['way_predict'] = ['电表用电预测']

    elif ammeter_or_station == '基站':
        resultdict['way_predict'] = ['基站用电预测']
        # resultdict['way_predict'] = ['基站用电预测', '基站窃电挖掘']
    else:
        resultdict['way_predict'] = []

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.0 预测方式
def ammeter_and_station():
    resultdict = {}
    resultdict['title'] = '预测方式'
    resultdict['ammeter_and_station'] = ['基站', '电表']


    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.1 获取所有电表：
def get_ammeter_station_list(veidoo='', ammeter_or_station=''):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    ammeter_list = []
    if ammeter_or_station == '电表':
        resultdict['title'] = '电表列表'
        if veidoo == '三方':
            table_name = 'pred_met_dl'

        elif veidoo == '自留':
            table_name = 'pred_met_yd'
        else:
            print('--veidoo err!----')

        sql = "select met_num from {} GROUP BY met_num".format(table_name)
        result = mysql.query(sql)
        for i in range(len(result)):
            ammeter_list.append(result[i][0])
    elif ammeter_or_station == '基站':
        resultdict['title'] = '基站列表'
        if veidoo == '三方':
            table_name = 'Predict_sta_load'
            sql = "select sta_name,sta_no FROM Xgdl_Basic_Stalist WHERE sta_no in(select sta_num from {} GROUP BY sta_no) GROUP BY sta_no".format(
                table_name)
        elif veidoo == '自留':
            table_name = 'pred_sta_yd'
            sql = "select sta_name,sta_num FROM basic_sta_list WHERE id in(select sta_id from {} GROUP BY sta_id) GROUP BY sta_num".format(
                table_name)
        else:
            print('--veidoo err!----')


        result = mysql.query(sql)
        if len(result) > 0:
            for i in range(len(result)):
                ammeter_list.append(str(result[i][0]) + '_' + str(result[i][1]))
        else:
            print('费用核算类型err!')
    else:
        resultdict['title'] = ''

    resultdict['lists'] = ammeter_list
    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 1.3根据具体电表或具体基站获取时间段
def get_time_range(veidoo='', ammeter_or_station='',detile=''):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    if veidoo == '三方':
        if ammeter_or_station == '电表':
            table_name = 'pred_met_dl'
            sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE met_num={}".format(table_name,detile)
        elif ammeter_or_station == '基站':
            table_name = 'Predict_sta_load'
            detile = str(detile).split('_')[1]
            sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE sta_num='{}'".format(table_name, detile)
        else:
            print('--ammeter_or_station err!----')
    elif veidoo == '自留':
        if ammeter_or_station == '电表':
            table_name = 'pred_met_yd'
            sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE met_num={}".format(table_name,detile)
        elif ammeter_or_station == '基站':
            table_name = 'pred_sta_yd'
            detile = str(detile).split('_')[1]
            sql = "select min(`date`) as minday,max(`date`) as maxday from {} WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}' limit 1)".format(table_name, detile)
        else:
            print('--ammeter_or_station err!----')
    else:
        print('--veidoo err!----')
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


# 3.预测数据
def predict_data(veidoo='',ammeter_or_station='',ammeter_or_station_detile='', way_predict='', StartDate='', EndDate=''):
    # veidoo: 维度
    # ammeter_or_station：电表或基站
    # ammeter_or_station_detile：电表或基站
    # way_predict:预测方式
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    result_list = []
    if veidoo == '三方':
        if ammeter_or_station == '电表':
            table_name = 'pred_met_dl'
            if way_predict == '电费预测':
                pass
            elif way_predict == '电表用电预测':
                resultdict['title'] = 'kw·h'
                sql = "select `date`,total_power from {} WHERE met_num={} ".format(table_name, ammeter_or_station_detile)
                sql += " and `date` BETWEEN '" + StartDate + "' and '" + EndDate + "'"
                result = mysql.query(sql)
            else:
                print('--way_predict err!----')
        elif ammeter_or_station == '基站':
            table_name = 'Predict_sta_load'
            if way_predict == '基站用电预测':
                resultdict['title'] = 'kw·h'
                ammeter_or_station_detile = ammeter_or_station_detile.split('_')[1]
                sql = "select `date`,`load` from {} WHERE sta_num='{}'".format(table_name,ammeter_or_station_detile)
                sql += " and `date` BETWEEN '" + StartDate + "' and '" + EndDate + "'"
                result = mysql.query(sql)
            elif way_predict == '基站窃电挖掘':
                pass
            else:
                print('--way_predict err!----')
        else:
            print('--ammeter_or_station err!----')
    elif veidoo == '自留':
        if ammeter_or_station == '电表':
            table_name = 'pred_met_yd'
            if way_predict == '电费预测':
                pass
            elif way_predict == '电表用电预测':
                resultdict['title'] = ''
                sql = "select `date`,total_power from {} WHERE met_num={} ".format(table_name,
                                                                                   ammeter_or_station_detile)
                sql += " and `date` BETWEEN '" + StartDate + "' and '" + EndDate + "'"
                result = mysql.query(sql)
            else:
                print('--way_predict err!----')
        elif ammeter_or_station == '基站':
            table_name = 'pred_sta_yd'
            if way_predict == '基站用电预测':
                resultdict['title'] = 'kw·h'
                ammeter_or_station_detile = ammeter_or_station_detile.split('_')[1]
                sql = "select `date`,total_power from {} WHERE sta_id=(select id from basic_sta_list WHERE sta_num='{}' limit 1) ".format(
                    table_name, ammeter_or_station_detile)
                sql += " and `date` BETWEEN '" + StartDate + "' and '" + EndDate + "'"
                result = mysql.query(sql)
            elif way_predict == '基站窃电挖掘':
                pass
            else:
                print('--way_predict err!----')
        else:
            print('--ammeter_or_station err!----')
    else:
        print('--veidoo err!----')

    for i in range(len(result)):
        result_list.append(list(result[i]))
    resultdict['result_list'] = result_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps

# def energy_charge_predict():
#     pass
#
#
# def base_station_electricity_predict():
#     pass
#
#
# def base_station_electricity_dig():
#     pass
