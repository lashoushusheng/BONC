import pandas as pd

actualDF = pd.read_csv("actualDF.csv")
predictionDF = pd.read_csv("predictionDF.csv")

"""
actualDF
                  time     T11
0  2017/01/26 18:45:45  495.40
1  2017/01/26 18:46:00  495.32
2  2017/01/26 18:46:15  495.32
3  2017/01/26 18:46:30  495.32
4  2017/01/26 18:46:45  495.40
predictionDF
                  time     T11
0  2017/01/26 18:46:00  495.32
1  2017/01/26 18:46:15  495.32
2  2017/01/26 18:46:30  495.32
3  2017/01/26 18:46:45  495.40
4  2017/01/26 18:47:00  495.32
5  2017/01/26 18:47:15  495.24
"""

# predictionDF.drop(predictionDF[predictionDF.time <= ""].index, inplace=True)
# print("删除后")
# print(predictionDF)

AccuracyList = []

lastTime = ""

actualDF.drop(actualDF[actualDF.time <= "2017/01/26 18:46:15"].index, inplace=True)
predictionDF.drop(predictionDF[predictionDF.time <= "2017/01/26 18:46:15"].index, inplace=True)

for index, actualRow in actualDF.iterrows():
    actualTime = actualRow['time']
    actualValue = actualRow['T11']
    predictRow = predictionDF[predictionDF['time'] == actualTime]

    if len(predictRow) > 0:
        predictValue = predictRow['T11'].reset_index(drop=True)[0]
        Accuracy = 1 - abs(float(predictValue) - actualValue) / actualValue
        AccuracyList.append(Accuracy)

print(AccuracyList)