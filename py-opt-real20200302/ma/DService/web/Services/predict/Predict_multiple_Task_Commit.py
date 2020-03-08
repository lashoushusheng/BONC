#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Predict import Mysql_MA_Predict
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DService.web.Services.Optim_Public_Predict import Optim_Public_Predict


class Predict_Commit_multiple_Task_Handler(DataServiceBaseHandler):
    """
        保存模型
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Commit_Task.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "modelNames", "predictDataSourceName"]
        )
        mylog.info("[Predict_Commit_Task.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return


        # # [Mysql]，[ma_predict]表记录是否存在.
        # row = Mysql_MA_Predict.find_one(
        #     modelType=reqDict["modelType"],
        #     modelName=reqDict["modelName"],
        #     dataSourceName=reqDict["predictDataSourceName"],
        # )
        #
        # if row:  # 记录已存在，返回
        #     self.write(json.dumps({
        #         "errorNo": row.predictState,
        #         "errorMsg": "模型预测记录已存在！"
        #     }))
        #     return

        # add by sip
        res = Mysql_MA_Predict.find_by_model_names(
            modelType=reqDict["modelType"],
            modelNames=reqDict["modelNames"],
            dataSourceName=reqDict["predictDataSourceName"],
        )

        exist_list = []
        for item in res:
            exist_list.append(item.modelName)

        new_mode_list = list(set(reqDict["modelNames"]) - set(exist_list))
        print(new_mode_list)

        if not new_mode_list:
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "模型预测记录已存在,没有新任务要提交！"
            }))
            return

        for modeName in new_mode_list:
            # [Mysql]，取[ma_data_source]数据源记录.
            dsRow = Mysql_MA_DataSource.find_one_by_name(
                dsName=reqDict["predictDataSourceName"],
            )
            if not dsRow:  # 无匹配记录，返回.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "获取数据源记录异常！"
                }))
                return

            # [Mysql]，取[ma_train]数据源记录.
            trainRow = Mysql_MA_Train.find_one(
                modelType=reqDict["modelType"],
                modelName=modeName,
            )
            if not trainRow:  # 无匹配记录，返回.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "获取模型训练记录异常！"
                }))
                return


            # [创建]，目录
            predictDir = Optim_Public_Predict.create_predict_dir(
                modelType=reqDict.get('modelType'),
                modelName=modeName,
                dsDataFileName="%s/%s" % (dsRow.dsDir, dsRow.dsFile),
            )
            if predictDir is None:  # 创建目录，异常.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "创建预测目录异常！"
                }))
                return

            # [插入]，Mysql记录.
            print("dsId={}...trainId={}".format(dsRow.id, trainRow.id))
            row = Mysql_MA_Predict.insert(
                trainId=trainRow.id,
                dsId=dsRow.id,
                modelType=reqDict.get('modelType'),
                modelName=modeName,
                dsName=dsRow.dsName,
                predictDir=predictDir,
                predictState=0,     # 0未开始，1进行中，2已完成
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
            "errorMsg": "成功",
            "newtask": new_mode_list
        })

        print(data)
        self.write(data)
