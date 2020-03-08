import pandas as pd

from DModel.Mysql_MA_Real_time import Mysql_MA_Real_time
from DPublic.MysqlDB import Base, db_session, engine
from Real_data.Dfd_data_struct import dfd_columns
import time


def read_data():
    df = pd.read_csv("/root/works/idata/ma16_data/origin_data/dfd/多氟多实时数据200116.csv")
    df.to_sql("dfd_ds_product", con=engine, if_exists="append", index=False, index_label="id")
    print("写入mysql {} 条数据".format(len(df)))


if __name__ == '__main__':
    while True:
        read_data()
        time.sleep(180)
    # read_data()