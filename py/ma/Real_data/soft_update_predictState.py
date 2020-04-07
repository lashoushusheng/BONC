#!/usr/bin/python
# -*- coding: utf-8 -*-

from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_dfd2 import Client_Soft_Params_Dfd1
from DModel.Mysql_MA_Real_time import Mysql_MA_Real_time
import time
import os


def update_predictState():
    predDsDir = Client_Soft_Params_Dfd1.predDsDir
    predDsFile = Client_Soft_Params_Dfd1.predDsFile
    sourceFile = f"{predDsDir}/{predDsFile}"

    inittime = time.ctime(os.path.getmtime(sourceFile))
    while True:
        time.sleep(60)
        currenttime = time.ctime(os.path.getmtime(sourceFile))
        if currenttime != inittime:
            # print("inittime {}".format(inittime))
            # print("currenttime {}".format(currenttime))
            Mysql_MA_Real_time.mysql_update_predictState(Client_Soft_Params_Dfd1.modelType, Client_Soft_Params_Dfd1.predDsName)
            print("更新状态")
            inittime = currenttime
        else:
            print("没有数据更新")


if __name__ == '__main__':
    update_predictState()