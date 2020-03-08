#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public


class Train_Choiced_DataSource_Handler(DataServiceBaseHandler):
    """
        选中-数据源
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Train_Choiced_DataSource.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "dataSourceName"]
        )
        mylog.info("[Train_Choiced_DataSource.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        # [Mysql]，取[ma_train]modeName列表.
        modelNameList = []
        modelNameRows = Mysql_MA_Train.find_modelNames_by_dataSouce(
            modelType=reqDict["modelType"],
            dataSourceName=reqDict["dataSourceName"],
        )
        print("..........", len(modelNameRows))
        if modelNameRows:
            for row in modelNameRows:
                # print("row...", row)
                modelNameList.append(row.modelName)


        # [Mysql]，取数据源参数.
        paramRow = Mysql_MA_DataSource.find_one_by_name(
            dsName=reqDict["dataSourceName"],
        )
        if not paramRow:  # 无匹配记录，返回.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "获取数据源参数异常！"
            }))
            return


        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "dataSourceParmas": json.loads(paramRow.paramsJson),
            "modelNameList": modelNameList
        })

        print(data)
        self.write(data)
