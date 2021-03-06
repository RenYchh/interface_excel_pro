import requests
from Util.ParseExcel import ParseExcel
from Config.Public_data import *
from Action.get_rely import GetRelyValue
from Util.HttpClient import HttpClient
from Action.Data_Store import RelyDataStore
from Action.check_result import CheckResult
from Action.write_result import write_result
from Util.md5_encrypt import *


def main():
    # 实现从获取接口测试数据到发送情况，再到获取返回结果，并处理结果
    # 创建ParseExcel类的实例对象
    parseE = ParseExcel()
    # 调用封装好的加载excel到内存的方法将需要解析的excel加载到内存
    parseE.loadWorkBook(excelPath)
    # 获取“API”表的表对象
    sheetObj = parseE.getSheetByName(apiExcelName)
    # 获取API表中是否需要执行api自动化case的列对象
    activeList = parseE.getColumn(sheetObj, API_active)
    # 遍历是否需要执行标记列，只执行标记为yes的api自动化测试
    for idx, cell in enumerate(activeList[1:], 2):
        if cell.value == "y":
            # 需要执行的api
            rowObj = parseE.getRow(sheetObj, idx)
            apiName = rowObj[API_apiName -1].value
            requestUrl = rowObj[API_requestUrl - 1].value
            requestMethod = rowObj[API_requestMothod - 1].value
            paramsType = rowObj[API_paramsType - 1].value
            apiTestCaseSheetName = rowObj[API_apiTestCaseFileName -1].value

            # 下一步就是获取api的测试case，然后准备执行用例
            caseSheetObj = parseE.getSheetByName(apiTestCaseSheetName)
            caseActiveObj = parseE.getColumn(caseSheetObj, CASE_active)
            print(caseActiveObj)
            for c_idx, col in enumerate(caseActiveObj[1:], 2):
                if col.value == "y":
                    # 说明当前case是需要被执行的
                    caseRowObj = parseE.getRow(caseSheetObj, c_idx)
                    requestData = caseRowObj[CASE_requestData - 1].value
                    relyData = caseRowObj[CASE_relyData - 1].value
                    dataStore = caseRowObj[CASE_dataStore - 1].value
                    checkPoint = caseRowObj[CASE_checkPoint - 1].value
                    # 下一步，在发送接口请求之前，需要处理数据依赖
                    if relyData:
                        # 需要进行数据依赖处理
                        requestData = GetRelyValue.get(requestData, relyData)
                        print(requestData)
                    else:
                        print("第%s个API的第%s条不需要做数据依赖处理！" %((idx -1), (c_idx -1)))
                    # 没有数据依赖处理时，需要判断下是不是json数据类型
                    if requestData[0] == "{" and requestData[-1] == "}":
                        # 说明请求参数是一个json串格式数据，若是，需要转成字典类型
                        requestData = eval(requestData)

                    # 处理登录时的密码加密
                    if apiName == "login":
                        requestData["password"] = md5_encrypt(requestData["password"])


                    # 处理完接口请求参数的依赖数据后，接下来就是发送请求并获取响应结果
                    response = HttpClient.request(requestUrl, requestMethod, paramsType, requestData)
                    print(response.status_code)
                    print(response.json())
                    # 下一步，根据接口响应结果，做数据依赖存储以及结果检测
                    if response.status_code == 200:
                        # 获取接口的响应body（获取的是字典类型）
                        responseBody = response.json()
                        # 接下来做数据依赖存储
                        if dataStore:
                            RelyDataStore.do(apiName,c_idx-1,requestData, responseBody, eval(dataStore))

                    # 接下来进行接口响应结果的检测
                    if checkPoint:
                        errorKey = CheckResult.check(response.json(),eval(checkPoint))

                        # 将测试结果写回excel
                        write_result(parseE,caseSheetObj,response.json(),errorKey,c_idx)

                else:
                    print("第%s个API的第%s条case被忽略执行！" %((idx -1), (c_idx -1)))
        else:
            print("第%s个API被忽略执行！" %(idx -1))

if  __name__ == "__main__":
    main()

