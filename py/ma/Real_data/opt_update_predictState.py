#!/usr/bin/python
# -*- coding: utf-8 -*-

from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_dfd_2 import Cli_Optmi_Params_Dfd_2
from DModel.Mysql_MA_Real_time import Mysql_MA_Real_time
import time
import os


def update_predictState():
    predDsDir = Cli_Optmi_Params_Dfd_2.predDsDir
    predDsFile = Cli_Optmi_Params_Dfd_2.predDsFile
    sourceFile = f"{predDsDir}/{predDsFile}"

    inittime = time.ctime(os.path.getmtime(sourceFile))
    while True:
        time.sleep(90)
        currenttime = time.ctime(os.path.getmtime(sourceFile))
        if currenttime != inittime:
            # print("inittime {}".format(inittime))
            # print("currenttime {}".format(currenttime))
            Mysql_MA_Real_time.mysql_update_predictState(Cli_Optmi_Params_Dfd_2.modelType, Cli_Optmi_Params_Dfd_2.predDsName)
            print("更新状态")
            inittime = currenttime
        else:
            print("没有数据更新")


if __name__ == '__main__':
    update_predictState()