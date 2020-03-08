# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from DPublic.MysqlDB import Base, db_session


class Mysql_MA_Train(Base):
    """
    """
    __tablename__ = 'ma_train'

    id = Column(Integer, primary_key=True)

    modelType = Column(String)
    modelName = Column(String)

    dsId = Column(Integer)
    modelParams = Column(String)     # 模型参数(前端)
    modelParams4ml = Column(String)  # 模型参数(算法)

    trainDir = Column(String)
    trainState = Column(Integer)    # 0未开始，1进行中，2已完成
    trainBeginTime = Column(Integer)
    trainEndTime = Column(Integer)

    state = Column(Integer)


    def __init__(self, modelType, modelName, dsId, modelParams, modelParams4ml, trainDir, trainState=0, state=1):
        self.modelType = modelType
        self.modelName = modelName
        self.dsId = dsId

        self.modelParams = modelParams
        self.modelParams4ml = modelParams4ml

        self.trainDir = trainDir
        self.trainState = trainState
        self.state = state


    @classmethod
    def find_one(cls, modelType, modelName):
        db_session.commit()
        return db_session.query(cls).filter(
            cls.modelType == modelType,
            cls.modelName == modelName
        ).first()


    @classmethod
    def find_modelNames_by_dataSouce(cls, modelType, dataSourceName):
        """
        """
        sql = """SELECT a.modelType modelType, b.dsName dsName, a.modelName modelName"""
        sql += """ FROM ma_train a, ma_data_source b
                WHERE a.dsId=b.id AND a.modelType='%s' AND b.dsName='%s'
                ORDER BY a.updateTime DESC
            """ % (modelType, dataSourceName)
        db_session.commit()
        return db_session.execute(sql).fetchall()


    @classmethod
    def find_modelNames_by_modelType(cls, modelType):
        """
        """
        sql = """SELECT a.modelType modelType, a.modelName modelName"""
        sql += """ FROM ma_train a WHERE a.modelType='%s' ORDER BY a.updateTime DESC
            """ % (modelType)
        db_session.commit()
        return db_session.execute(sql).fetchall()

    @classmethod
    def find_all_dataSource(cls, modelType, modelName):
        """
        """
        sql = """SELECT dataSourceName"""
        sql += """ FROM ma_train WHERE modelType='%s'  AND modelName='%s' 
            """ % (modelType, modelName)
        db_session.commit()
        return db_session.execute(sql).fetchall()


    @classmethod
    def insert(cls, modelType, modelName, dsId, modelParams, modelParams4ml,
               trainDir, trainState=0, state=1, mylog=None):
        """
        """
        newRecord = cls(
            modelType=modelType, modelName=modelName, dsId=dsId,
            modelParams=modelParams, modelParams4ml=modelParams4ml,
            trainDir=trainDir, trainState=trainState, state=state
        )
        try:
            db_session.add(
                newRecord
            )
            db_session.commit()

            str = "insert [ma_train] ok...modelType={}...modelName={}...dsId={}".format(
                modelType, modelName, dsId
            )
            if mylog:
                mylog.info(str)
            else:
                print(str)
            return newRecord
        except Exception as e:
            str = "DB Error, insert [ma_train]..., {}".format(e)
            if mylog:
                mylog.error(str)
            else:
                print(str)
            db_session.rollback()
            return None
