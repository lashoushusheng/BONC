#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public


class Predict_Get_DataSource_List_Handler(DataServiceBaseHandler):
    """
        获取-数据源列表
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Get_DataSource.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType"]
        )
        mylog.info("[Predict_Get_DataSource.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return


        # [Mysql]，取记录.
        rows = Mysql_MA_DataSource.find_predict_dataSourceList(
            modelType=reqDict["modelType"]
        )
        if not rows:  # 无匹配记录，返回.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "没有匹配的数据源."
            }))
            return

        # [生成]，数据源名称列表.
        dataSourceList = []
        for row in rows:
            # print(row)
            dataSourceList.append({
                "modelName": row.modelName,
                "dataSource": row.dsName
            })


        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "dataSourceList": dataSourceList,
        })

        print(data)
        self.write(data)
