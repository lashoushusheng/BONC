# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from DPublic.MysqlDB import Base, db_session


class Mysql_MA_Predict(Base):
    """
    """
    __tablename__ = 'ma_predict'

    id = Column(Integer, primary_key=True)

    trainId = Column(Integer)
    dsId = Column(Integer)
    dsName = Column(String)

    modelType = Column(String)
    modelName = Column(String)

    predictDir = Column(String)
    predictState = Column(Integer)      # 0未开始，1进行中，2已完成
    predictBeginTime = Column(Integer)
    predictEndTime = Column(Integer)

    state = Column(Integer)

    def __init__(self, trainId, dsId, modelType, modelName, dsName, predictDir, predictState=0, state=1):
        self.trainId = trainId
        self.dsId = dsId

        self.modelType = modelType
        self.modelName = modelName
        self.dsName = dsName

        self.predictDir = predictDir
        self.predictState = predictState
        self.state = state


    @classmethod
    def find_one(cls, modelType, modelName, dataSourceName):
        db_session.commit()
        return db_session.query(cls).filter(
            cls.modelType == modelType,
            cls.modelName == modelName,
            cls.dsName == dataSourceName,
        ).first()

    # add by sun.jiping
    @classmethod
    def find_by_model_names(cls, modelType, modelNames, dataSourceName):
        """
        """
        if len(modelNames) == 1:
            modelNames_t = f"('{modelNames[0]}')"
        else:
            modelNames_t = tuple(modelNames)

        sql = """SELECT a.modelType modelType, a.modelName modelName, a.predictDir predictDir,a.dsId dsId,a.predictState predictState FROM ma_predict a
         WHERE a.modelType='%s' AND a.dsName='%s' AND a.modelName IN %s ORDER BY a.updateTime DESC""" \
              % (modelType, dataSourceName, modelNames_t)
        db_session.commit()
        return db_session.execute(sql).fetchall()

    # add by sun.jiping
    @classmethod
    def find_modelNames_by_modelType_dsName(cls, modelType, dataSourceName):
        """
        """
        sql = """SELECT a.modelType modelType, a.modelName modelName"""
        sql += """ FROM ma_predict a WHERE a.modelType='%s' AND a.dsName='%s' AND a.predictState=2 ORDER BY a.updateTime DESC
            """ % (modelType, dataSourceName)
        db_session.commit()
        return db_session.execute(sql).fetchall()

    @classmethod
    def insert(cls, trainId, dsId, modelType, modelName, dsName, predictDir="", predictState=0, state=1, mylog=None):
        """
        """
        newRecord = cls(
            trainId=trainId, dsId=dsId, modelType=modelType, modelName=modelName, dsName=dsName,
            predictDir=predictDir, predictState=predictState, state=state
        )
        try:
            db_session.add(
                newRecord
            )
            db_session.commit()

            str = "insert [ma_predict] ok...modelType={}...modelName={}...dsId={}...trainId={}".format(
                modelType, modelName, dsId, trainId
            )
            if mylog:
                mylog.info(str)
            else:
                print(str)
            return newRecord
        except Exception as e:
            str = "DB Error, insert [ma_predict]..., {}".format(e)
            if mylog:
                mylog.error(str)
            else:
                print(str)
            db_session.rollback()
            return None

    @classmethod
    def find_test(cls):
        """
        """
        sql = """SELECT a.modelType modelType, a.modelName modelName, a.predictDir predictDir,a.predictState predictState,b.modelParams4ml modelParams4ml FROM ma_predict a, ma_train b
        WHERE a.modelType='产品质量软测量' AND a.dsName='多氟多_2#_质量软测#在线数据'  AND a.modelName=b.modelName AND a.modelName IN ("质量软测量_2#", "质量软测量_2#001", "质量软测量_2#003", "质量软测量_2#004")
        ORDER BY a.updateTime DESC"""

        db_session.commit()
        return db_session.execute(sql).fetchall()


if __name__ == '__main__':
    # res = Mysql_MA_Predict.find_test()
    # for item in res:
    #     print(item.modelType, item.modelName, item.predictDir, item.modelParams4ml)

    modenames = ["质量软测量_2#B", "质量软测量_2#B_test1"]
    res = Mysql_MA_Predict.find_by_model_names("产品质量软测量", modenames, "多氟多_2#_质量软测#在线数据")
    exist_list = []
    for item in res:
        exist_list.append(item.modelName)

    new_mode_list = list(set(modenames) - set(exist_list))
    print(new_mode_list)

    if not new_mode_list:
        print("模型预测记录已存在")


    # set(res)
    # print(type(res))
    # print(res)


