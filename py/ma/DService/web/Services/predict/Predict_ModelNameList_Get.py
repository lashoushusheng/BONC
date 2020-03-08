#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sun.jiping

import json

from DModel.Mysql_MA_Predict import Mysql_MA_Predict
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public


class Predict_Get_ModelName_List_Handler(DataServiceBaseHandler):
    """
        获取-模型名称列表
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Get_ModelNameList.Request]...[%s]/[%s]" % (type(reqData), reqData))

        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData, paramList=["modelType", "predictDataSourceName"]
        )

        mylog.info("[Predict_Get_ModelNameList.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        # [Mysql]，取[ma_predict]记录.
        predictRow = Mysql_MA_Predict.find_modelNames_by_modelType_dsName(
            modelType=reqDict["modelType"], dataSourceName=reqDict["predictDataSourceName"]
        )

        modelNameList = []
        if predictRow:
            for row in predictRow:
                modelNameList.append(row.modelName)

        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "modelNameList":  modelNameList
        })

        print(data)
        self.write(data)
