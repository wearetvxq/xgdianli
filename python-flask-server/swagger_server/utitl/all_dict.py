from pandas import json
def get_keys(d, value):
    a = [k for k, v in d.items() if v == value]
    return a[0]


area_dict = {
    '':'',
    1: '安陆',
    2: '大悟',
    3: '汉川',
    4: '孝昌',
    5: '孝南',
    6: '应城',
    7: '云梦',
}

if_dict={
    '':'',
    1:'是',
    2:'否',
}

rank_dict = {
    1: '普通',
    2: '高等化',
}
jifan_dict = {2: '自建机房',
              1: '一体化',
              3: '租赁机房'}
tower_dict = {2: '四角塔',
              6: '路灯杆',
              5: '楼面抱杆',
              4: '拉线塔',
              3: '三角塔',
              1: '美化天线'}
jizhan_dict = {
    2: '2G+3G+4G',
    5: '3G',
    3: '3G+4G',
    4: '2G',
    1: '2G+4G',
    6: '4G'}
transfer_dict = {
    3: '铁塔移交',
    2: '机房移交',
    1: '全部移交'}
share_dict ={
    1: '电信',
    2: '联通',
    3: '电信+联通'}

# jizhandesc_dict={
#     1:"一体化（2G+3G+4G）",
# 1:"共址两套（2G+4G）",
# 1:"共址三套（2G+3G+4G）",
# 1:"拉远（3G+4G）",
# 1:"拉远（2G）",
# 1:"",
#     1:"",
#
# }

list = ['电信', '联通', '电信+联通', ]
if __name__ == '__main__':

    a=get_keys(rank_dict,'普通')
    print(type(a))
    #
    #  dict = {}
    # for index, name in enumerate(list):
    #     dict[str(index + 1)] = name
    # dict = json.loads(dict, indent=2)
    # print(dict)
    # rank = random.randint(1, 2),  # 和
    # jifan = random.randint(1, 3),  # 一体话 自建 租赁
    # tower = random.randint(1, 6),  # 美化天线  四角塔 三角塔 拉线塔 楼面抱杆  路灯杆
    # jizhan = random.randint(1, 6),  # 2+4  2+3+4 3+4 2 3 4
    # height = random.randint(3, 10),
    # transfer = random.randint(1, 3),  # 全部移交 机房移交 铁塔移交
    # share = random.randint(1, 3),  # 电信 联通 电信+联通
