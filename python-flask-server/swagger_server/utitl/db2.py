'''
from peewee import MySQLDatabase
from peewee import *

database = MySQLDatabase('xgyd', **{'user': 'root', 'use_unicode': True, 'charset': 'utf8', 'host': '39.108.165.149',
                                    'port': 3306, 'password': 'lcj123456'})
class BaseModel(Model):
    class Meta:
        database = database


class AXgdlEquipment(BaseModel):
    area= CharField()#县市分公司
    jifang= CharField()#机房
    node= CharField()#节点
    station= CharField()#基站名称（机房楼要写清楚机房名称和楼层）
    code= CharField()  #基站编码(站号)
    node_type= CharField()  #节点类型
    typec = CharField()  #设备类型
    offen= CharField()  #是否属于本地区停电频繁基站
    oil= CharField()  #该站是否配置了固定自启动油机
    desc= CharField()  #备注
    people= CharField()  #填报人
    phone= CharField()  #联系电话
    factory= CharField()  #生产厂家
    frame= CharField()  #机架型号
    cap= CharField()  #机架容量（A）
    starttime= CharField()  #开始使用时间（格式：YYYY年MM月）
    monitoring= CharField()  #监控模块型号
    rectification= CharField()  #整流模块型号
    renumber= CharField()  #整流模块数量（块）
    modulecap= CharField()  #模块容量（）
    loadele= CharField()  #负载电流（A）
    iftransmission= CharField()  #传输及基站是否共用
    ifpowerdown= CharField()  #是否有二次下电功能
    ifstatus = CharField()  #目前运行状态是否正常
    type= CharField()  #型号
    group= CharField()  #组数
    ifmonitoring= CharField()  #是否安装单体监控
    hbtime= CharField()  #经放电测试大约后备时长（小时）
    ktpower= CharField()  #功率（匹）
    kttype= CharField()  #柜式 / 壁挂 / 窗式 / 一体化
    xuhao= CharField()  #序号
    changebox= CharField()  #交流配电箱
    number= CharField()  #数量
    brand= CharField()  #品牌
    address= CharField()  #地点

    # id
    # type
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
    # oil
    # pic
    # desc
    # people
    # phone
    # tid
    # 
    # 
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
    # ifstatus
    # xuhao

    # tower_name#铁塔公司基站名称
    # tower_address#详细地点描述
    # tower_code#铁塔公司站址编码
    # if_tower_pay#电费是否有铁塔公司支付
    # tower_type#铁塔类别
    # tower_higu#铁塔高度
    # 机房类型（自建机房 / 租赁机房 / 一体化机柜 / RRU拉远 / 无机房）
    # 移交类型（已移交 / 移交塔 / 移交机房 / 新建）
    # 是否共享
    # 铁塔共享用户数
    # 铁塔共享清单（1
    # 家和3家可不写，2
    # 家要写移动 + 电信或者移动 + 联通）
    # 机房共享用户数
    # 机房共享清单
    # 电表共享情况
    # 电表共享清单
    # RRU是否安装在景观塔上
    # 天线数量
    # 照片（单独文件夹，放上塔型和机房类型的照片）
    # 填表日期
    # 交转直
    # 局端型号
    # 监控型号
    # 功率（KW）模块型号
    # 模块数量
    # 开始使用时间（格式：YYYY年MM月）备注

    class Meta:
        table_name = 'a_xgdl_equipment'



if __name__ == '__main__':
    f = open("./1.text")
    #
    ip_list = []
    for line in f:
        line = line.replace('\n', '').replace(' ','')
        if line not in ip_list:
            ip_list.append(line)
    f.close()
    for i in ip_list:
        print(i)
    print(ip_list)
    # database.connect()
    # #创建表时如果表已存在会报错，捕获异常直接跳过
    # try:
    #     database.create_tables([ search_info])
    # except:
    #     pass
    
    
'''