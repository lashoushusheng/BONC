import pandas as pd
import datetime

# df = pd.read_csv("/root/works/idata/ma16_data/origin_data/生产预警分析/predic_data/merge_data_在线数据.csv")
# # df = pd.read_csv("/root/works/idata/ma16_data/origin_data/生产预警分析/train_data/merge_data_训练数据.csv")
#
# datastr = df.loc[0, "time"]
#
# initTime = datetime.datetime.strptime(datastr, '%Y/%m/%d %H:%M')
#
# tempTime = initTime
#
# for index, row in df.iterrows():
#     df.loc[index, "time"] = datetime.datetime.strftime(tempTime, '%Y/%m/%d %H:%M:%S')
#     tempTime = tempTime + datetime.timedelta(seconds=15)
#     print(index)
#
# df.to_csv("merge_data_在线数据_sec.csv", index=False)
from pandas.errors import *

try:
    df = pd.read_csv("/root/works/idata/ma16_data/生产预警分析/TI284_1塔顶温度-test/train_result/predictSucessSta/part-00000-6bb923c0-9e9b-443c-aa1d-5ce9b9a21536-c000.csv", engine='python')
except EmptyDataError:
    print("haha")