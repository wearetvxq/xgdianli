# -*- coding: UTF-8 -*-
import connexion
from datetime import date, datetime
from typing import List, Dict

import re
from six import iteritems

from swagger_server.controllers.xgdl_statistics import utc_str_to_timestamp
from swagger_server.utitl.all_dict import *
from swagger_server.utitl.db import *
from swagger_server.utitl.db import AXgdlClean, AXgdlReading
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from flask import json, jsonify
from flask import Response, request
from swagger_server.utitl.excleutil import ExcleUtil1

import os, sys
import time
# import math
import socket
import random
import tarfile
import zipfile
import datetime
import os
from multiprocessing import Process, Queue, Array, RLock
import multiprocessing

def get_keys(d, value):
    a = [k for k, v in d.items() if v == value]
    return a[0]


# 目前两个都要加入基站  area 三个接口都加入 x  y  code
# noinspection PyStatementEffect
def post_phone_reading(
        station='',
        last='',
        meter='',
        now='',
        percentage='',
        reason='',
        pic='',
        x_code='',
        y_code='',
        dianbiao_id=''):
    '''
    station *  基站名称
    last * 上月日均耗电量
    meter *  示数
    now *  本月
    percentage *   耗电比
    reason *  原因
    pic *图片url
    '''

    # 有id  还要根据dianbiao_id 得到area 并且进行转码
    try:
        # posttime=int(time.time())-5
        # count=AXgdlReading.select().where(AXgdlReading.posttime )
        area=XgAmmeter.select().where(XgAmmeter.id==dianbiao_id).get().area
        number=XgAmmeter.select().where(XgAmmeter.id==dianbiao_id).get().number
        last = last.replace('kWh', '')
        print(x_code)
        print(y_code)
        AXgdlReading.insert(
            compare=percentage,
            desc=reason,
            last=last,
            meter=meter,
            name=station,
            now=now,
            pic=pic,
            pid=1,
            x_code=x_code,
            y_code=y_code,
            posttime=int(time.time()),
            dianbiao_id=dianbiao_id,
            area=get_keys(area_dict,area),
            number=number
        ).execute()
        return {"code": 0, "msg": 'success'}
    except Exception as e:
        print(e)
        return {"code": -1, "msg": "error"}


def post_phone_clean(pic, number, station, synergy,
                     address, rank, jifang, tieta, jizhan, height, transfer, shared
                     ):
    '''
    pic * 图片url
    number *  编号
    station *  基站名称
    synergy *  综资名称
    address *   地址
    rank *  维护级别
    jifang *   机房类型
    tieta *  铁塔类型
    jizhan *  基站类型
    height *  铁塔高度
    transfer * 是否移交
    shared *  共享家数
    # '''
    try:
        # a = get_keys(rank_dict, '普通')
        # print(type(a))
        # rank = get_keys(rank_dict,rank)
        # print(type(rank))
        # print(rank[0])
        # print(type(rank))
        # print(int(rank))
        # jifan = get_keys(jifan_dict, jifang),
        # tower = get_keys(tower_dict, tieta),
        # jizhan = get_keys(jizhan_dict, jizhan),
        # transfer = get_keys(transfer_dict, transfer),
        # share = get_keys(share_dict, shared),
        print(number)
        area = XgAmmeter.select().where(XgAmmeter.name == station).get().area
        axgdlclean = AXgdlClean()
        axgdlclean.create(
#还是缺area
            #     'rank': rank_dict[item.rank],
            # 'jifan': jifan_dict[item.jifan],
            # 'tower': tower_dict[item.tower],
            # 'height': item.height,
            # 'jizhan': jizhan_dict[item.jizhan],
            # 'transfer': transfer_dict[item.transfer],
            # 'share': share_dict[item.share],
            # 'area': area_dict[item.area]
            name=station,
            number=number,
            capital=synergy,
            address=address,
            rank=get_keys(rank_dict,rank),
            jifan=get_keys(jifan_dict,jifang),
            tower= get_keys(tower_dict,tieta),
            jizhan= get_keys(jizhan_dict,jizhan),
            height=height,
            transfer=get_keys(transfer_dict,transfer),
            share=get_keys(share_dict,shared),
            pic=pic,
            pid=1,
            area=get_keys(area_dict,area) ,
            posttime=int(time.time())
        )
        return {"code": 0, "msg": 'success'}
    except Exception as e:
        print(e)
        return {"code": "-1", "msg": "error"}


def post_phone_equipment(
        type='',
        area='',
        station='',
        number='',
        node='',
        ground='',
        produce='',
        frame='',
        cap='',
        starttime='',
        monitoring='',
        rectification='',
        renumber='',
        modulecap='',
        loadele='',
        transmission='',
        powerdown='',
        oil='',
        pic='',
        desc='',
        people='',
        phone='',
        tid='',
        group='',
        brand='',
        changebox='',
        jifang='',
        kttype='',
        ktpower='',
        ifmonitoring='',
        hbtime='',
        iftransmission='',
        ifpowerdown='',
        ifstatus='',
        xuhao='', ):
    try:
        if type == '10':
            axgdltower = AXgdlTower()
            axgdltower.create(

            )

        else:
            print(type)
            type=int(type)
            tid=type
            axgdlequipment = AXgdlEquipment()
            axgdlequipment.create(
                type=type,
                area=area,
                station=station,
                number=number,
                node=node,
                ground=ground,
                produce=produce,
                frame=frame,
                cap=cap,
                starttime=starttime,
                monitoring=monitoring,
                rectification=rectification,
                renumber=renumber,
                modulecap=modulecap,
                loadele=loadele,
                transmission=transmission,
                powerdown=powerdown,
                oil=oil,
                pic=pic,
                desc=desc,
                people=people,
                phone=phone,
                tid=tid,
                group=group,
                brand=brand,
                changebox=changebox,
                jifang=jifang,
                kttype=kttype,
                ktpower=ktpower,
                ifmonitoring=ifmonitoring,
                hbtime=hbtime,
                iftransmission=iftransmission,
                ifpowerdown=ifpowerdown,
                ifstatus=ifstatus,
                xuhao=xuhao,
                posttime=int(time.time())
            )
        return {"code": 0, "msg": 'success'}
    except Exception as e:
        print(e)
        return {"code": "-1", "msg": "error"}


# 图片上传 返回图片接口
def post_phone_up(files):
    try:
        file = request.files["files"]
        file.save(os.path.join('/var/www/downfile/xiaogan', file.filename))
        return {"code": 0, "msg": "success", "url": "192.168.188.178:86/xiaogan/{}".format(file.filename)}
    except Exception as e:
        print(e)
        return {"code": -1, "msg": "Error"}


def post_phone_tower(area='',
                     station='',
                     address='',
                     tnumber='',
                     stype='',
                     money='',
                     ttpye='',
                     hight='',
                     stationtype='',
                     transfer='',
                     share='',
                     tshare='',
                     tsharelist='',
                     sharelist='',
                     sharenumber='',
                     sharedesc='',
                     elesharelist='',
                     rru='',
                     antenna='',
                     pic='',
                     reading='',
                     phone='',
                     ):
    try:
        axgdltower = AXgdlTower()
        print(area)
        print(stype)
        print(ttpye)
        print(stationtype)
        axgdltower.create(
            area=get_keys(area_dict, area),
            station=station,
            address=address,
            tnumber=tnumber,
            stype=get_keys(jizhan_dict, stype),
            money=money,
            ttpye=get_keys(tower_dict, ttpye),
            hight=hight,
            stationtype=get_keys(jifan_dict, stationtype),
            transfer=transfer,
            share=share,
            tshare=tshare,
            tsharelist=tsharelist,
            sharelist=sharelist,
            sharenumber=sharenumber,
            sharedesc=sharedesc,
            elesharelist=elesharelist,
            rru=rru,
            antenna=antenna,
            pic=pic,
            reading=reading,
            phone=phone,
            posttime=int(time.time())
        )
        return {"code": 0, "msg": 'success'}
    except Exception as e:
        print(e)
        return {"code": "-1", "msg": "error"}


def get_phone_code(x_code='', y_code='', name='', code='', bh=''):  # 站点名称  dianbiao_id 传  接收
    # data=AXgdlReading.select().where(AXgdlReading.x_code==x_code,AXgdlReading.y_code==y_code).get()
    # if data:
    #     name=data.stition
    #     last=data,last
    address = ''
    address2 = ''
    number = ''
    area = XgAmmeter.select().where(XgAmmeter.name == name).get().area
    number = XgAmmeter.select().where(XgAmmeter.name == name).get().number
    if bh != '':
        data = XgAmmeter.select().where(XgAmmeter.usercode == code,
                                        XgAmmeter.biaohao == bh,
                                        XgAmmeter.status=='运行',
                                        XgAmmeter.name==name).get()
        if data.y_code:
            y = data.y_code
        else:
            return {"code":10003,"msg":"未找到该站点坐标"}
        if data.x_code:
            x = data.x_code
        else:
            return {"code": 10003, "msg": "未找到该站点坐标"}
        if abs(float(y) - float(y_code)) + abs(float(x) - float(x_code)) <= 0.02:
            try:
                fstarttime = utc_str_to_timestamp(get_f_l_day()[0])
                fendtime = utc_str_to_timestamp(get_f_l_day()[1])
                data2 = AXgdlReading.select().where(
                    AXgdlReading.posttime >= fstarttime,
                    AXgdlReading.posttime <= fendtime,
                    AXgdlReading.dianbiao_id == data.id
                ).get()
                days = (fendtime - fstarttime) / 86400
                last = '%.2f' % (float(data2.now) / days)
                dianbiao_id = data.id
                area = data.area

            except Exception as e:
                print(e)
                return {"code": 10003, "msg": "核算上月耗电量出错"}
        else:
            return {"code": -1, "msg": "请靠近站点重新扫码"}
    else:
        data = XgAmmeter.select().where(
                                        XgAmmeter.status == '运行',
                                        XgAmmeter.name == name).get()
        if data.y_code:
            y = data.y_code
        else:
            return {"code": 10003, "msg": "未找到该站点坐标"}
        if data.x_code:
            x = data.x_code
        else:
            return {"code": 10003, "msg": "未找到该站点坐标"}
        if abs(float(y) - float(y_code)) + abs(float(x) - float(x_code)) <= 0.02:
            number = data.number
            name = data.name
            address=data.address
            address2=name
            area=data.area

        dianbiao_id = ''
        last = ''
    return {"code": 0, "msg": "success", "station": name,"area":area ,
            'number':number,"address2":address2,
            'address' :address,
            "last": last, "dianbiao_id": dianbiao_id}


def tofloat(num):
    last = num.replace('kWh', '')
    last = '%.2f' % float(last)
    return last


import datetime


# 获取上个月的时间
def get_f_l_day():
    # 上一个月的第一天
    lst_fist = str(datetime.date(datetime.date.today().year, datetime.date.today().month - 1, 1)) + ' 00:00:00'
    # 上一个月的最后一天
    lst_last = str(
        datetime.date(datetime.date.today().year, datetime.date.today().month, 1) - datetime.timedelta(1)) + ' 23:59:59'
    return (lst_fist, lst_last)


# 获取当月的时间
def get_f_l_day_now():
    # 本月的第一天
    lst_fist = str(datetime.date(datetime.date.today().year, datetime.date.today().month, 1)) + ' 00:00:00'
    # 本月的最后一天
    lst_last = str(datetime.date(datetime.date.today().year, datetime.date.today().month + 1, 1) - datetime.timedelta(
        1)) + ' 23:59:59'
    return (lst_fist, lst_last)
