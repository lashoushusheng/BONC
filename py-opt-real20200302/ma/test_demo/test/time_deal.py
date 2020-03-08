
import time, datetime
import pandas as pd

# d1 = datetime.datetime.strptime('2017/1/26 18:45:30', '%Y/%m/%d %H:%M:%S')
d1 = datetime.datetime.strptime('2017/1/26 18:45:30', '%H:%M:%S')


print(type(d1))

# df = pd.read_csv("/root/works/idata/ma16_data/origin_data/生产预警分析/train_data/生产预警_训练数据.csv")
# print(len(df))
# # print(df)
#
# temp = d1
#
# for index, row in df.iterrows():
#     temp = temp + datetime.timedelta(seconds=15)
#     print(index, row['time'], row['T11'])
#     df.loc[index, "time"] = temp.strftime('%Y/%m/%d %H:%M:%S')
#
# print(df)
# df.to_csv("/root/works/idata/ma16_data/origin_data/生产预警分析/train_data/生产预警_训练数据new.csv",
#           index=False, header=True)
