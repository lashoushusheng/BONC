import requests
import json

body={
    "dataSourceName": "生产预警分析",
    "dataSourceDesc": "生产预警分析",
    "dataSourceDir": "生产预警分析",
    "dataFileName": "生产预警分析"
}

headers = {
    'content-type': "application/json"
    # 'content-type': 'charset=utf8',
    # 'content-type': 'charset=gb2312'
}
# res = requests.post("http://demo.shenzhuo.vip:49019/a/b/c/e", data=json.dumps(body) ,headers=headers)
res = requests.post("http://demo.shenzhuo.vip:49019/analysis_api/v1/greyPredict/train_get_dataSource_list")
# res = requests.post("http://172.16.71.159:7752/analysis_api/v1/greyPredict/train_get_dataSource_list")
# res1 = requests.get("http://demo.shenzhuo.vip:49019/a/b/c/e")

print(res.text)
# print(res1.text)




# http://172.16.71.159:7752/analysis_api/v1/greyPredict/train_get_dataSource_list