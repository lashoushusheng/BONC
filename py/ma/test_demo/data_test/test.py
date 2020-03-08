import pandas as pd

from DModel.Mysql_MA_Real_time import Mysql_MA_Real_time
from DPublic.MysqlDB import Base, db_session, engine
from test_demo.data_test.columns import columns,soft_columns
import time
import os


def count():
    sql = "SELECT count(*) FROM dfd_ds_product"
    db_session.commit()
    return db_session.execute(sql).fetchone()[0]

readfile = "/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data/2号软测量预测数据1.csv"
writefile = "/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data/2号软测量预测数据2.csv"

def read_data():
    df = pd.read_csv(readfile)
    df.to_sql("dfd_ds_product", con=engine, if_exists="append", index=False, index_label="id")


def data_deal():
    cnx = engine.raw_connection()
    data = pd.read_sql('SELECT * FROM dfd_ds_product limit 50', cnx)
    if not data.empty:
        data.to_csv(writefile, sep=",", index=False,
                columns=columns)
        data[columns].to_sql("dfd_ds_history", con=engine, if_exists="append", index=False)
        Mysql_MA_Real_time.delete("dfd_ds_product", len(data))
        # Mysql_MA_Real_time.reset_id("dfd_ds_product")
        # print(data)
        return data.to_json()


if __name__ == '__main__':
    count = 0
    # while True:
    #     data_deal()
    #     count += 1
    #     print(count)
    #     print(time.ctime(os.path.getmtime(writefile)))
    #     time.sleep(5)

    # while True:
    #     read_data()
    #     count += 1
    #     print(count)
    #     time.sleep(2)
    res = pd.read_csv("/root/works/src/git_test/rtc/poc_MAnalysis/py/ma/test_demo/data_test/多氟多实时数据200116.csv")
    print(res)
    res.to_csv("2号软测量预测数据.csv", columns=soft_columns, index=False)

