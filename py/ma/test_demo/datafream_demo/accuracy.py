import pandas as pd


actualDF = pd.DataFrame(columns=['date', 'prediction', 'isFault'])
# 保存预测值
predictionDF = pd.DataFrame(columns=['date', 'prediction', 'isFault'])



actualValue0 = [{'date': '2017-01-27 00:00:00', 'prediction': 498.4, 'isFault': 0},
                {'date': '2017-01-27 13:30:00', 'prediction': 498.4, 'isFault': 0},
                {'date': '2017-01-27 13:30:15', 'prediction': 498.4, 'isFault': 0}]

actualValue1 = [{'date': '2017-01-27 13:30:30', 'prediction': 498.4, 'isFault': 0},
                {'date': '2017-01-27 13:30:45', 'prediction': 498.48, 'isFault': 0},
                {'date': '2017-01-27 13:31:00', 'prediction': 498.48, 'isFault': 0}]

actualValue2 = [{'date': '2017-01-27 13:31:15', 'prediction': 498.48, 'isFault': 0},
                {'date': '2017-01-27 13:31:30', 'prediction': 498.48, 'isFault': 0},
                {'date': '2017-01-27 13:31:45', 'prediction': 498.52, 'isFault': 0}
                ]
aa = [actualValue0, actualValue1, actualValue2]

predictionValue = [{'date': '2017-01-27 13:33:30', 'prediction': 498.66, 'isFault': 0}, {'date': '2017-01-27 13:33:45', 'prediction': 498.68, 'isFault': 0}, {'date': '2017-01-27 13:34:00', 'prediction': 498.7, 'isFault': 0}]

# print(actualValue0[-1])

for i in range(3):
    actualDF = actualDF.append(aa[i][len(aa[i])-1], ignore_index=True)

print(actualDF)
print('~~~~~~~~~~~~~~~~~~~~~~')
print(actualDF.iloc[1:, :])
# for index, row in actualDF.iterrows():
#     # print(index)
#     print(row['date'], row['prediction'])
#     print(type(row['prediction']))

# aa = actualDF[actualDF['date'] == "2017-01-27 13:31:45"]
# print(type(aa["prediction"]))
# b = aa["prediction"].reset_index(drop=True)[0]
# print(float(b))
# print(type(float(b)))

# for i,v in b.items():
#     print(i,v)
