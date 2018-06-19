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
import time




"""def low_err_count(choose_city=''):
    '''
    低压异常数量
    :return:
    '''
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}

    if choose_city == 'all':
        sql = "select count(id) from xgld_load_abnormal WHERE `type` != '正常' AND sta_num IN (SELECT sta_no FROM xgdl_low_voltage_user GROUP BY sta_no)"
    else:
        sql = "select count(id) from xgld_load_abnormal WHERE sta_num in(select sta_no FROM xgdl_low_valtage_user_sta_no WHERE city='{}') AND `type` != '正常' AND sta_num IN (SELECT sta_no FROM xgdl_low_voltage_user GROUP BY sta_no)".format(choose_city)

    print('--sql-1-', sql)
    result = mysql.query(sql)

    resultdict['count'] = result[0][0]

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps

def city_voltage_low(choose_city=''):
    '''
    高压基站 对应的城市
    :return:
    '''
    # choose_city = 'all'
    print('---choose_city:-', choose_city)
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    if choose_city == 'all':
        city_list = ['全部']

        sql = "select city from xgdl_low_voltage_user GROUP BY city"
        print('--sql-1-', sql)
        result = mysql.query(sql)

        for i in range(len(result)):
            city_list.append(result[i][0])
    else:
        city_list = [choose_city]
    print('---city_list:-', city_list)
    resultdict['city_list'] = city_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def type_err_low():
    '''
    低压基站，异常类型
    :return:
    '''
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    type_list = ['全部']

    sql = "select `type` from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_low_voltage_user GROUP BY sta_no) GROUP BY `type`"
    print('--sql-2-', sql)
    result = mysql.query(sql)

    for i in range(len(result)):
        type_list.append(result[i][0])

    resultdict['type_list'] = type_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def table_low_err(city='', type_err='', PageIndex=1):
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    type_list = []

    err_list = []
    sta_no_list = []
    sta_list = []
    met_reader_list = []

    if city != '' and city != '全部':
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE `type`='{}' AND sta_num in(select sta_no FROM xgdl_low_voltage_user WHERE city='{}')".format(type_err, city)
            print('--sql-3-', sql)
        else:
            sql = "select * from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_low_voltage_user WHERE city='{}')".format(city)
            print('--sql-4-', sql)
    else:
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE `type`='{}' AND sta_num in(select sta_no FROM xgdl_low_voltage_user)".format(type_err)
            print('--sql-3-', sql)
        else:
            sql = "select * from xgld_load_abnormal WHERE `type` != '正常' AND sta_num in(select sta_no FROM xgdl_low_voltage_user)"
            print('--sql-4-', sql)
    result = mysql.query(sql)
    print('--result-4-', result)
    print('--result-4-', len(result))
    for i in range(len(result)):
        err_list.append(list(result[i]))
        sta_no_list.append(result[i][1])
    for i in range(len(err_list)):
        err_list[i] = err_list[i][1:]
        # del(err_list[i][0])
    print('--err_list-4-', err_list)
    if len(sta_no_list) > 0:
        if len(sta_no_list) == 1:
            sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num = '{}'".format(sta_no_list[0])
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[0])
            sql_3 = "select city from xgdl_low_voltage_user WHERE sta_no = '{}' GROUP BY city".format(sta_no_list[0])
            # sql_3 = "select sta_no,city from xgdl_low_voltage_user WHERE sta_no = '{}'".format(sta_no_list[0])
            print('--sql-5-', sql_1)
            print('--sql-6-', sql_2)
            print('--sql-6-0-', sql_2)
        if len(sta_no_list) > 1:
            # for i in range(len(sta_no_list)):
            #     sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num = '{}'".format(sta_no_list[i])
            #     sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[i])
            #     result_1 = mysql.query(sql_1)
            #     result_2 = mysql.query(sql_2)
            #     print('---------------------------')
            #     print('--result_1--', result_1)
            #     print('--result_1--', len(result_1))
            #     print('--result_2--', result_2)
            #     print('--result_2--', len(result_2))
            #     print('---------------------------')
            # print('--len(sta_no_list):---', len(sta_no_list))
            sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num in {}".format(tuple(sta_no_list))
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no in {}".format(tuple(sta_no_list))
            # sql_3 = "select sta_no,city from xgdl_low_voltage_user WHERE sta_no in {} GROUP BY sta_no".format(tuple(sta_no_list))
            sql_3 = "select sta_no,city from xgdl_low_valtage_user_sta_no WHERE sta_no in {} GROUP BY sta_no".format(tuple(sta_no_list))
            print('--sql-7-', sql_1)
            print('--sql-8-', sql_2)
            print('--sql-8-0-', sql_3)
        print('time_0: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_1 = mysql.query(sql_1)
        print('time_1: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_2 = mysql.query(sql_2)
        print('time_2: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_3 = mysql.query(sql_3)
        print('time_3: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('--result_1--', result_1)
        print('--result_1--', len(result_1))
        print('--result_2--', result_2)
        print('--result_2--', len(result_2))
        print('--result_3--', result_3)
        print('--result_3--', len(result_3))
        for i in range(len(result_1)):
            err_list[i][0] = str(result_1[i][0]) + '_' + str(result_1[i][1])

        for i in range(len(result_2)):
            err_list[i].insert(1, result_2[i][0])

        for i in range(len(result_3)):
            err_list[i].insert(2, result_3[i][1])

        # for i in range(len(err_list)):
        #     sql_3 = "select city from xgdl_low_voltage_user WHERE sta_no = '{}' GROUP BY city".format(err_list[i][0].split('_')[0])
        #     result_3 = mysql.query(sql_3)
        #     err_list[i].insert(2, result_3[0][0])
    print('--err_list--', err_list)

    show_tz = com.paging(err_list, everyPage_count=10, PageIndex=PageIndex)
    page_resultList = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]

    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount

    title = ['基站', '抄表责任人', '区域', '异常类型', '负荷均值', '低值负荷覆盖率', '跳变次数', '热季负荷', '其他季负荷']
    resultdict['title'] = title

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps"""

# ##############################################
#                                              #
#                  跳变异常页面                  #
#                                              #
# ##############################################

def jump_err_count(choose_city=''):
    '''
    跳变异常数量
    :return:
    '''
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    print (choose_city)
    #如果选择城市为全部，就找到所有跳变异常数量
    if choose_city=='' or choose_city=='全部':
        choose_city='all'
    if choose_city == 'all':
        sql = "select count(id) from xgld_load_abnormal WHERE type='跳变异常' AND sta_num IN (SELECT sta_no FROM Xgdl_Basic_Stalist GROUP BY sta_no)"
    if choose_city!='all':
        sql = "select count(id) from xgld_load_abnormal WHERE sta_num in(select sta_no FROM Xgdl_Basic_Stalist WHERE city='{}') AND type = '跳变异常' AND sta_num IN (SELECT sta_no FROM Xgdl_Basic_Stalist GROUP BY sta_no)".format(choose_city)

    print('--sql-1-', sql)
    result = mysql.query(sql)

    resultdict['count'] = result[0][0]
    print (resultdict['count'])

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
#选择地区
def city_voltage_jump(choose_city=''):
    '''
    跳变异常 对应的城市
    :return:
    '''
    # choose_city = 'all'
    print('---choose_city:-', choose_city)
    if choose_city=='' or choose_city=='全部':
        choose_city='all'
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    if choose_city == 'all':
        city_list = ['全部']

        sql = "select city from Xgdl_Basic_Stalist WHERE sta_no in (SELECT sta_num FROM xgld_load_abnormal WHERE type='跳变异常' GROUP BY sta_num)"
        print('--sql-1-', sql)
        result = mysql.query(sql)

        for i in range(len(result)):
            city_list.append(result[i][0])
        city_list=list(set(city_list))
        #排序
        for x in range(len(city_list)):
            if city_list[x]=='全部':
                haha=city_list[0]
                city_list[0]='全部'
                city_list[x]=haha
    else:
        city_list = [choose_city]
    print('---city_list:-', city_list)
    resultdict['city_list'] = city_list

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps



def table_jump_err(city='', PageIndex=1):
    err1_list=[]
    type_err='跳变异常'
    mysql = MySQL(2)
    mysql.mysql_connect()
    resultdict = {}
    type_list = []
    mean_list=[]
    jump_list=[]
    print ('++++++++++++++++++++++++')
    print (PageIndex)

    err_list = []
    sta_no_list = []
    sta_list = []
    met_reader_list = []

    if city != '' and city != '全部':
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE type='跳变异常' AND sta_num in(select sta_no FROM Xgdl_Basic_Stalist WHERE city='{}') ORDER BY jump DESC ".format(city)
            print('--sql-3-', sql)
    else:
        if type_err != '' and type_err != '全部':
            sql = "select * from xgld_load_abnormal WHERE type='跳变异常' AND sta_num in(select sta_no FROM Xgdl_Basic_Stalist) ORDER BY jump DESC "
            print('--sql-4-', sql)


    result = mysql.query(sql)
    print('--result-4-', result)
    print('--result-4-', len(result))
    for i in range(len(result)):
        err_list.append(list(result[i]))
        #基站编号
        sta_no_list.append(result[i][1])
        #负荷均值(大于50度才会选取)
        mean_list.append(result[i][3])
        #跳变次数
        jump_list.append(result[i][5])

    for i in range(len(err_list)):
        err_list[i] = [err_list[i][1],err_list[i][3],err_list[i][5]]
    print('--err_list-4-', err_list)
    if len(sta_no_list) > 0:
        if len(sta_no_list) == 1:
            #基站编号和基站名称
            sql_1 = "select sta_no,sta_name from Xgdl_Basic_Stalist WHERE sta_no ='{}'".format(sta_no_list[0])
            #责任人
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[0])
            #区域
            sql_3 = "select city from Xgdl_Basic_Stalist WHERE sta_no = '{}' GROUP BY city".format(sta_no_list[0])
            # sql_3 = "select sta_no,city from xgdl_low_voltage_user WHERE sta_no = '{}'".format(sta_no_list[0])
            print('--sql-5-', sql_1)
            print('--sql-6-', sql_2)
            print('--sql-6-0-', sql_2)
        if len(sta_no_list) > 1:
            # for i in range(len(sta_no_list)):
            #     sql_1 = "select sta_num,sta_name from basic_sta_list WHERE sta_num = '{}'".format(sta_no_list[i])
            #     sql_2 = "select met_reader from basic_reader_list WHERE sta_no = '{}'".format(sta_no_list[i])
            #     result_1 = mysql.query(sql_1)
            #     result_2 = mysql.query(sql_2)
            #     print('---------------------------')
            #     print('--result_1--', result_1)
            #     print('--result_1--', len(result_1))
            #     print('--result_2--', result_2)
            #     print('--result_2--', len(result_2))
            #     print('---------------------------')
            # print('--len(sta_no_list):---', len(sta_no_list))
            sql_1 = "select sta_no,sta_name from Xgdl_Basic_Stalist WHERE sta_no in {} order by FIND_IN_SET(sta_no,'XG1879,XG8173,XG1100,XG0757,XG1846,XG0571,XG2003,XG0159,XC1349,XG1004,XG1028,XG-0750,XG0977,XG1156,XG-0777,XHhc46,XG2965,XG1536,XG-2773,XG-1190,XG-2680,XG-0736,XG1574,XG0685,XG1576,XG0102,XG2113,XG0482,XG2756,XG0180,XG-2757,XG0456,XG0479,XG0642,XG1131,XG0438,XG1035,XG0524,XG1038,XG-0368,XG0645,XG0114,XG-2560,XG0145,XG1057,XG0389,XG0887,XG0913,XG0144,XG-0058,XG-0331,XG0663,XG-0073,XG0626,XG0633,XG0682,XG-1176,XG-1683,XG1559,XG0969,XG1107,XG0631,XG1449,XG1478,XG-2672,XG2642,XG0133,XG1136,XG-0714,XG0655,XG1226,XG0454,XG-0231,XG0283,XG1283,XG-1353,XG1527,XG0143,XG0189,XG0235,XG0625,XG0692,XG1348,XG0377,XG1455,XG1531,XG-0468,XG0433,XG0443,XG0934,XG0229,XG-0079,XG1253,XG-1375,XG0447,XG1867,XG0480,XG0953,XG0993,XG1217,XG1506,XG-5073,XG1578,XG2557,XG0982,XG1033,XG0397,XG1510,XG0905,XG0495,XG0135,XG0141,XG0234,XG1206,XG0326,XG1334,XG-1281,XG0449,XG-0080,XG0247,XG0628,XG0636,XG-0610,XG-0725,XG1248,XG1330,XG0418,XG1570,XG2226,XG0131,XG0132,XG0974,XG0248,XG-0452,XG0639,XG0643,XG0367,XG1060,XG0227,XG0236,XG0629,XG0637,XG0683,XG-1264,XG1469,XG0429,XG-1608,XG1512,XG-2671,XG1568,XG0925,XG2245,XG2867,XG0515,XG0522,XG0171,XG-0060,XG0675,XG0684,XG-1090,XG1345,XG-1292,XG-1384,XG0450,XG1869,XG0923,XG0118,XG2670,XG0124,XG0140,XG0541,XG0188,XG0200,XG1059,XG0600,XG0634,XG0262,XG0272,XG0276,XG1216,XG0672,XG0681,XG1344,XG0390,XG0420,XG1492,XG1496,XG0883,XG0900,XG0477,XG0932,XG0521,XG0542,XG0549,XG-0021,XG-0056,XG0225,XG0228,XG0232,XG0259,XG-0716,XG0284,XG0285,XG0442,XG0137,XG0176,XG1036,XG-0020,XG0579,XG-0031,XG1069,XG-0063,XG1126,XG1129,XG1161,XG1163,XG-0476,XG0265,XG0649,XG1218,XG1227,XG0698,XG1471,XG0885,XG0888,XG-2873,XG0100,XG0474,XG0504,XG0963,XG2906,XG2909,XG0526,XG1012,XG-0769,XG0745,XG1447,XG0445,XG0467,XG0487,XG2811,XG0142,XG0146,XG0564,XG0567,XG1068,XG0599,XG1125,XG1133,XG1134,XG1158,XG0252,XG1162,XG1196,XG-0701,XG0280,XG0661,XG-0780,XG1252,XG-1066,XG-1280,XG-1371,XG-1520,XG0901,XG0112,XG2560,XG0493,XG0955,XG0966,XG0525,XG0987,XG0528,XG0157,XG1002,XG0553,XG0182,GX0986,XG0573,XG0584,XG-0062,XG-0084,XG1198,XG0659,XG0669,XG-1044,XG-1285,XG0426,XG-1393,XG0107,XG0921,XG2556,XG0536,GX0962,XG0574,XG0589,XG0219,XG-0048,XG1121,XG0606,XG1124,XG-0068,XG1127,XG-0098,XG1164,XG0635,XG0260,XG1172,XG1197,XG1199,XG0273,XG1219,XG1247,XG0693,XG0706,XG-1259,XG0792,XG0415,XG1458,XG0838,XG-1397,XG0430,XG-1417,XG0448,XG0455,XG0909,XG0469,XG2016,XG2558,XG0940,XG0494,XG0497,XG0126,XG0961,XG0136,XG0511,XG0970,XG0138,XG2923,XG2950,XG0529,XG0169,XG1008,XG0557,XG0561,XG1026,XG0575,XG-0023,XG0212,XG-0039,XG-0046,XG0243,XG0644,XG1201,XG1202,XG1210,XG1213,XG1250,XG0313,XG0328,XG-1265,XG-1333,XG-1340,XG0852,XG0870,XG0441,XG0116,XG2937,XG0153,XG0155,XG1023,XG1024,XG1025,XG0568,XG1034,XG0583,XG0586,XG0597,XG0598,XG0619,XG0249,XG1159,XG1168,XG0264,XG-0713,XG1205,XG0651,XG-0719,XG0653,XG0275,XG0282,XG0662,XG0665,XG0286,XG0667,XG-1177,XG-1261,XG0786,XG0407,XG0446,XG0452,XG0009,XG1584,XG0912,XG0924,XG0505,XG2859,XG0134,XG2944,XG0519,XG0158,XG0533,XG0996,XG1006,XG1007,XG0547,XG1009,XG0179,XG1017,XG1018,XG0195,XG-0022,XG0581,XG0207,XG0218,XG0594,XG1070,XG0618,XG0641,XG0271,XG-0723,XG-0748,XG1254,XG0695,XG0788,XG-1284,XG1477,XG0431,XG-1569,XG0889,XG-2819,XG0105,XG0922,XG0122,XG0123,XG0956,XG0513,XG2960,XG0150,XG0156,XG0537,XG0165,XG0168,XG0544,XG0178,XG1015,XG0181,XG1021,XG1030,XG1140,XG0687,XG1525,XG-1805,XG0540,XG0647,XG0559,XG1031,XG0582,XG1228,XG1427,XG0890,XG0908,XG0952,XG0523,XG0548,XG1437,XG0585,XG1235,XG0322,XG2899,XG0532,XG0527,XG0569,XG2914,XG0110,XG0978,XG1295')".format(tuple(sta_no_list))
            sql_2 = "select met_reader from basic_reader_list WHERE sta_no in {}".format(tuple(sta_no_list))
            # sql_3 = "select sta_no,city from xgdl_low_voltage_user WHERE sta_no in {} GROUP BY sta_no".format(tuple(sta_no_list))
            sql_3 = "select city from Xgdl_Basic_Stalist WHERE sta_no in {} GROUP BY sta_no".format(tuple(sta_no_list))
            print('--sql-7-', sql_1)
            print('--sql-8-', sql_2)
            print('--sql-9-', sql_3)
        print('time_0: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_1 = mysql.query(sql_1)
        print('time_1: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_2 = mysql.query(sql_2)
        print('time_2: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        result_3 = mysql.query(sql_3)
        print('time_3: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('--result_1--', result_1)#基站编号
        print('--result_1--', len(result_1))#长度
        print('--result_2--', result_2)#责任人
        print('--result_2--', len(result_2))#责任人长度
        print('--result_3--', result_3)#区域
        print('--result_3--', len(result_3))#区域长度
        print (len(err_list))
        print (len(result_1))

        for i in range(len(result_1)):
            print (result_1[i][0],err_list[i][0])
            if err_list[i][0]==str(result_1[i][0]):
                err_list[i][0]=str(result_1[i][1]) + '_' + str(result_1[i][0])



        for i in range(len(result_2)):
            haha=result_2[i][0]
            if haha==None:
                haha='-'
            err_list[i].insert(1, haha)

        for i in range(len(result_3)):
            err_list[i].insert(2, result_3[i][0])

        # for i in range(len(err_list)):
        #     sql_3 = "select city from xgdl_low_voltage_user WHERE sta_no = '{}' GROUP BY city".format(err_list[i][0].split('_')[0])
        #     result_3 = mysql.query(sql_3)
        #     err_list[i].insert(2, result_3[0][0])
    print('--err_list--', err_list)
    print ('-----------------------------------------------------------------')
    print (len(err_list))
    for i in err_list:
        if i[3]>=50:
            err1_list.append(i)
    show_tz = com.paging(err1_list, everyPage_count=10, PageIndex=PageIndex)
    page_resultList = show_tz[0]
    rowCount = show_tz[1]
    pageCount = show_tz[2]

    resultdict['page_resultList'] = page_resultList
    resultdict['rowCount'] = rowCount
    resultdict['pageCount'] = pageCount

    title = ['基站编号', '责任人', '区域','负荷均值','跳变次数','操作']
    resultdict['title'] = title

    mysql.mysql_close()
    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


