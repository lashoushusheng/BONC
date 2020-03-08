import json

fpath = r"E:\code\Athena\taurus_开发_测试\_data\ma16_data\ori_data\优化分析\train_data\#常减压优化分析历史数据_参数.csv"

with open(fpath, 'r') as f:
    aaa = f.readlines()
    print(type(aaa), aaa)


ds = {
    "dataSourceName": "1#常减压优化历史数据",
    "dataSourceDesc": "这是个测试",
    "dataSourceDir": aaa,
    "dataFileName": "1#常减压优化历史数据.csv",
    "paramsFileName": "#常减压优化分析历史数据_参数.csv"
}

fpath2 = r"E:\111.json"
with open(fpath2, 'w') as f:
    f.write(json.dumps(ds))
