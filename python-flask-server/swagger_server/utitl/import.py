import time
from datetime import datetime

import xlrd
from xlrd import xldate_as_tuple

from swagger_server.controllers.xgdl_statistics import get_keys
from swagger_server.utitl.all_dict import area_dict
from swagger_server.utitl.db import AXgdlEquipment, AXgdlTowerCount


# ground 代替地点和存放地点
# renumber  代替了数字
# ktpower 代替功率

def inventory_val2():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(0)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[23]
        posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=2,  # 设备类型                    type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],  # 节点类型                     node='基站'
            ground=row_data[5],  # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
            produce=row_data[18],  # 生产厂家                    produce=row_data[7]
            frame=row_data[19],  # 机架型号                    frame
            cap=row_data[20],  # 机架容量
            #                     cap
            starttime=posttime,  # 开始使用时间
            #                 starttime
            loadele=row_data[
                24],  # 负载电流                    loadele=row_data[3]
            oil=row_data[
                27],  # 是否固定启动油机（1,是。。。2否）                    oil
            desc=row_data[
                28],  # 备注                    desc
            people=row_data[
                29],  # people
            phone=
            row_data[30],  # phone
            tid=2,
            # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
            group=row_data[21],  # group
            ifmonitoring=row_data[22],  # ifmonitoring
            hbtime=row_data[25],  # hbtime
            ifpowerdown=row_data[26],  # ifpowerdown
            posttime=int(
                time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val1():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(0)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[9]
        posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=1,  # 设备类型
            tid=1,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],  # 节点类型                     node='基站'
            ground=row_data[5],  # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
            produce=row_data[6],  # 生产厂家                    produce=row_data[7]
            frame=row_data[7],  # 机架型号                    frame
            cap=row_data[8],  # 机架容量                    cap
            starttime=posttime,  # 开始使用时间                    starttime
            monitoring=row_data[10],  # 监控模块型号                    monitoring
            rectification=row_data[
                11],  # 整流模块型号                    rectification =row_data[0]
            renumber=row_data[
                12],  # 整流模块数量                    renumber=row_data[1],
            modulecap=row_data[
                13],  # 模块容量                    modulecap=row_data[2]
            loadele=row_data[
                14],  # 负载电流                    loadele=row_data[3]
            transmission=row_data[
                15],  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
            powerdown=
            row_data[16],  # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
            ifstatus=row_data[17],  # ifstatus=row_data[6]
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val3():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(1)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[9]
        posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=3,  # 设备类型
            tid=3,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],  # 节点类型                     node='基站'
            produce=row_data[5],  # 生产厂家
            frame=row_data[6],  # produce=row_data[7]
            starttime=posttime,  # 开始使用时间                    starttime
            desc=row_data[10],  # 备注                    desc
            people=row_data[11],  # people
            phone=row_data[12],  # phone
            kttype=row_data[8],  # 空调类型                    kttype
            ktpower=row_data[7],  # ktpower
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val4():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(2)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[8]
        posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=4,  # 设备类型
            tid=4,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],  # 节点类型                     node='基站'
            produce=row_data[5],  # 生产厂家
            frame=row_data[6],  # produce=row_data[7]
            starttime=posttime,  # 开始使用时间                    starttime
            renumber=row_data[7],
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val5():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(3)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[7]
        try:
            posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        except:
            posttime = ''
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=5,  # 设备类型
            tid=5,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            produce=row_data[4],  # 生产厂家
            frame=row_data[5],  # produce=row_data[7]
            starttime=posttime,  # 开始使用时间                    starttime
            renumber=row_data[6],
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val6():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(4)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[11]
        try:
            posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        except:
            posttime = ''
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=6,  # 设备类型
            tid=6,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],
            produce=row_data[5],  # 生产厂家
            frame=row_data[6],  # produce=row_data[7]

            monitoring=row_data[7],
            ktpower=row_data[8],

            rectification=row_data[9],  # 整流模块型号                    rectification =row_data[0]
            renumber=row_data[10],
            starttime=posttime,  # 开始使用时间                    starttime
            desc=row_data[12],
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def inventory_val7():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(5)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(4, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[8]
        try:
            posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        except:
            posttime = ''
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=7,  # 设备类型
            tid=7,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2
            station=row_data[2],  # 基站名称                    station='基站2'
            number=row_data[3],  # 基站编码                    number='no2'
            node=row_data[4],
            produce=row_data[5],  # 生产厂家
            brand =row_data[6],
            frame=row_data[7],  # produce=row_data[7]
            renumber=row_data[9],
            starttime=posttime,  # 开始使用时间                    starttime
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''

def inventory_val8():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(6)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(3, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[7]
        try:
            posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        except:
            posttime = ''
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=8,  # 设备类型
            tid=8,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2

            ground=row_data[2],
            produce=row_data[3],  # 生产厂家
            brand =row_data[4],
            frame=row_data[5],  # produce=row_data[7]
            ktpower=row_data[6],
            renumber=row_data[8],
            starttime=posttime,  # 开始使用时间                    starttime
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''

def inventory_val9():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    print(data)

    sheet1 = data.sheet_by_index(7)
    nrows = sheet1.nrows
    print(nrows)
    for i in range(3, 14):
        row_data = sheet1.row_values(i)
        posttime = row_data[6]
        try:
            posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        except:
            posttime = ''
        print(posttime)

        print(row_data)

        ax = AXgdlEquipment()
        ax.create(
            type=9,  # 设备类型
            tid=9,  # type=2
            area=get_keys(area_dict, row_data[1]),  # 县市（安陆，云梦....）                    area=2

            produce=row_data[2],  # 生产厂家
            brand =row_data[3],
            frame=row_data[4],  # produce=row_data[7]
            ktpower=row_data[5],
            renumber=row_data[7],
            starttime=posttime,  # 开始使用时间
            ground =row_data[8],    #               starttime
            posttime=int(time.time()),  # 发送时间                    posttime
        )

        '''
            #                    id
            type=2         # 设备类型                    type=2
        area = 2             # 县市（安陆，云梦....）                    area=2
        station = '基站2'    # 基站名称                    station='基站2'
        number = 'no2'         # 基站编码                    number='no2'
        node = '基站'         # 节点类型                     node='基站'
        ground = '1城区'        # 地理位置 (1城区 ，0乡镇)                    ground='1城区'
        produce = row_data[7]    # 生产厂家                    produce=row_data[7]
        frame = row_data[8] # 机架型号                    frame
        cap = row_data[9] # 机架容量                    cap
        starttime = row_data[12] # 开始使用时间                    starttime
        monitoring  # 监控模块型号                    monitoring
        rectification =   # 整流模块型号                    rectification =row_data[0]
        renumber = ,  # 整流模块数量                    renumber=row_data[1],
                   modulecap = ] # 模块容量                    modulecap=row_data[2]
        loadele = = row_data[13]  # 负载电流                    loadele=row_data[3]
        transmission =  # 传输及基站是否公共（1.是，，，2否）                    transmission=row_data[4]
        powerdown =   # 二次下电（1,是。。。2否）                    powerdown=row_data[5]
        oil = row_data[16] # 是否固定启动油机（1,是。。。2否）                    oil
        pic  # 图片地址                    pic
        desc = row_data[17] # 备注                    desc
        people = row_data[18] # people
        phone = row_data[19] # phone
        tid = 2  # 设备类型id (1.开关电源   2.蓄电池  3. 空调  4.交配配电箱  5.拉远站 6 .直流远供局端 7.一体化机柜 8 变压器 9 应急油机 10.铁塔)                    tid=1
        group = row_data[10] # group
        brand  # brand
        changebox  # 交换机                    changebox
        jifang  # 机房                    jifang
        kttype  # 空调类型                    kttype
        ktpower  # ktpower
        ifmonitoring = row_data[11] # ifmonitoring
        hbtime = row_data[14] # hbtime
        iftransmission  # iftransmission
        ifpowerdown = row_data[15] # ifpowerdown
        ifstatus =   # ifstatus=row_data[6]
        xuhao  # 序号                    xuhao
        posttime  # 发送时间                    posttime
        '''


def tower_count():
    data = xlrd.open_workbook('/var/www/downfile/附件3：铁塔服务费疑点基站基础数据清理.xls')
    print(data)

    sheet1 = data.sheet_by_index(0)
    # nrows = sheet1.nrows
    # print(nrows)
    for i in range(1, 14):
        row_data = sheet1.row_values(i)
        # posttime = row_data[6]
        # try:
        #     posttime = str(datetime(*xldate_as_tuple(posttime, 0)))
        # except:
        #     posttime = ''
        # print(posttime)
        #
        print(row_data)

        ax = AXgdlTowerCount()
        ax.create(

        area=get_keys(area_dict,row_data[0]),
        totle=row_data[1],
        yijiao=row_data[2],
        yijiaotower=row_data[3],
        yijiaojifan=row_data[4],
        nowtower=row_data[5],
        noyijiao=row_data[6],
        biaoyijiao=row_data[7],
        desc=row_data[8],
        piccount=row_data[9],


        posttime=int(time.time()),  # 发送时间                    posttime
        )



if __name__ == '__main__':
    tower_count()
