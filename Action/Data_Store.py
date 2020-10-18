#专门用于做数据依赖存储处理

from Config.Public_data import *

class RelyDataStore(object):
    def __init__(self):
        pass

    @classmethod
    def do(cls,apiName,caseId,requestData,responseBody,dataStore):
        param_dict = {}
        if isinstance(requestData,str):
            p_list = requestData.split("&")
            for i in p_list:
                key,value = i.split("=")
                param_dict[key] = value
            requestData = param_dict

        for key,value in dataStore.items():
            if key == "request":
                # 说明需要存储的数据是来自于接口的请求参数
                # datastore_{"request":["username","password"],"response":["code"]}
                # requestdata_ {"username":"srsdcx01","password":"wcx123wac1","email":"wcx@qq.com"}
                # REQUEST_DATA = {"用户注册":{"1":{"username":"zhangsan","password":"234dr3"}}}
                for i in value:
                    if i in requestData:

                        # 先看下你的结构在不在
                        if apiName not in REQUEST_DATA:
                            REQUEST_DATA[apiName] = {str(caseId):{i:requestData[i]}}
                        else:
                            if str(caseId) in REQUEST_DATA[apiName]:
                                REQUEST_DATA[apiName][str(caseId)][i] = requestData[i]
                            else:

                                REQUEST_DATA[apiName][str(caseId)] = {i:requestData[i]}
                    else:
                        print("需要做数据依赖存储的参数%s不存在" %i)

            elif key == "response":
                # 说明需要存储的数据是来自于接口的响应body
                for j in value:
                    if j in responseBody:
                        if not apiName in RESPONSE_DATA:
                            RESPONSE_DATA[apiName] = {str(caseId):{j:responseBody[j]}}
                        else:
                            if str(caseId) in RESPONSE_DATA[apiName]:
                                RESPONSE_DATA[apiName] = [str(caseId)][j] = responseBody[j]
                            else:
                                RESPONSE_DATA[apiName][str(caseId)] = {j:requestData[j]}
                    else:
                        print("需要存储的依赖参数%s在响应body中未找到" %j)

        print(REQUEST_DATA)
        print(RESPONSE_DATA)

if __name__ == "__main__":
    # 字典类型的参数
    r = {"username":"srsdcx01","password":"wcx123wac1","email":"wcx@qq.com"}

    # 字符串类型的参数
    # r = "username=sdfwe&password=xdswewe&flag=true"

    s = {"request":["username","password"],"response":["userid"]}
    res = {"userid":12,"code":"00"}
    # do(cls, apiName, caseId, requestData, responseBody, dataStore)
    RelyDataStore.do("register",1,r,res,s)
    print(REQUEST_DATA)
    print(RESPONSE_DATA)