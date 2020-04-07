# -*- coding: utf-8 -*-
from DPublic.MysqlDB import Base, db_session


class Mysql_MA_Result(object):

    def __init__(self):
        pass

    @classmethod
    def find_result(cls, modelType, modelNames, dataSourceName):
        """
        """
        if len(modelNames) == 1:
            modelNames_t = f"('{modelNames[0]}')"
        else:
            modelNames_t = tuple(modelNames)

        sql = """SELECT a.modelType modelType, a.modelName modelName, a.predictDir predictDir,
        b.modelParams modelParams,b.dsId traindsId,a.predictState predictState 
        FROM ma_predict a,ma_train b WHERE a.modelType='%s' AND a.dsName='%s'
         AND a.modelName IN %s AND a.modelName=b.modelName ORDER BY a.updateTime DESC""" \
              % (modelType, dataSourceName, modelNames_t)
        db_session.commit()
        return db_session.execute(sql).fetchall()

    @classmethod
    def find_test(cls):
        """
        """
        sql = """SELECT a.modelType modelType, a.modelName modelName, a.predictDir predictDir,
                b.modelParams modelParams,b.dsId traindsId,a.predictState predictState 
                FROM ma_predict a,ma_train b WHERE a.modelType='产品质量软测量' AND a.dsName='多氟多_2#_质量软测#在线数据'
                 AND a.modelName IN ("质量软测量_2#", "质量软测量_2#001", "质量软测量_2#003", "质量软测量_2#004") 
                 AND a.modelName=b.modelName ORDER BY a.updateTime DESC"""

        db_session.commit()
        return db_session.execute(sql).fetchall()

    @classmethod
    def soft_result_insert_2mysql(cls,modelName, optColid, time, prediction):
        """
        """
        sql = f"""INSERT INTO soft_predict_result(modelName,optColid,`time`,prediction) VALUES 
        ('{modelName}',{optColid},'{time}','{prediction}')"""
        db_session.execute(sql)
        db_session.commit()

    @classmethod
    def soft_result_Compare(cls):
        sql = """SELECT a.modelName,a.time,a.prediction,b.Sample_TestResult,c.test_code FROM 
        soft_predict_result a,lims_data b,lim_dict c WHERE a.optColid=b.DICTIONARYID AND 
        b.DICTIONARYID=c.dictionaryid AND  a.time=b.Sampling_Date ORDER BY a.time"""
        db_session.commit()
        return db_session.execute(sql).fetchall()


if __name__ == '__main__':
    res = Mysql_MA_Result.soft_result_Compare()
    for item in res:
        print(item.test_code)

