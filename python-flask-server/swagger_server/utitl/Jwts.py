# - * - coding: utf-8 - * -
import jwt,time,json,urllib.request
class Jwts:
    #生成AuthToken
    login_url = ''    #登录地址
    api_url = ''    #其他业务接口地址
    def __init__(self):
        self.login_url = 'http://test.awarepower.com:8444/jwt/login'
        self.api_url = 'http://test.awarepower.com:8080'

    def getAuthToken(self):
        sub = '544032576'
        exp = int(time.time() + 900)
        # 生成AuthToken,获取后没有做缓存，你们自行考虑是否需要缓存，目前过期时间为15分钟
        token = jwt.encode({'sub': sub, 'exp': exp}, key='4fba6786c7e54b00976270ab52f75dbe').decode('UTF-8')
        return token

    def getToken(self):
        token = self.getAuthToken()
        userinfo = {'username': 'mo', 'password': 'mo1234'}
        headers = {
            'X-Ca-AuthToken': token,
            'Content-type': 'application/json'
        }
        req = urllib.request.Request(url=self.login_url, headers=headers, data=json.dumps(userinfo).encode('UTF-8'), method='POST')
        x = urllib.request.urlopen(req)
        result = json.loads(x.read().decode('UTF-8'))
        return result

    #获取电表组数据
    def getGroupMeter(self):
        url = self.api_url+'/jwt/mgt/meter/list/23'    #电表组ID替换为系统存在的否则报406错误
        authToken = self.getAuthToken()
        token = self.getToken()['payload']['token']
        headers = {
            'Host': 'test.awarepower.com:8080',
            'User-Agent': 'curl/7.46.0',
            'Accept': '*/*',
            'Content-type': 'application/json',
            'X-Ca-AuthToken': authToken,
            'X-Ca-AccessToken': token
        }
        req = urllib.request.Request(url=url,headers=headers)
        f = urllib.request.urlopen(req)
        result = f.read().decode('utf-8')
        return result


    #获取实时数据
    def getRealTime(self,meter_list=''):
        #另外一个电表号：161211000010
        url = self.api_url+'/jwt/data/realtime/' + meter_list   # 电表ID替换为系统存在的否则报406错误
        authToken = self.getAuthToken()

        token = self.getToken()['payload']['token']
        headers = {
            'Host': 'test.awarepower.com:8080',
            'User-Agent': 'curl/7.46.0',
            'Accept': '*/*',
            'Content-type': 'application/json',
            'X-Ca-AuthToken': authToken,
            'X-Ca-AccessToken': token
        }
        req = urllib.request.Request(url=url, headers=headers)
        f = urllib.request.urlopen(req)
        result = f.read().decode('utf-8')
        return result

jwt_s = Jwts()
if __name__ == '__main__':
    a = Jwts()
    # print('------a.getAuthToken()-------', a.getAuthToken())
    # print('------a.getToken()----------', a.getToken())
    # print(a.getGroupMeter())    #获取电表组
    # print(a.getRealTime('161211000010'))    #获取电表实时数据
