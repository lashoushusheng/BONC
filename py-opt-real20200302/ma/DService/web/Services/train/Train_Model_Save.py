#!/usr/bin/python
# -*- coding: utf-8 -*-
import decimal
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DService.web.Services.Optim_Public_Train import Optim_Public_Train


class Train_Save_Model_Handler(DataServiceBaseHandler):
    """
        保存模型
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Train_Save_Model.Request]...{}...{}".format(type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "dataSourceName", "modelName", "modelParams"]
        )
        mylog.info("[Train_Save_Model.Verify]...errno=[{}]...errMsg=[{}]...reqDict=[{}]".format(
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        # [校验], [优化分析]“op_w”权重值之和应该是1.
        if reqDict["modelType"] == "优化分析":
            sumVal = self.verify_op_w(modelParams=reqDict["modelParams"])
            if sumVal != 1:
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "(优化目标)权重值之和应该等于1！"
                }))
                return

        # [Mysql]，[ma_train]表modelName记录是否存在.
        row = Mysql_MA_Train.find_one(
            modelType=reqDict["modelType"],
            modelName=reqDict["modelName"]
        )
        if row:  # 记录已存在，返回
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "模型名称已存在！"
            }))
            return

        # [Mysql]，取[ma_data_source]数据源记录.
        dsRow = Mysql_MA_DataSource.find_one_by_name(
            dsName=reqDict["dataSourceName"],
        )
        if not dsRow:  # 无匹配记录，返回.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "获取数据源异常！"
            }))
            return


        # [创建]，训练目录
        trainDir = Optim_Public_Train.create_train_dir(
            modelType=reqDict.get('modelType'),
            modelName=reqDict.get('modelName'),
            modelParams=reqDict.get("modelParams"),
            dsDataFileName = "%s/%s" % (dsRow.dsDir, dsRow.dsFile),
            dsParamFileName = "%s/%s" % (dsRow.dsDir, dsRow.paramsFile),
        )
        if trainDir is None:  # 创建目录，异常.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "创建训练目录异常！"
            }))
            return


        # [插入]，Mysql记录.
        # print(dsRow.id)
        # 将模型参数转换为 算法API可用参数.
        modelParams4ml = Optim_Public_Train.convert_modelParams_4ml(
            modelType=reqDict.get('modelType'),
            modelParams=reqDict.get('modelParams')
        )
        print("...........", modelParams4ml)
        # 插入DB.
        row = Mysql_MA_Train.insert(
            modelType=reqDict.get('modelType'),
            modelName=reqDict.get('modelName'),
            dsId=dsRow.id,
            modelParams=json.dumps(reqDict.get('modelParams')),
            modelParams4ml=modelParams4ml,
            trainDir=trainDir,
            trainState=0,  # 0未开始，1进行中，2已完成
            mylog=mylog
        )
        if not row:  # 插入Mysql，异常.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "Mysql插入失败！"
            }))
            return

        # [返回], 给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功"
        })

        print(data)
        self.write(data)


    def verify_op_w(self, modelParams):
        """
            [校验], “op_w”权重值之和应该是1
        """
        opwList = []
        for x in modelParams:
            if x.get("enStep", None) == "optCol":
                y = x.get("data", None)
                if y:
                    for z in y:
                        opwList.append(z.get("op_w", 0))
        print("opwList...", opwList)

        sumVal = decimal.Decimal("0")
        if opwList and len(opwList) > 0:
            for x in opwList:
                sumVal += decimal.Decimal(x)
        print("opwList...sumVal..", sumVal)

        return sumVal
