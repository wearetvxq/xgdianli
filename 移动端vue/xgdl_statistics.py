# -*- coding: UTF-8 -*-
import connexion
from datetime import date, datetime
from typing import List, Dict

import xlwt
from six import iteritems

# from swagger_server.utitl.all_dict import area_list
from swagger_server.utitl.all_dict import *
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from swagger_server.utitl.db import *
from flask import json, jsonify
from flask import Response, request
from swagger_server.utitl.excleutil import ExcleUtil1
import os, sys
import time
import math
import socket
import random
import tarfile
import zipfile
import datetime
import os
from multiprocessing import Process, Queue, Array, RLock
import multiprocessing


def get_statistics_list():
    '''
    re
    :return:
    '''
    try:
        resultdict = {}
        mysql = MySQL(2)
        mysql.mysql_connect()

        choose_city = 'all'

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
            elif result[i][1] == '基站未工作' or result[i][1] == '负荷过高' or result[i][1] == '负荷曲线连续三个月以上基本无变化' or result[i][
                1] == '跳变异常' or result[i][1] == '反季节变化':
                sta_list[i].append('red')
        for i in range(len(sta_list)):
            for j in range(len(result)):
                if sta_list[i][0] == result_1[j][0]:
                    sta_list[i][0] = str(result_1[j][0]) + '_' + str(result_1[j][1])

        sta_list = sta_list[:10]
        mysql.mysql_close()
        result = [{"station": item[0],
                   "type": item[1],
                   "load": str(item[2]),
                   "color": item[3]} for item in sta_list]
        return result
        '''  # sta_list.insert(0, ['基站', '异常类型', '负荷', '颜色'])#往0号位置插入
        # print('--sta_list--9--', sta_list)
        # 
        # resultdict['sta_list'] = sta_list
        # print('完')
        # 
        # reps = jsonify(resultdict)
        # reps.headers["Access-Control-Allow-Origin"] = "*"
        # return reps'''

        return {"code": 0, "msg": 'success', "result": result}
    except Exception as e:
        print(e)
        return {"code": "-1", "msg": "error"}


# p z s e area name money  yijiao desc
def get_statistics_inspect(page='1', size='10', starttime='', endtime='',
                           area='',
                           name='',
                           money='',
                           yijiao='',
                           desc='', ):
    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'

    data = _filter(AXgdlInspect,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   station=name,
                   type=money,
                   tower=yijiao,
                   )
    if desc != '':
        like = "%" + desc + "%"
        data = data.where(AXgdlInspect.desc % like)
    # desc = desc,  做成keyword


    total = data.count()
    data = data.paginate(int(page), int(size))
    # pass  # p z s e area name money  yijiao desc
    result = [{
        # ax.create(
        #     posttime=int(time.time()),
        #     company=row_data[1],
        #     area=row_data[2],
        #     station=row_data[3],
        #     desc=row_data[4],
        #     typr=row_data[5],
        #     inspect=get_keys(if_dict, row_data[9]),
        #     month='5',
        #     tower=row_data[6],
        #     rank=get_keys(if_dict, row_data[8])
        #
        # )


        'company': item.company,
        'area': area_dict[item.area],
        'station': item.station,
        'desc': item.desc,
        'type': item.type,
        'tower': item.tower,
        'month': item.month,
        'rank': if_dict[item.rank],
        'inspect': if_dict[item.inspect],
        'posttime': utc_timestamp_to_str(item.posttime),
    } for item in data]
    return {"code": 0, "msg": "success", "total": total, "result": result}


# company
# area
# station
# desc
# type
# tower
# month
# rank
# inspect
# posttime


def get_statistics_inspect_export(page='1', size='10', starttime='', endtime='',
                                  area='',
                                  name='',
                                  money='',
                                  yijiao='',
                                  desc='', ):
    # data = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'],
    #         ['a', 'b', 'c', 'd']]
    #
    # exprort(data, 'text', 'style4', 'A', 'B', 'C', 'D')
    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    data = _filter(AXgdlInspect,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   station=name,
                   type=money,
                   tower=yijiao,
                   )
    if desc != '':
        like = "%" + desc + "%"
        data = data.where(AXgdlInspect.desc % like)
    result = [[

        #     'company': item.company,
        #                'area': area_dict[item.area],
        # 'station': item.station,
        # 'desc': item.desc,
        # 'type': item.type,
        # 'tower': item.tower,
        # 'month': item.month,
        # 'rank': if_dict[item.rank],
        # 'inspect': if_dict[item.inspect],
        # 'posttime': utc_timestamp_to_str(item.posttime),

        item.company,
        area_dict[item.area],
        item.station,
        item.desc,
        item.type,
        item.tower,
        item.month,
        if_dict[item.rank],
        if_dict[item.inspect],
        utc_timestamp_to_str(item.posttime)]
        for item in data]
    name_list = ['代维公司', '县市', '基站名称', '基站设备明细'
        , '费用核算类型', '是否移交铁塔', '交维月份', '是否高级站点'
        , '1-4月份是否巡检', '巡检时间']
    filename = exprort(result, '巡检报表', 'style4', '代维公司', '县市', '基站名称', '基站设备明细'
                       , '费用核算类型', '是否移交铁塔', '交维月份', '是否高级站点'
                       , '1-4月份是否巡检', '巡检时间')

    return {
        "msg": "msg",
        "code": 0,
        "url": "192.168.188.178:86/xiaogan/{}".format(filename),
    }


# 有不用  名称和地区
# p z s e area name money  yijiao desc
def get_statistics_reading_export(page='1', size='10', starttime='', endtime='',
                                  area='',
                                  name='',
                                  money='',
                                  yijiao='',
                                  desc='', ):
    name_list = ['县市', '基站名称', '基站编号', '经度',
                 '纬度', '示数', '抄表时间', '照片']
    if endtime != '':
        endtime =endtime+' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'

    if area != '':
        area = get_keys(area_dict, area)
    data = _filter(AXgdlReading,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   name=name,
                   )

    result = [[
        area_dict[item.area],
        item.name,
        item.number,
        item.x_code,
        item.y_code,
        item.meter,
        utc_timestamp_to_str(item.posttime) ,
        item.pic
    ] for item in data]

    filename = exprort(result, '巡检报表', 'style4', '县市', '基站名称', '基站编号', '经度',
                       '纬度', '示数', '抄表时间', '照片')

    return {
        "msg": "msg",
        "code": 0,
        "url": "192.168.13.201:86/xiaogan/{}".format(filename),
    }


# page size  area name type tower desc
def get_statistics_reading(page='1', size='10', starttime='', endtime='',
                           area='',
                           name='',
                           money='',
                           yijiao='',
                           desc='', ):
    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'

    data = _filter(AXgdlReading,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   name=name,
                   )
    total = data.count()
    data = data.order_by(AXgdlReading.posttime.desc()).paginate(int(page), int(size))
    # pass  # p z s e area name money  yijiao desc
    result = [{
        'area': area_dict[item.area],
        'name': item.name,
        'number': item.number,
        'x_code': item.x_code,
        'y_code': item.y_code,
        'meter': item.meter,
        'posttime': utc_timestamp_to_str(item.posttime),
        'pic': item.pic
    } for item in data]
    return {"code": 0, "msg": "success", "total": total, "result": result}


# pa siz star end


# area
# station
# ground
# 地理位置
# produce
# frame
# 型号
# cap
# 容量
# transmission
# 传输基站公用
# 1
# ifmonitoring
# 是否安装单体监控
# 2
# ktpower
# 功率3
# kttype
# people


# area produce cap name type tower desc
def get_statistics_inventory(page='',
                             size='',
                             starttime='',
                             endtime='',
                             id='',
                             area='',
                             station='',
                             ground='',
                             produce='',
                             frame='',
                             cap='',
                             transmission='',
                             ifmonitoring='',
                             ktpower='',
                             kttype='',
                             people=''
                             ):
    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    data = _filter(AXgdlEquipment,
                   starttime=starttime,
                   endtime=endtime,
                   id=id,
                   area=area,
                   station=station,
                   ground=ground,
                   produce=produce,
                   frame=frame,
                   cap=cap,
                   transmission=transmission,
                   ifmonitoring=ifmonitoring,
                   ktpower=ktpower,
                   kttype=kttype,
                   peoplep=people,
                   )
    total = data.count()
    print(total)
    data = data.paginate(int(page), int(size))
    # for item in data:
    #
    #     result=json.dumps(item,default=lambda o:o.__dict__)
    # # result=data.__dict__
    #     print(result)
    result = [{
        'type': item.type,
        'area': item.area,
        'station': item.station,
        'number': item.number,
        'node': item.node,
        'ground': item.ground,
        'produce': item.produce,
        'frame': item.frame,
        'cap': item.cap,
        'starttime': item.starttime,
        'monitoring': item.monitoring,
        'rectification': item.rectification,
        'renumber': item.renumber,
        'modulecap': item.modulecap,
        'loadele': item.loadele,
        'transmission': item.transmission,
        'powerdown': item.powerdown,
        'oil': item.oil,
        'pic': item.pic,
        'desc': item.desc,
        'people': item.people,
        'phone': item.phone,
        'tid': item.tid,
        'group': item.group,
        'brand': item.brand,
        'changebox': item.changebox,
        'jifang': item.jifang,
        'kttype': item.kttype,
        'ktpower': item.ktpower,
        'ifmonitoring': item.ifmonitoring,
        'hbtime': item.hbtime,
        'iftransmission': item.iftransmission,
        'ifpowerdown': item.ifpowerdown,
        'ifstatus': item.ifstatus,
        'xuhao': item.xuhao,
        'posttime': item.posttime,
    } for item in data]

    return {"code": 0, "msg": "success", "total": total, "result": result}


# powerdown 二次下电 和什么在一起  meishi  ifpowerdown
# page
# area produce cap name type tower desc
def get_statistics_inventory_export(page='',
                                    size='',
                                    starttime='',
                                    endtime='',
                                    id='',
                                    area='',
                                    station='',

                                    ground='',
                                    produce='',
                                    frame='',
                                    cap='',
                                    transmission='',
                                    ifmonitoring='',
                                    ktpower='',

                                    kttype='',
                                    people=''
                                    ):
    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    data = _filter(AXgdlEquipment,
                   starttime=starttime,
                   endtime=endtime,
                   id=id,
                   area=area,
                   station=station,
                   ground=ground,
                   produce=produce,
                   frame=frame,
                   cap=cap,
                   transmission=transmission,
                   ifmonitoring=ifmonitoring,
                   ktpower=ktpower,
                   kttype=kttype,
                   peoplep=people,
                   )
    if id == '1':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.ground,
            item.produce,
            item.frame,
            item.cap,
            item.starttime,
            item.monitoring,
            item.rectification,
            item.renumber,
            item.modulecap,
            item.loadele,

            item.transmission,
            item.powerdown,
            item.ifstatus,
            item.ifpowerdown,
            item.oil,
            item.desc,
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4', '县市',
                           '基站名称',
                           '基站编码',
                           '节点类型',
                           '基站地理位置',
                           '生产厂家',
                           '机架型号',
                           '机架容量（A）',
                           '开始使用时间',
                           '监控模块型号',
                           '整流模块型号',
                           '整流模块数量（块）',
                           '模块容量',
                           '负载电流（A）',
                           
                           '传输及基站是否共用',
                           '是否有二次下电功能',
                           '目前运行状态是否正常',
                           '是否属于本地区停电频繁基站',
                           '该站是否配置了固定自启动油机',
                           '备注',
                           '填报人',
                           '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/xiaogan/{}".format(filename),
        }
    name_list1 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '基站地理位置',
        '生产厂家',
        '机架型号',
        '机架容量（A）',
        '开始使用时间',
        '监控模块型号',
        '整流模块型号',
        '整流模块数量（块）',
        '模块容量',
        '负载电流（A）',
        '传输及基站是否共用',
        '是否有二次下电功能',
        '目前运行状态是否正常',
        '是否属于本地区停电频繁基站',
        '该站是否配置了固定自启动油机',
        '备注',
        '填报人',
        '联系电话',
    ]
    # area
    # station
    # number
    # node
    # ground
    # produce
    # frame
    # cap
    # starttime
    # monitoring
    # rectification
    # renumber
    # modulecap
    # loadele
    # transmission
    # powerdown
    # ifstatus
    # ifpowerdown
    # oil
    # desc
    # people
    # phone
    if id == '2':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.ground,
            item.produce,
            item.frame,
            item.cap,
            item.group,
            item.ifmonitoring,
            item.starttime,
            item.loadele,
            item.hbtime,
            item.ifpowerdown,
            item.oil,
            item.desc,
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4', '县市',
                           '基站名称',
                           '基站编码',
                           '节点类型',
                           '基站地理位置',
                           '厂家',
                           '型号',
                           '容量（A）',
                           '组数',
                           '是否安装单体监控',
                           '开始使用时间',
                           '当前负载（A）',
                           '经放电测试大约后备时长（小时）',
                           '是否属于本地区停电频繁基站',
                           '该站是否配置了固定自启动油机',
                           '备注',
                           '填报人',
                           '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list2 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '基站地理位置',
        '厂家',
        '型号',
        '容量（A）',
        '组数',
        '是否安装单体监控',
        '开始使用时间',
        '当前负载（A）',
        '经放电测试大约后备时长（小时）',
        '是否属于本地区停电频繁基站',
        '该站是否配置了固定自启动油机',
        '备注',
        '填报人',
        '联系电话',
    ]

    # area
    # station
    # number
    # node
    # ground
    # produce
    # frame
    # cap
    # group
    # ifmonitoring
    # starttime
    # loadele
    # hbtime
    # ifpowerdown
    # oil
    # desc
    # people
    # phone
    if id == '3':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.produce,
            item.frame,
            item.ktpower,
            item.kttype,
            item.starttime,
            item.desc,
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4', '县市',
                           '基站名称',
                           '基站编码',
                           '节点类型',
                           '厂家'
                           '型号'
                           '功率（匹）'
                           '类型'
                           '开始使用时间'
                           '备注',
                           '填报人',
                           '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list3 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家'
        '型号'
        '功率（匹）'
        '类型'
        '开始使用时间'
        '备注',
        '填报人',
        '联系电话',
    ]
    #     area
    #     station
    #     number
    #     node
    #     produce
    #     frame
    #     ktpower
    #       kttype
    # starttime
    # desc
    # people
    # phone

    if id == '4':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.produce,
            item.frame,
            item.renumber,
            item.starttime,
            item.desc,
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',   '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家'
        '型号'
        '数量'
        '开始使用时间'
        '备注',
        '填报人',
        '联系电话',)
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list4 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家'
        '型号'
        '数量'
        '开始使用时间'
        '备注',
        '填报人',
        '联系电话',
    ]

    # area
    # station
    # number
    # node
    # produce
    # frame
    # renumber
    # starttime
    # desc
    # people
    # phone
    if id == '5':
        result = [[
            item.area,
            item.station,
            item.number,
            item.produce,
            item.frame,
            item.renumber,
            item.starttime,
            item.desc,
            item.people,
            item.phone,
        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',    '县市',
        '基站名称',
        '基站编码',
        '厂家'
        '型号'
        '数量'
        '开始使用时间'
        '备注',
        '填报人',
        '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list5 = [
        '县市',
        '基站名称',
        '基站编码',
        '厂家'
        '型号'
        '数量'
        '开始使用时间'
        '备注',
        '填报人',
        '联系电话',
    ]
    # area
    # station
    # number
    # produce
    # frame
    # renumber
    # starttime
    # desc
    # people
    # phone
    if id == '6':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.produce,
            item.frame,
            item.monitoring,
            item.ktpower,
            item.rectification,
            item.renumber,
            item.starttime,
            item.desc, 
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',  '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家',
        '局端型号',
        '监控型号',
        '功率（KW）',
        '模块型号',
        '模块数量',
        '开始使用时间',
        '备注',
        '填报人',
        '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list6 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家',
        '局端型号',
        '监控型号',
        '功率（KW）',
        '模块型号',
        '模块数量',
        '开始使用时间',
        '备注',
        '填报人',
        '联系电话',
    ]

    # area
    # station
    # number
    # node
    # produce
    # frame
    # monitoring
    # ktpower
    # rectification
    # renumber
    # starttime
    # desc
    # people
    # phone
    if id == '7':
        result = [[
            item.area,
            item.station,
            item.number,
            item.node,
            item.produce,
            item.frame,
            item.starttime,
            item.renumber,
            item.desc,
            item.people,
            item.phone,
        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',       
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家',
        '型号',
        '开始使用时间',
        '数量',
        '备注',
        '填报人',
        '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list7 = [
        '县市',
        '基站名称',
        '基站编码',
        '节点类型',
        '厂家',
        '型号',
        '开始使用时间',
        '数量',
        '备注',
        '填报人',
        '联系电话',
    ]
    # area
    # station
    # number
    # node
    # produce
    # frame
    # starttime
    # renumber
    # desc
    # people
    # phone
    if id == '8':
        result = [[
            item.area,
            item.ground,
            item.produce,
            item.frame,
            item.ktpower,
            item.starttime,
            item.renumber,
            item.desc,
            item.people,
            item.phone,
        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',    '县市',
        '地点',
        '厂家'
        '型号'
        '功率（KVA）'
        '开始使用时间'
        '数量',
        '备注',
        '填报人',
        '联系电话', )
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list8 = [
        '县市',
        '地点',
        '厂家'
        '型号'
        '功率（KVA）'
        '开始使用时间'
        '数量',
        '备注',
        '填报人',
        '联系电话',
    ]
    # area
    # ground
    # produce
    # frame
    # ktpower
    # starttime
    # renumber
    # desc
    # people
    # phone
    if id == '9':
        result = [[
            item.area,
            item.produce,
            item.frame,
            item.ktpower,
            item.starttime,
            item.renumber,
            item.ground,
            item.desc,
            item.people,
            item.phone,

        ] for item in data]
        filename = exprort(result, '开关电源报表', 'style4',  '县市',
        '厂家'
        '型号'
        '功率（KW）'
        '开始使用时间'
        '数量'
        '存放地点'
        '备注',
        '填报人',
        '联系电话',)
        return {
            "msg": "msg",
            "code": 0,
            "url": "192.168.188.178:86/{}".format(filename),
        }

    name_list9 = [
        '县市',
        '厂家'
        '型号'
        '功率（KW）'
        '开始使用时间'
        '数量'
        '存放地点'
        '备注',
        '填报人',
        '联系电话',
    ]
    # area
    # produce
    # frame
    # ktpower
    # starttime
    # renumber
    # ground
    # desc
    # people
    # phone


# s e  p s  area  机房  铁塔类型 基站类型
def get_statistics_tower(id, starttime='', endtime='', page=1, size=10,
                         area='', stationtype='', ttpye='', stype=''):
    print(type(id))

    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    if id == '2':
        if area != '':
            area = get_keys(area_dict, area)
        data = _filter(AXgdlTowerCount,
                       starttime=starttime,
                       endtime=endtime,
                       area=area,
                       )
        total = data.count()
        data = data.paginate(int(page), int(size))
        result = [{
            'area': item.area,
            'totle': item.totle,
            'yijiao': item.yijiao,
            'yijiaotower': item.yijiaotower,
            'yijiaojifan': item.yijiaojifan,
            'nowtower': item.nowtower,
            'noyijiao': item.noyijiao,
            'biaoyijiao': item.biaoyijiao,
            'desc': item.desc,
            'piccount': item.piccount,
            'posttime': item.posttime,

        } for item in data]
        return {"code": 0, "msg": "success", "total": total, "result": result}

    if area != '':
        area = get_keys(area_dict, area)
    if stationtype != '':
        stationtype = get_keys(jifan_dict, stationtype)
    if ttpye != '':
        ttpye = get_keys(tower_dict, ttpye)
    if stype != '':
        stype = get_keys(jizhan_dict, stype)

    data = _filter(AXgdlTower,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   stationtype=stationtype,
                   ttpye=ttpye,
                   stype=stype,
                   )
    total = data.count()
    data = data.paginate(int(page), int(size))
    # pass  # p z s e area name money  yijiao desc
    for item in data:
        print(item.station)

    result = [{
        'area': area_dict[item.area],
        'station': item.station,
        'address': item.address,
        'tnumber': item.tnumber,
        'stype': jizhan_dict[item.stype],
        'money': item.money,
        'ttpye': tower_dict[item.ttpye],
        'hight': item.hight,
        'stationtype': jifan_dict[item.stationtype],
        'transfer': item.transfer,
        'share': item.share,
        'tshare': item.tshare,
        'sharelist': item.sharelist,
        'sharenumber': item.sharenumber,
        'sharedesc': item.sharedesc,
        'elesharelist': item.elesharelist,
        'rru': item.rru,
        'antenna': item.antenna,
        'pic': item.pic,
        'reading': item.reading,
        'phone': item.phone,
        'posttime': utc_timestamp_to_str(item.posttime),
        'tsharelist': item.tsharelist,

    } for item in data]
    return {"code": 0, "msg": "success", "total": total, "result": result}


# s e  p s  area
def get_statistics_tower_export(id, starttime='', endtime='', page=1, size=10,
                                area='', stationtype='', ttpye='', stype=''):

    if area != '':
        area = get_keys(area_dict, area)
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    if id == '2':
        if area != '':
            area = get_keys(area_dict, area)
            data = _filter(AXgdlTowerCount,
                           starttime=starttime,
                           endtime=endtime,
                           area=area,
                           )
            name_list = [
                '县市',
                '站点总数',
                '全部移交',
                '移交铁塔',
                '移交机房',
                '铁塔新建站',
                '未移交',
                '备注'

            ]

            result = [[
                item.area,
                item.totle,
                item.yijiao,
                item.yijiaotower,
                item.yijiaojifan,
                item.nowtower,
                item.noyijiao,
                # item.biaoyijiao,
                item.desc,
                item.piccount,
                item.posttime,

            ] for item in data]
            filename = exprort(result, '铁塔总数报表', 'style4', '县市',
                               '站点总数',
                               '全部移交',
                               '移交铁塔',
                               '移交机房',
                               '铁塔新建站',
                               '未移交',
                               '备注')
            return {
                "msg": "msg",
                "code": 0,
                "url": "192.168.188.178:86/{}".format(filename),
            }

    if area != '':
        area = get_keys(area_dict, area)
    if stationtype != '':
        stationtype = get_keys(jifan_dict, stationtype)
    if ttpye != '':
        ttpye = get_keys(tower_dict, ttpye)
    if stype != '':
        stype = get_keys(jizhan_dict, stype)

    data = _filter(AXgdlTower,
                   starttime=starttime,
                   endtime=endtime,
                   area=area,
                   stationtype=stationtype,
                   ttpye=ttpye,
                   stype=stype,
                   )
    # total = data.count()
    # data = data.paginate(int(page), int(size))
    # pass  # p z s e area name money  yijiao desc
    result = [[

        #     'area':
        #             'station': item.station,
        # 'address': item.address,
        # 'tnumber': item.tnumber,
        # 'stype':
        # 'money': item.money,
        # 'ttpye':
        # 'hight': item.hight,
        # 'stationtype':
        area_dict[item.area],
        item.station,
        item.address,
        item.tnumber,
        jizhan_dict[item.stype],
        item.money,
        tower_dict[item.ttpye],
        item.hight,
        jifan_dict[item.stationtype],
        item.transfer,
        item.share,
        item.tshare,
        item.tsharelist,
        item.sharenumber,
        item.sharelist,
        item.sharedesc,
        item.elesharelist,
        item.rru,
        item.antenna,
        item.pic,
        # item.reading,   导出不用抄表人和联系方式
        # item.phone,
        utc_timestamp_to_str(item.posttime),

    ] for item in data]
    name_list = ['县市', '基站名称', '详细地点描述', '公司编码',
                 '基站类型', '是否支付', '铁塔类型', '铁塔高度',
                 '机房类型', '移交类型', '是否共享', '铁塔共享用户数',
                 '铁塔共享清单', '机房共享用户数', '机房共享清单', '电表共享情况',
                 '电表共享清单', 'RRU', '天线数量', '照片', '日期', ]
    filename = exprort(result, '铁塔报表', 'style4', '县市', '基站名称', '详细地点描述', '公司编码',
                       '基站类型', '是否支付', '铁塔类型', '铁塔高度',
                       '机房类型', '移交类型', '是否共享', '铁塔共享用户数',
                       '铁塔共享清单', '机房共享用户数', '机房共享清单', '电表共享情况',
                       '电表共享清单', 'RRU', '天线数量', '照片', '日期', )
    return {
        "msg": "msg",
        "code": 0,
        "url": "192.168.188.178:86/{}".format(filename),
    }


# area rank station tower gtype transfer
def get_statistics_clean(starttime='', endtime='', page=1, size=10,
                         area='', rank='', station=''
                         , tower='', gtype='', transfer=''):
    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    if area != '':
        area = get_keys(area_dict, area)
    if rank != '':
        rank = get_keys(rank_dict, rank)
    if station != '':
        jifan = get_keys(jifan_dict, station)
    else:
        jifan = ''
    if tower != '':
        tower = get_keys(tower_dict, tower)
    if gtype != '':
        jizhan = get_keys(jizhan_dict, gtype)
    else:
        jizhan = ''
    if transfer != '':
        transfer = get_keys(transfer_dict, transfer)

    data = _filter(AXgdlClean, area=area, rank=rank, jifan=jifan,
                   tower=tower, jizhan=jizhan, transfer=transfer,
                   starttime=starttime, endtime=endtime)
    total = data.count()
    # jia area
    data = data.paginate(int(page), int(size))

    result = [{
        'name': item.name,
        'number': item.number,
        'address': item.address,
        'rank': rank_dict[item.rank],
        'jifan': jifan_dict[item.jifan],
        'tower': tower_dict[item.tower],
        'height': item.height,
        'jizhan': jizhan_dict[item.jizhan],
        'transfer': transfer_dict[item.transfer],
        'share': share_dict[item.share],
        'area': area_dict[item.area]
    } for item in data]

    return {"code": 0, "msg": "success", "total": total, "result": result}


def get_statistics_clean_export(starttime='', endtime='', page=1, size=10,
                                area='', rank='', station=''
                                , tower='', gtype='', transfer=''):

    if endtime != '':
        endtime = endtime + ' 00:00:00'
    if starttime != '':
        starttime = starttime + ' 00:00:00'
    if area != '':
        area = get_keys(area_dict, area)
    if rank != '':
        rank = get_keys(rank_dict, rank)
    if station != '':
        jifan = get_keys(jifan_dict, station)
    else:
        jifan = ''
    if tower != '':
        tower = get_keys(tower_dict, tower)
    if gtype != '':
        jizhan = get_keys(jizhan_dict, gtype)
    else:
        jizhan = ''
    if transfer != '':
        transfer = get_keys(transfer_dict, transfer)

    data = _filter(AXgdlClean, area=area, rank=rank, jifan=jifan,
                   tower=tower, jizhan=jizhan, transfer=transfer,
                   starttime=starttime, endtime=endtime)
    name_list = ['县市', '基站名称', '基站编号', '详细地点描述', '维护级别'
        , '机房类型', '铁塔类型', '铁塔高度', '基站类型', '是否移交', '共享家数']
    result = [[
        area_dict[item.area],
        item.name,
        item.number,
        item.address,
        rank_dict[item.rank],
        jifan_dict[item.jifan],
        tower_dict[item.tower],
        item.height,
        jizhan_dict[item.jizhan],
        transfer_dict[item.transfer],
        share_dict[item.share],

    ] for item in data]

    filename = exprort(result, '基站清理报表', 'style4', '区县', '基站名称', '基站编号', '详细地点描述', '维护级别'
                       , '机房类型', '铁塔类型', '铁塔高度', '基站类型', '是否移交', '共享家数')
    return {
        "msg": "msg",
        "code": 0,
        "url": "192.168.188.178:86/{}".format(filename),
    }
    # name
    # number
    # address
    # rank
    # jifan
    # tower
    # height
    # jizhan
    # transfer
    # share


# def get_statistics_chart():
#     pass
#
# def get_statistics_chart_export():
#     pass



def one_filter(data, db, k, val):
    date = data
    if val != None and val != '':
        print(db)

        # AXgdlEquipment,
        # starttime = starttime,
        # endtime = endtime,
        # id = id,
        # area = area,
        # station = station,
        # ground = ground,
        # produce = produce,
        # frame = frame,
        # cap = cap,
        # transmission = transmission,
        # ifmonitoring = ifmonitoring,
        # ktpower = ktpower,
        # kttype = kttype,
        # peoplep = people,

        if db == AXgdlEquipment:
            if k == 'starttime':
                starttime = utc_str_to_timestamp(val)
                data = date.where(starttime <= db.posttime)
            if k == 'endtime':
                endtime = utc_str_to_timestamp(val)
                data = date.where(db.posttime <= endtime)
            if k == 'id':
                data = date.where(db.type == val)
            if k == 'area':
                data = date.where(db.area == val)
            if k == 'station':
                data = date.where(db.station == val)
            if k == 'ground':
                data = date.where(db.ground == val)
            if k == 'produce':
                data = date.where(db.produce == val)
            if k == 'frame':
                data = date.where(db.frame == val)
            if k == 'cap':
                data = date.where(db.cap == val)
            if k == 'transmission':
                data = date.where(db.transmission == val)
            if k == 'ifmonitoring':
                data = date.where(db.ifmonitoring == val)
            if k == 'ktpower':
                data = date.where(db.ktpower == val)
            if k == 'peoplep':
                data = date.where(db.peoplep == val)
            if k == 'kttype':
                data = date.where(db.kttype == val)

        if db == AXgdlTower:
            print('keyijinru')
            if k == 'stationtype':
                data = date.where(db.stationtype == val)
            if k == 'ttype':
                data = date.where(db.ttype == val)
            if k == 'stype':
                data = date.where(db.stype == val)
            if k == 'starttime':
                starttime = utc_str_to_timestamp(val)
                data = date.where(starttime <= db.posttime)
            if k == 'endtime':
                endtime = utc_str_to_timestamp(val)
                data = date.where(db.posttime <= endtime)
            if k == 'area':
                try:
                    data = date.where(db.area == val)
                except:
                    data = date.where(db.address == val)

        # data = _filter(AXgdlTower,
        #                starttime=starttime,
        #                endtime=endtime,
        #                area=area,
        #                stationtype=stationtype,
        #                ttpye=ttpye,
        #                stype=stype,
        #                )
        if db == AXgdlInspect:
            print('keyijinru')
            if k == 'tower':
                data = date.where(db.tower == val)
            if k == 'starttime':
                starttime = utc_str_to_timestamp(val)
                data = date.where(starttime <= db.posttime)
            if k == 'endtime':
                endtime = utc_str_to_timestamp(val)
                data = date.where(db.posttime <= endtime)
            if k == 'area':
                try:
                    data = date.where(db.area == val)
                except:
                    data = date.where(db.address == val)
            if k == 'station':
                data = date.where(db.station == val)

            if k == 'type':
                data = date.where(db.type == val)




        else:
            if k == 'starttime':
                starttime = utc_str_to_timestamp(val)
                data = date.where(starttime <= db.posttime)
            if k == 'endtime':
                endtime = utc_str_to_timestamp(val)
                data = date.where(db.posttime <= endtime)
            if k == 'name':
                data = date.where(db.name == val)
            if k == 'area':
                try:
                    data = date.where(db.area == val)
                except:
                    data = date.where(db.address == val)

            if k == 'jifan':
                data = date.where(db.jifan == val)
            if k == 'jizhan':
                data = date.where(db.jizhan == val)

            if k == 'rank':
                data = date.where(db.rank == val)
            if k == 'station':
                try:
                    data = date.where(db.station == val)
                except:
                    data = date.where(db.jifan == val)
            if k == 'tower':
                data = date.where(db.tower == val)
            if k == 'gtype':
                data = date.where(db.jizhan == val)
            if k == 'transfer':
                data = date.where(db.transfer == val)
        print(data.count())
        return data


def _filter(db, **kw):
    date = db.select()
    for k, val in kw.items():
        if val != None and val != '':
            date = one_filter(date, db, k, val)
            print(date.count())
    num = 0
    for val in kw.values():
        if val == None or val == '':
            num += 1
    if num == len(kw):
        date = db.select()
    return date


def utc_str_to_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return (int(timestamp))


def utc_timestamp_to_str(dt):
    # 时间戳变成字符串
    timeArray = time.localtime(dt)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def get_keys(d, value):
    a = [k for k, v in d.items() if v == value]
    return a[0]


def exprort(data, name, style, *args):
    workbook_m = xlwt.Workbook(encoding='utf-8')
    xlsheet = workbook_m.add_sheet(name, cell_overwrite_ok=True)
    # 格式1 （有自动换行）
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour white')
    style1.font.height = 200
    style1.font.name = u'文泉驿点阵正黑'
    style1.font.colour_index = 0
    style1.borders.left = xlwt.Borders.THIN
    style1.borders.right = xlwt.Borders.THIN
    style1.borders.top = xlwt.Borders.THIN
    style1.borders.bottom = xlwt.Borders.THIN
    # style1.font.bold = True
    style1.alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style1.alignment.horz = xlwt.Alignment.HORZ_CENTER

    # 格式2  （没有自动换行）
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour white')
    style2.font.height = 200
    style2.font.name = u'文泉驿点阵正黑'
    style2.font.colour_index = 0
    style2.borders.left = xlwt.Borders.THIN
    style2.borders.right = xlwt.Borders.THIN
    style2.borders.top = xlwt.Borders.THIN
    style2.borders.bottom = xlwt.Borders.THIN
    # style2.font.bold = True
    # style2.alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    # style2.alignment.horz = xlwt.Alignment.HORZ_CENTER

    # 格式3 黄色背景色
    style3 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow')
    style3.font.height = 200
    style3.font.name = u'文泉驿点阵正黑'
    style3.font.colour_index = 0
    # style3.borders.left = xlwt.Borders.THIN
    # style3.borders.right = xlwt.Borders.THIN
    # style3.borders.top = xlwt.Borders.THIN
    # style3.borders.bottom = xlwt.Borders.THIN

    # style4 格式4 0.00%
    style4 = xlwt.easyxf('pattern: pattern solid, fore_colour white')
    style4.font.height = 200
    style4.font.name = u'文泉驿点阵正黑'
    style4.font.colour_index = 0
    style4.borders.left = xlwt.Borders.THIN
    style4.borders.right = xlwt.Borders.THIN
    style4.borders.top = xlwt.Borders.THIN
    style4.borders.bottom = xlwt.Borders.THIN
    # style4.font.bold = True
    style4.alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style4.alignment.horz = xlwt.Alignment.HORZ_CENTER
    style4.num_format_str = '0.00%'

    # style2.font.bold = True
    # style2.alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    # style2.alignment.horz = xlwt.Alignment.HORZ_CENTER
    # 写excel表头
    # 设置单元格
    style_dict = {
        'style1': style1,
        'style2': style2,
        'style3': style3,
        'style4': style4,
    }
    for i, val in enumerate(args):
        xlsheet.write(0, i, val, style_dict[style])

    number = 0
    for item in data:
        number += 1
        for j, val in enumerate(item):
            xlsheet.write(number, j, val)
            # for j in range(0,len(item)):
            #     xlsheet.write(number, j, item['j'])
    xlsname = name + str(int(time.time()))
    workbook_m.save('/var/www/downfile/xiaogan/{}.xls'.format(xlsname))
    return xlsname+'.xls'


    # data = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'],
    #         ['a', 'b', 'c', 'd']]
    #
    # exprort(data, 'text', 'style4', 'A', 'B', 'C', 'D')
