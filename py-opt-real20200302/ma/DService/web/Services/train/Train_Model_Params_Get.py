#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public


class Train_Get_Model_Params_Handler(DataServiceBaseHandler):
    """
        获取-模型参数
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Train_Get_Model_Params.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "modelName"]
        )
        mylog.info("[Train_Get_Model_Params.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return


        # [Mysql]，取[ma_train]记录.
        trainRow = Mysql_MA_Train.find_one(
            modelType=reqDict["modelType"],
            modelName=reqDict["modelName"]
        )
        if not trainRow:  # 记录不存在，返回
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "模型记录不存在异常！"
            }))
            return

        # [Mysql]，取[ma_data_source]记录.
        dsRow = Mysql_MA_DataSource.find_one_by_id(
            dsId=trainRow.dsId,
        )
        if not dsRow:  # 记录不存在，返回.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "数据源记录不存在异常！"
            }))
            return


        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "dataSourceParams":  json.loads(dsRow.paramsJson),
            "modelParams": json.loads(trainRow.modelParams),
            "trainState": int(trainRow.trainState)
        })

        print(data)
        self.write(data)
