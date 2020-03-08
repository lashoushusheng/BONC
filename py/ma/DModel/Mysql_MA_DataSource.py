# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from DPublic.MysqlDB import Base, db_session


class Mysql_MA_DataSource(Base):
    """
    """
    __tablename__ = 'ma_data_source'

    id = Column(Integer, primary_key=True)

    dsName = Column(String)
    dsType = Column(Integer)        # 数据源类型。1文件，2数据库
    dsDesc = Column(String)
    useType = Column(Integer)       # 用途类型。1训练，2预测
    modelType = Column(String)      # 模型类型

    dsDir = Column(String)
    dsFile = Column(String)

    paramsFile = Column(String)
    paramOriJson = Column(String)
    paramsJson = Column(String)

    state = Column(Integer)

    def __init__(self, modelType, dsName, dsDesc, useType, dsDir, dsFile,
                 paramsFile, paramOriJson, paramsJson, dsType=1, state=1):
        """
        """
        self.modelType = modelType

        self.dsName = dsName
        self.dsDesc = dsDesc
        self.useType = useType

        self.dsDir = dsDir
        self.dsFile = dsFile

        if paramsFile:
            self.paramsFile = paramsFile
        if paramOriJson:
            self.paramOriJson = paramOriJson
        if paramsJson:
            self.paramsJson = paramsJson

        self.dsType = dsType
        self.state = state


    @classmethod
    def find_one_by_id(cls, dsId):
        db_session.commit()
        return db_session.query(cls).filter(
            cls.id == dsId,
            cls.state == 1
        ).first()


    @classmethod
    def find_one_by_name(cls, dsName):
        db_session.commit()
        return db_session.query(cls).filter(
            cls.dsName == dsName,
            cls.state == 1
        ).first()


    @classmethod
    def find_all(cls, useType, modelType):
        db_session.commit()
        return db_session.query(cls).filter(
            cls.state == 1,
            cls.useType == useType,
            cls.modelType == modelType
        ).all()


    @classmethod
    def find_predict_dataSourceList(cls, modelType):
        """
        """
        sql = """SELECT a.modelType modelType, b.dsName dsName, a.modelName modelName"""
        # sql += """ FROM ma_train a, ma_data_source b
        #         WHERE a.dsId=b.id AND a.modelType=b.modelType AND a.modelType='%s'
        #             AND b.useType=2 AND a.state=1 AND b.state=1
        #         ORDER BY a.modelName, a.updateTime DESC
        #     """ % (modelType)
        sql += """ FROM ma_train a, ma_data_source b
                WHERE a.modelType=b.modelType AND a.modelType='%s'
                    AND b.useType=2 AND a.state=1 AND b.state=1
                ORDER BY a.modelName, a.updateTime DESC
            """ % (modelType)
        print("sql...",sql)
        db_session.commit()
        return db_session.execute(sql).fetchall()


    @classmethod
    def insert(cls, modelType, dsName, dsDesc, useType, dsDir, dsFile, dsType=1,
               paramsFile=None, paramOriJson=None, paramsJson=None, state=1, mylog=None):
        """
        """
        newRecord = cls(
            modelType=modelType, dsName=dsName, dsDesc=dsDesc, useType=useType,
            dsDir=dsDir, dsFile=dsFile, dsType=dsType,
            paramsFile=paramsFile, paramOriJson=paramOriJson, paramsJson=paramsJson, state=state,
        )
        try:
            db_session.add(
                newRecord
            )
            db_session.commit()

            str = "insert [ma_data_source] ok...dsName={}".format(dsName)
            if mylog:
                mylog.info(str)
            else:
                print(str)
            return newRecord
        except Exception as e:
            str = "DB Error, insert [ma_data_source]..., {}".format(e)
            if mylog:
                mylog.error(str)
            else:
                print(str)
            db_session.rollback()
            return None
