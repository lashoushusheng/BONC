# -*- coding: utf-8 -*-
from DPublic.MysqlDB import Base, db_session


class Mysql_MA_Real_time(object):

    def __init__(self):
        pass

    @classmethod
    def count(cls, tb_name):
        sql = f"SELECT count(*) FROM {tb_name}"
        db_session.commit()
        return db_session.execute(sql).fetchone()[0]

    @classmethod
    def reset_id(cls, tb_name, id=1):
        sql = f"ALTER TABLE {tb_name} AUTO_INCREMENT={id};"
        db_session.execute(sql)
        db_session.commit()

    @classmethod
    def delete(cls, tb_name, nums):
        sql = f"DELETE FROM {tb_name} LIMIT {nums};"
        db_session.execute(sql)
        db_session.commit()

    @classmethod
    def mysql_update_predictState(cls, modelType, dsName):
        sql = f"""UPDATE ma_predict a,ma_data_source b SET a.predictState=0 """ \
              f"""WHERE a.predictState IN (-1,2) AND a.modelType="{modelType}" AND a.dsName="{dsName}" AND a.dsId=b.id;"""
        db_session.execute(sql)
        db_session.commit()


if __name__ == '__main__':
    test = Mysql_MA_Real_time()
    print(test.count("dfd_ds_product"))
    # test.reset_id("dfd_ds_product")
    # test.delete("dfd_ds_product", 20)

