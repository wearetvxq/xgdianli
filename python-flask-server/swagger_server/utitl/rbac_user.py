# - * - coding: utf-8 - * -
# Rbac通用认证方法
from .mysqlset import MySQL
import json

class Rbac:
    def __init__(self):
        self.ms = MySQL(1)

    #判断是否拥有当前模块权限
    def checkModule(self, role_id, module):
        result = self.ms.query('SELECT COUNT(*) FROM `r_access` WHERE `role_id`=' + str(role_id) +' AND `route`="'+ module +'"')[0][0]
        if not result:
            return False
        else:
            return True

    #检查当前操作是否需要认证
    def checkAccess(self, uid, module):
        #根据uid查询到用户分组
        result = self.ms.query('SELECT `group` FROM `r_user` WHERE `id`='+str(uid))
        if not result:
            return False
        else:
            group_result = self.ms.query('SELECT `role_id` FROM `r_role_group` WHERE `user_group_id`='+str(result[0][0]))
            if not group_result:
                return False
            else:
                if self.checkModule(group_result[0][0], module) == True:
                    return self.getAccessMenuList(group_result[0][0])
                else:
                    return False

    #获取已授予权限的菜单及按钮等操作
    def getAccessMenuList(self,role_id):
        result = self.ms.query('SELECT * FROM `r_access` WHERE `role_id`='+str(role_id))
        node_id = []
        for i in range(len(result)):
            node_id.append(str(result[i][1]))
        map = ",".join(node_id) #将需要查询的list转换为字符串
        menu_list = self.ms.query('SELECT * FROM `r_node` WHERE `id` in('+ map +')')
        #获取菜单并返回list
        menu = []
        for n in range(len(menu_list)):
            #获取一级菜单
            if menu_list[n][7] == 0:
                level_one_temp = {
                    'id': menu_list[n][0],
                    'name': menu_list[n][2],
                    'level': menu_list[n][7],
                    'child': ''
                }
                menu.append(level_one_temp)

        for t in range(len(menu)):
            childs = []
            for u in range(len(menu_list)):
                if menu_list[u][6] == menu[t]['id']:
                    temp = {
                        'pid':menu_list[u][6],
                        'name':menu_list[u][2],
                        'level': menu_list[u][7],
                        'url': menu_list[u][1]
                    }
                    childs.append(temp)
            menu[t]['child'] = childs
        return menu

    #添加用户分组
    def addUserGroup(self, data):
        total = self.ms.query('SELECT COUNT(*) FROM `r_user_group` WHERE `name`="'+ data['name'] +'"')[0][0]
        if total == 0:
            value = {
                'name': data['name'],
                'status': str(data['status'])
            }
            user_group_id = self.ms.insert('r_user_group', value)
            if user_group_id > 0:
                values = {
                    'role_id': str(data['role_id']),
                    'user_group_id': str(user_group_id)
                }
                self.ms.insert('r_role_group', values)
                return True
            else:
                return False
        else:
            return False

    #获取用户组
    def getUserGroup(self):
        result = self.ms.query('SELECT * FROM `r_user_group`')
        lists = []
        for i in range(len(result)):
            temp = {
                'id': result[i][0],
                'name': result[i][1],
                'status': result[i][2]
            }
            lists.append(temp)
        return lists

    #改变用户分组状态
    def editUserGroupStatus(self, group_id, status):
        value = {
            'status': str(status)
        }
        if self.ms.update('r_user_group', value, 'id='+str(group_id)):
            return True
        else:
            return False

    # 编辑用户分组
    def editUserGroup(self, data):
        value = {
            'name': data['name'],
            'status': data['status']
        }
        if self.ms.update('r_user_group', value, 'id=' + str(data['id'])):
            return True
        else:
            return False

    #添加角色列表
    def addRole(self, data):
        total = self.ms.query('SELECT COUNT(*) FROM `r_role` WHERE `name`="' + data['name'] + '"')[0][0]
        if total == 0:
            value = {
                'name': data['name'],
                'status': str(data['status']),
                'remark': data['remark']
            }
            if self.ms.insert('r_role', value) > 0:
                return True
            else:
                return False
        else:
            return False

    #获取角色列表
    def getRole(self):
        result = self.ms.query('SELECT * FROM `r_role`')
        lists = []
        for i in range(len(result)):
            temp = {
                'id': result[i][0],
                'name': result[i][1],
                'status': result[i][3],
                'remark': result[i][4]
            }
            lists.append(temp)
        return lists

    # 改变角色状态
    def editRoleStatus(self, role_id, status):
            value = {
                'status': str(status)
            }
            if self.ms.update('r_user_group', value, 'id=' + str(role_id)):
                return True
            else:
                return False

    #编辑角色
    def editRole(self, data):
        value = {
            'name': data['name'],
            'status': data['status'],
            'remark': data['remark']
        }
        if self.ms.update('r_role', value, 'id=' + str(data['id'])):
            return True
        else:
            return False

    #添加节点列表
    def addNode(self, data):
        total = self.ms.query('SELECT COUNT(*) FROM `r_node` WHERE `name`="' + data['name'] + '"')[0][0]
        if total == 0:
            value = {
                'name': data['name'],
                'title': data['title'],
                'status': str(data['status']),
                'remark': data['remark'],
                'sort': str(data['sort']),
                'pid': str(data['pid']),
                'level': str(data['level'])
            }
            if self.ms.insert('r_node', value):
                return True
            else:
                return False
        else:
            return False

    #获取节点列表
    def getNodeList(self):
        menu_list = self.ms.query('SELECT * FROM `r_node`')
        # 获取菜单并返回list
        menu = []
        for n in range(len(menu_list)):
            # 获取一级菜单
            if menu_list[n][7] == 0:
                level_one_temp = {
                    'id': menu_list[n][0],
                    'name': menu_list[n][2],
                    'level': menu_list[n][7],
                    'child': ''
                }
                menu.append(level_one_temp)

        for t in range(len(menu)):
            childs = []
            for u in range(len(menu_list)):
                if menu_list[u][6] == menu[t]['id']:
                    temp = {
                        'id': menu_list[u][0],
                        'pid': menu_list[u][6],
                        'name': menu_list[u][2],
                        'level': menu_list[u][7],
                        'url': menu_list[u][1]
                    }
                    childs.append(temp)
            menu[t]['child'] = childs
        return menu

    #编辑节点菜单
    def editNodeList(self, data):
        value = {
            'name': data['name'],
            'title': data['title'],
            'status': data['status'],
            'remark': data['remark'],
            'sort': data['sort'],
            'pid': data['pid'],
            'level': data['level']
        }
        if self.ms.update('r_node', value, 'id=' + str(data['id'])):
            return True
        else:
            return False

    #将用户选择的权限入库
    def saveAccess(self, data):
        data = json.loads(data)
        role_id = data['id']
        node_list = data['node']
        self.ms.delete('r_access', 'role_id='+str(role_id))   #添加权限的时候先将原有权限全部删除
        for i in range(len(node_list)):
            value = {
                'role_id': role_id,
                'node_id': node_list[i]['name'],
                'level': node_list[i]['level'],
                'route': node_list['url']
            }
            bool = self.ms.insert('r_access',value)
        if bool:
            return True
        else:
            return False


if __name__ == '__main__':
    print('comm')
    # rbac = Rbac()
    # print(json.dumps(rbac.checkAccess('1', 'home')))
    #rbac.getUserGroup()
    #rbac.editUserGroupStatus(1,0)
    #rbac.getRole()
    #print(json.dumps(rbac.getNodeList()))

    '''data = json.dumps({
        "id": "1",
        "node": [{
            "id": 2,
            "pid": 1,
            "name": "首页添加",
            "level": 1,
            "url": "home/add"
        },
        {
            "id": 3,
            "pid": 1,
            "name": "首页删除",
            "level": 1,
            "url": "home/del"
        }]
    })
    rbac.saveAccess(data)'''

    '''data = {
        'role_id': 1,
        'name': '测试2',
        'status': '0'
    }
    if rbac.addUserGroup(data) == True:
        print(2)
    else:
        print(3)'''


    '''data = {
        'name': '测试角色',
        'status': '0',
        'remark': 'cced'
    }
    if rbac.addRole(data) == True:
        print(2)
    else:
        print(3)'''

    '''data = {
        'name': 'home/index',
        'title': '测试节点',
        'status': '0',
        'remark': '测试',
        'sort': '1',
        'pid': '0',
        'level': '0'
    }
    if rbac.addNode(data) == True:
        print(111)
    else:
        print(333333)'''
