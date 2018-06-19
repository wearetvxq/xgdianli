import json
import random
import time

import requests
import xlrd
from peewee import *

from swagger_server.utitl.all_dict import if_dict, area_dict

database = MySQLDatabase('xgyd', **{'user': 'root', 'use_unicode': True, 'charset': 'utf8', 'host': '39.108.165.149',
                                    'port': 3306, 'password': 'lcj123456'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class AXgdlClean(BaseModel):
    posttime = IntegerField(null=True)
    address = CharField()
    capital = CharField()
    height = FloatField()
    jifan = IntegerField()
    jizhan = IntegerField(null=True)
    name = CharField()
    number = CharField()
    pic = CharField()
    pid = IntegerField(null=True)
    rank = IntegerField()
    share = IntegerField()
    tower = IntegerField()
    transfer = IntegerField()
    area = IntegerField()

    class Meta:
        table_name = 'a_xgdl_clean'


class AXgdlEquipment(BaseModel):
    posttime = IntegerField(null=True)
    area = CharField(null=True)
    brand = CharField(null=True)
    cap = CharField(null=True)
    changebox = CharField(null=True)
    desc = CharField(null=True)
    frame = CharField(null=True)
    ground = CharField(null=True)
    group = CharField(null=True)
    hbtime = CharField(null=True)
    ifmonitoring = CharField(null=True)
    ifpowerdown = CharField(null=True)
    ifstatus = CharField(null=True)
    iftransmission = CharField(null=True)
    jifang = CharField(null=True)
    ktpower = CharField(null=True)
    kttype = CharField(null=True)
    loadele = CharField(null=True)
    modulecap = CharField(null=True)
    monitoring = CharField(null=True)
    node = CharField(null=True)
    number = CharField()
    oil = CharField(null=True)
    people = CharField(null=True)
    phone = CharField(null=True)
    pic = CharField(null=True)
    powerdown = CharField(null=True)
    produce = CharField(null=True)
    rectification = CharField(null=True)
    renumber = CharField(null=True)
    starttime = CharField(null=True)
    station = CharField()
    tid = IntegerField()
    transmission = CharField(null=True)
    type = IntegerField()
    xuhao = CharField(null=True)

    class Meta:
        table_name = 'a_xgdl_equipment'


class AXgdlInspect(BaseModel):
    area = IntegerField()
    company = CharField()
    desc = CharField()
    inspect = IntegerField()
    month = CharField()
    posttime = IntegerField()
    rank = IntegerField()
    station = CharField()
    tower = CharField()
    type = CharField()

    class Meta:
        table_name = 'a_xgdl_inspect'


class AXgdlReading(BaseModel):
    compare = CharField()
    desc = CharField(null=True)
    last = CharField()
    meter = CharField()
    name = CharField()
    now = CharField()
    pic = CharField()
    pid = IntegerField(null=True)
    posttime = IntegerField(null=True)
    number = CharField()
    x_code = CharField()
    y_code = CharField()
    area = IntegerField()
    dianbiao_id = IntegerField()

    class Meta:
        table_name = 'a_xgdl_reading'

class AXgdlTowerCount(BaseModel):
    area = IntegerField(null=True)
    biaoyijiao = IntegerField(null=True)
    desc = TextField(null=True)
    nowtower = IntegerField(null=True)
    noyijiao = IntegerField(null=True)
    piccount = IntegerField(null=True)
    totle = IntegerField(null=True)
    yijiao = IntegerField(null=True)
    yijiaojifan = IntegerField(null=True)
    yijiaotower = IntegerField(null=True)
    posttime =IntegerField(null=True)

    class Meta:
        table_name = 'a_xgdl_tower_count'

class XgAmmeter(BaseModel):
    address = CharField(null=True)
    area = CharField(null=True)
    biaohao = CharField(null=True)
    btype = CharField(null=True)
    city = CharField(null=True)
    daishou = CharField(null=True)
    gongsi = CharField(null=True)
    huming = CharField(null=True)
    max = CharField(null=True)
    name = CharField(null=True)
    num = CharField(null=True)
    number = CharField(null=True)
    rate = CharField(null=True)
    status = CharField(null=True)
    times = CharField(null=True)
    type = CharField(null=True)
    usercode = CharField(null=True)
    x_code = CharField(null=True)
    y_code = CharField(null=True)

    class Meta:
        table_name = 'xg_ammeter'


class AXgdlTower(BaseModel):
    posttime = IntegerField(null=True)
    address = CharField()
    antenna = CharField()
    area = IntegerField()
    elesharelist = CharField()
    hight = CharField()
    money = CharField()
    phone = CharField()
    pic = CharField()
    reading = CharField()
    rru = CharField()
    share = CharField()
    sharedesc = CharField()
    sharelist = CharField()
    sharenumber = CharField()
    station = CharField()
    stationtype = IntegerField()
    stype = IntegerField()
    tnumber = CharField()
    transfer = CharField()
    tshare = CharField()
    ttpye = IntegerField()
    tsharelist = CharField()

    class Meta:
        table_name = 'a_xgdl_tower'


import time


def get_keys(d, value):
    a = [k for k, v in d.items() if v == value]
    return a[0]


def inspect_val():
    data = xlrd.open_workbook('/var/www/downfile/附件1：巡检站点统计.xlsx')
    sheet1 = data.sheet_by_index(0)
    nrows = sheet1.nrows

    for i in range(1, nrows):
        row_data = sheet1.row_values(i)
        ax = AXgdlInspect()
        ax.create(
            posttime=int(time.time()),
            company=row_data[1],
            area=get_keys(area_dict, row_data[2]),
            station=row_data[3],
            desc=row_data[4],
            type=row_data[5],
            inspect=get_keys(if_dict, row_data[9]),
            month='5',
            tower=row_data[6],
            rank=get_keys(if_dict, row_data[8])

        )
        print(row_data)


def inventory_val():
    data = xlrd.open_workbook('/var/www/downfile/附件2：动力设备资源清查表.xlsx')
    sheet1 = data.sheet_by_index(0)
    nrows = sheet1.nrows

    # for i in range(4, nrows):
    #     row_data = sheet1.row_values(i)
    #     print(row_data)
    #     ax = AXgdlEquipment()
    #     ax.create(
    #         type=2
    #         area=2
    #         station='基站2'
    #         number='no2'
    #         node='基站'
    #         ground='1城区'
    #         produce=row_data[7]
    #         frame
    #         cap
    #         starttime
    #         monitoring
    #         rectification =row_data[0]
    #         renumber=row_data[1],
    #         modulecap=row_data[2]
    #         loadele=row_data[3]
    #         transmission=row_data[4]
    #         powerdown=row_data[5]
    #         oil
    #         pic
    #         desc
    #         people
    #         phone
    #         tid=1
    #         group
    #         brand
    #         changebox
    #         jifang
    #         kttype
    #         ktpower
    #         ifmonitoring
    #         hbtime
    #         iftransmission
    #         ifpowerdown
    #         ifstatus=row_data[6]
    #         xuhao
    #         posttime
    #     )

    '''
    for i in range(4, nrows):
        row_data = sheet1.row_values(i)
        print(row_data)
        ax = AXgdlEquipment()
        ax.create(
        type=1,
        area = 1,
        station = '基站1',
        number = 'no1',
        node = '基站',
        ground = '1城区',
        produce = row_data[7],
        rectification = row_data[0],
        renumber = row_data[1],
        modulecap = row_data[2],
        loadele = row_data[3],
        transmission = row_data[4],
        powerdown = row_data[5],
        people = row_data[19],
        phone = row_data[20],
        tid = 1,
        ifstatus = row_data[6],
        posttime = int(time.time()),
        # type=1
        # area=1
        # station='基站1'
        # number='no1'
        # node='基站'
        # ground='1城区'
        # produce=row_data[7]
        # frame
        # cap
        # starttime
        # monitoring
        # rectification =row_data[0]
        # renumber=row_data[1],
        # modulecap=row_data[2]
        # loadele=row_data[3]
        # transmission=row_data[4]
        # powerdown=row_data[5]
        # oil
        # pic
        # desc
        # people
        # phone
        # tid=1
        # group
        # brand
        # changebox
        # jifang
        # kttype
        # ktpower
        # ifmonitoring
        # hbtime
        # iftransmission
        # ifpowerdown
        # ifstatus=row_data[6]
        # xuhao
        # posttime


        )
    '''


if __name__ == '__main__':
    name_list = [
        '汉川中五甲',
        '汉川钟家台',
        '汉川双山GTNG1',
        '孝感汉宜边界补点（赵湾田水湾）',
        '后庄屋',
        '牛头村',
        '西畈村',
        '全心村',
        '汉宜共青',
        '汉川业集二GTNG1',
        '孝感项家湾',
        '庙湾',
        '孝感八大GT',
        '高观水厂',
        '银湖城基站',
        '北河转盘基站',
        '祥源新材',
        '新湖村(头潭村1)',
        '赵湾东',
        '汉川脉望NG1',
        '汉川刁汊湖NG1',
        '汉川庙头陈谢台NG1',
        '汉川城隍王集NG1',
        '汉川澎湖NG1',
        '汉川回龙水利管理站NG1',
        '汉川杨水湖挂口NG1',
        '汉川中洲赤壁NG1',
        '汉川业集林场NG1',
        '汉川洪三NG1',
        '汉川马口高湖NG1',
        '汉川石豆NG1',
        '汉川李集NG1',
        '汉川榔头NG1',
        '汉川福星NG1',
        '汉川窑新NG1',
    ]

    address_list = [
        '湖北孝感汉川乡镇西江乡中午甲村40米三管塔二期',
        '湖北孝感汉川乡镇西江钟家台40米三管塔二期',
        '湖北孝感汉川乡镇马鞍乡双山村40米三管塔二期',
        '湖北孝感汉川乡镇沉湖镇田水湾村美化塔 - 内40二期',
        '湖北孝感汉川乡镇杨林沟后庄屋村40米三管塔二期',
        '湖北孝感汉川乡镇杨林沟牛头村40米三管塔二期',
        '湖北孝感汉川乡镇杨林沟西畈村40米三管塔二期',
        '湖北孝感汉川乡镇西江全心村40米三管塔二期',
        '湖北孝感汉川乡镇杨林沟共青村40米三管塔二期',
        '湖北孝感汉川乡镇南河乡业集村40米三管塔二期',
        '湖北孝感汉川乡镇南河乡项家湾40米三管塔二期',
        '湖北孝感汉川乡镇南河乡庙湾村40米三管塔二期',
        '湖北孝感汉川乡镇南河乡八大村改40米三管塔二期',
        '湖北孝感汉川乡镇马鞍乡高观村40米三管塔二期',
        '湖北孝感汉川乡镇城关镇滨湖大道银湖城小区美化塔 - 内40二期',
        '湖北孝感汉川乡镇北河乡北河工业园内美化塔 - 内40二期',
        '湖北孝感汉川乡镇新河开发区皮草城内美化塔内40二期',
        '湖北孝感汉川乡镇新河镇头潭村40米三管塔二期',
        '湖北孝感汉川乡镇沉湖镇赵湾村美化塔 - 内40二期',
        '湖北省孝感市汉川市脉旺镇曹家湾',
        '湖北省孝感市汉川市刁汊湖',
        '湖北省孝感市汉川市庙头陈谢台',

    ]
    # nums=random.randint(0, 21)
    # axgdlclean=AXgdlClean()
    inventory_val()
    # inspect_val()
    # data = XgAmmeter.select()
    # for item in data:
    # address=item.address
    # url1 = 'https://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=json&ak=gRManfxm4xGfswhaIT4xGh78UpHV8kCV'
    # r = requests.get(url1)
    # print(r.text)
    # try:
    #     result = json.loads(r.text)
    #     x = result['result']['location']['lng']
    #     y = result['result']['location']['lat']
    #     XgAmmeter.update(x_code=x,y_code=y).where(XgAmmeter.id==item.id).execute()
    # except:
    #     pass










    # count = XgAmmeter.select().where(XgAmmeter.name == item.name,
    #                                  XgAmmeter.number == item.number,
    #                                  XgAmmeter.usercode == item.usercode,
    #                                  XgAmmeter.biaohao == item.biaohao).count()
    # if count > 1:
    #     print(count)
    #     print(item.biaohao)

    # towers=AXgdlTower()
    # towers.create(
    #
    # area=get_keys(area_dict,'孝南'),
    # station='孝南天仙南路NG1',
    # address='湖北孝感孝南槐荫大道中段天仙南路西侧路边',
    # tnumber='420902908000000294',
    # stype='2G+3G+4G',
    # money='是',
    # ttpye='景观塔',
    # hight='40',
    # stationtype='一体化机柜',
    # transfer='已移交',
    # share='是',
    # tshare='3',
    # tsharelist='',
    # sharelist='',
    # sharenumber='1',
    # sharedesc='2',
    # elesharelist='',
    # rru='是',
    # antenna='3',
    # pic='',
    # reading='抄表人',
    # phone='18696100212',
    # posttime=int(time.time())
    #
    # )


    # axgdlclean.create(
    #     name=name_list[nums],
    #     number='No' + str(random.randint(0, 15)),
    #     area=str((random.randint(1, 7))),
    #     posttime=int(time.time()),
    #     pid='1',
    #     pic='192.168.188.178:86/a.png',
    #     address=address_list[nums],
    #     capital=address_list[nums],
    #
    #     rank=random.randint(1,2), # 普通和高等话
    #     jifan=random.randint(1,3), #一体话 自建 租赁
    #     tower=random.randint(1,6), #美化天线  四角塔 三角塔 拉线塔 楼面抱杆  路灯杆
    #     jizhan=random.randint(1,6),  #2+4  2+3+4 3+4 2 3 4
    #     height=random.randint(3,10),
    #     transfer=random.randint(1,3), #全部移交 机房移交 铁塔移交
    #     share=random.randint(1,3),  #电信 联通 电信+联通
    # )

    # axgdlreading = AXgdlReading()
    # axgdlreading.create(
    # name=name_list[random.randint(0, 34)],
    # pid='1',
    # last=(random.randint(0, 180)),
    # meter=(random.randint(180, 380)),
    # pic='192.168.188.178:86/a.png',
    # now=(random.randint(0, 180)),
    # compare=str(random.randint(40,80)),
    # desc ='备注待补充',
    # posttime = int(time.time()),
    # x_code = random.randint(0, 180),
    # y_code = random.randint(0, 180),
    # area = str((random.randint(1, 7))),
    # number='No'+str(random.randint(0,15)),
    # )

    # database.connect()
    # #创建表时如果表已存在会报错，捕获异常直接跳过
    # try:
    #     database.create_tables([ search_info])
    # except:
    #     pass
