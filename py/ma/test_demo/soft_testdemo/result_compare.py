from DPublic.MysqlDB import Base, db_session, engine
import pandas as pd
import json
import time


def read_from_mysql_2_DataFrame():
    try:
        df = pd.read_sql("""SELECT a.modelName,a.time,a.prediction,b.Sample_TestResult,c.test_code 
        FROM soft_predict_result a,lims_data b,lim_dict c WHERE a.optColid=b.DICTIONARYID AND 
        b.DICTIONARYID=c.dictionaryid AND  a.time=b.Sampling_Date ORDER BY a.time""", engine.raw_connection())
        return df
    except Exception as e:
        print(e)


if __name__ == '__main__':
    modelNames = ["1#质量软测量-A", "1#质量然测量-B"]
    df = read_from_mysql_2_DataFrame()

    if len(df)!=0:

        resultList = []
        for modelName in modelNames:
            resultDict = {}
            resJson = df[df['modelName'] == modelName][['time', 'prediction', 'Sample_TestResult', 'test_code']].to_json(orient='records')
            resultDict['modelName'] = modelName
            resultDict['data'] = json.loads(resJson)
            resultList.append(resultDict)

        res = {"result": resultList}
        print(json.dumps(res))



