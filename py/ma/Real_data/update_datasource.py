import pandas as pd

from DModel.Mysql_MA_Real_time import Mysql_MA_Real_time
from DPublic.MysqlDB import Base, db_session, engine
from Real_data.Dfd_data_struct import dfd_columns
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_dfd import Client_Soft_Params_Dfd1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_dfd_2 import Cli_Optmi_Params_Dfd1
import time
import os

soft_predDsDir = Client_Soft_Params_Dfd1.predDsDir
soft_predDsFile = Client_Soft_Params_Dfd1.predDsFile

opt_predDsDir = Cli_Optmi_Params_Dfd1.predDsDir
opt_predDsFile = Cli_Optmi_Params_Dfd1.predDsFile


def data_deal():

    cnx = engine.raw_connection()

    data = pd.read_sql('SELECT * FROM dfd_ds_product limit 45', cnx)
    if not data.empty:
        data.to_csv(f"{soft_predDsDir}/{soft_predDsFile}", sep=",", index=False,
                columns=dfd_columns)

        data.to_csv(f"{opt_predDsDir}/{opt_predDsFile}", sep=",", index=False,
                columns=dfd_columns)

        data[dfd_columns].to_sql("dfd_ds_history", con=engine, if_exists="append", index=False)
        Mysql_MA_Real_time.delete("dfd_ds_product", len(data)*2)
        # Mysql_MA_Real_time.reset_id("dfd_ds_product")
        print("更新 {} 条数据".format(len(data)))
        return data.to_json()
    else:
        print("没有数据可以更新")


if __name__ == '__main__':
    count = 0
    while True:
        data_deal()
        time.sleep(90)

    # cnx = engine.raw_connection()
    #
    # data = pd.read_sql('SELECT * FROM dfd_ds_product limit 90', cnx)
    # print(len(data))
    #
    # data.to_csv(f"{opt_predDsDir}/{opt_predDsFile}", sep=",", index=False,
    #             columns=dfd_columns)
    #
    # print(f"{opt_predDsDir}/{opt_predDsFile}")
