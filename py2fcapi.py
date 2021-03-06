import requests
import json
import time
'''
用法:
acc='123'
psw='***'
token='1h2h4h5j6j7jk8'
a= FCAPI(acc,psw,token)
result = a.getKeywords('keyword')
print(result)

>>> [{word:'keyword',pcPV:1,mobPV:2,pv:3}]

如果需要打印请求状态
a= FCAPI(acc,psw,token)
result = a.getKeywords('keyword')
print(a.status)


>>> keyword success
'''

class FCAPI(object):
    def __init__(self, acc, psw, token, maxnum=1000):
        self.acc = acc
        self.psw = psw
        self.token = token
        self.payload = {
            "header":
            {
                "username": self.acc,
                "password": self.psw,
                "token": self.token
            },
            "body":
            {
                "queryType": 1,
                "query": "",
                "seedFilter": {
                    "maxNum": maxnum
                }
            }
        }
        self.url = "https://api.baidu.com/json/sms/service/KRService/getKRByQuery"

    def _push(self,kw):
        self.payload['body']['query'] = kw
        req = requests.post(self.url, data=json.dumps(self.payload))
        return req.text

    def _analysis(self,result):
        result_list = json.loads(self.result)['body']['data']
        out_result = []
        for i in result_list:
            out_result.append(
                dict(word=i['word'], pcPV=i['pcPV'], mobPV=i['mobilePV'], pv=i['pv']))
        return out_result

    def getKeywords(self, kw):
        self.kw=kw
        self.result = self._push(self.kw)
        return self._analysis(self.result)

    @property
    def status(self):
        return self.kw+' '+json.loads(self.result)['header']['desc']

