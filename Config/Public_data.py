import os

# 整个项目根目录的绝对路劲
baseDir = os.path.dirname(os.path.dirname(__file__))
print(baseDir)

# 测试数据文件相对于工程根目录的相对路径
excelPath = baseDir + "\\TestData\\inter_test_data.xlsx"


apiExcelName = "API"

# 测试数据excel文件中，API表中列号数字映射
API_apiName = 2
API_requestUrl = 3
API_requestMothod = 4
API_paramsType = 5
API_apiTestCaseFileName = 6
API_active = 7

# 测试数据excel文件中，API的测试用例表中的列号数字映射
CASE_requestData = 1
CASE_relyData = 2
CASE_responseCode = 3
CASE_responseData = 4
CASE_dataStore = 5
CASE_checkPoint = 6
CASE_active = 7
CASE_status = 8
CASE_errorInfo = 9

# 存储请参数里面依赖数据
# REQUEST_DATA = {"用户注册":{"1":{"username":"zhangsan","password":"234dr3"}}}
REQUEST_DATA = {}

# 存储响应对象中的依赖数据
RESPONSE_DATA = {}