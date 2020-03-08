#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public


class Train_Get_ModelNameList_Handler(DataServiceBaseHandler):
    """
        获取-模型参数
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Train_Get_ModelNameList.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData, paramList=["modelType"]
        )
        mylog.info("[Train_Get_ModelNameList.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return


        # [Mysql]，取[ma_train]记录.
        trainRow = Mysql_MA_Train.find_modelNames_by_modelType(
            modelType=reqDict["modelType"]
        )
        # modify @2019-11-25，没有匹配modelName返回空列表.
        # if not trainRow:  # 记录不存在，返回
        #     self.write(json.dumps({
        #         "errorNo": -1,
        #         "errorMsg": "模型名称不存在异常！"
        #     }))
        #     return

        modelNameList = []
        if trainRow:
            for row in trainRow:
                modelNameList.append(row.modelName)

        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "modelNameList":  modelNameList
        })

        print(data)
        self.write(data)
