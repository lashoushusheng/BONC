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


if __name__ == '__main__':
    res = Mysql_MA_Result.find_test()

    print(type(res))
    print(res[0].modelType, res[0].modelName, res[0].predictDir, res[0].modelParams, res[0].traindsId)

    # for item in res:
    #     print(item.modelType, item.modelName, item.predictDir, item.modelParams, item.traindsId)

