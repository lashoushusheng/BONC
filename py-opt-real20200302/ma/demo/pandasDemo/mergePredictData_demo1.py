# -*- coding: utf-8 -*-
import time

import pandas as pd

outputFpath = r'E:\code\BONC\rtc_开发_测试\_data\ma16_data\优化分析\1#常减压优化分析模型\predict_result\result_2\part-00000-2f20181b-d19c-4e02-a20c-75a69c152c0e-c000.csv'
dfOutput = pd.read_csv(outputFpath, engine='python')
# dfOutput = pd.DataFrame(dfOutput, index=['time'])
print(dfOutput.iloc[[0]])
print(dfOutput['time'][0])
print("*" * 100)

inputFpath = r'E:\code\BONC\rtc_开发_测试\_data\ma16_data\优化分析\1#常减压优化分析模型\predict_input\optmodel_0814.csv'
# df = pd.read_csv(inputFpath, engine='python', encoding='utf-8')
# dfInput = pd.read_csv(inputFpath, engine='python', index=['time'])
dfInput = pd.read_csv(inputFpath, engine='python')
print(dfInput.iloc[[0]])
print(dfInput['time'][0])
timeStamp = time.mktime(time.strptime(dfInput['time'][0], '%Y/%m/%d %H:%M'))
print(int(timeStamp))

dfInput['time'] = dfInput['time'].apply(
    lambda x: int(time.mktime(time.strptime(x, '%Y/%m/%d %H:%M')))
)
print(dfInput.iloc[[0]])
print("*" * 100)


dfMerge11 = pd.merge(dfOutput, dfInput, how='left', on='time')
print(dfMerge11.iloc[[0]])
print(dfMerge11.columns)

# dfMerge12 = pd.concat([dfOutput,dfInput],axis=1)
# print(dfMerge2.iloc[[0]])
print("*" * 100)


# dfMerge21 = pd.merge(dfOutput, dfInput, how='outer', on='time')
# print(dfMerge21.iloc[[0]])
# print(dfMerge21.count)

# dfMerge22 = pd.concat([dfOutput, dfInput], axis=1)
# print(dfMerge22.count)

# dfMerge23 = dfMerge22.groupby(['time']).apply(list)
# print(dfMerge23.count)


# for oRow in dfOutput.itertuples():
#     print("111111111111", oRow.time)
#     print("111111111111", oRow)
#     break
    # for iRow in dfOutput.rows:

for index, oRow in dfOutput.iterrows():
    print("2222222222222...time...", oRow['time'])
    print("2222222222222...oRow...", oRow)
    oTime = oRow['time']

    iRow = dfInput[dfInput['time']==oTime]
    # iRow = dfInput._ix(oTime)
    print("2222222222222...iRow...", iRow)

    for oClmn in dfOutput.columns:
        print("2222222222222...{} | {} | {}".format(oClmn, oRow.get(oClmn), iRow.iloc[0].get(oClmn)))

    break