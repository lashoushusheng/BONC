# -*- coding: utf-8 -*-
import pandas as pd

# fpath = r'E:\code\Athena\taurus_开发_测试\_data\ma16_log\优化分析\source_data\数据源.csv'
# csvData = pd.read_csv(fpath, engine='python')
# print(csvData)


# fpath = r'E:\code\Athena\taurus_开发_测试\_data\ma16_log\优化分析\train_data\train_result_2.csv'
fpath = r'E:\code\Athena\taurus_开发_测试\_data\ma16_data\ori_data\优化分析\train_data\#常减压优化分析历史数据_参数.csv'

df = pd.read_csv(fpath, engine='python', encoding='utf-8')

print(df)
# print(data[:0])
print(df.columns)
# print(df.values)
# print(df.shape)

for x in df.columns:
    print(x, type(x))
    print(df[x])
    break

a = df.to_json()
print(a)

