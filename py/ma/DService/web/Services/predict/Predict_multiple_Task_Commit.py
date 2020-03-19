#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Predict import Mysql_MA_Predict
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DService.web.Services.Optim_Public_Predict import Optim_Public_Predict
from CConfig import conf
import os


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

        # add by sip
        res = Mysql_MA_Predict.find_by_model_names(
            modelType=reqDict["modelType"],
            modelNames=reqDict["modelNames"],
            dataSourceName=reqDict["predictDataSourceName"],
        )

        # 将已经存在的模型名称存入列表
        exist_list = []
        for item in res:
            exist_list.append(item.modelName)

        # 新建模型名称列表
        new_mode_list = list(set(reqDict["modelNames"]) - set(exist_list))
        print(new_mode_list)

        # 没有新模型，直接启动算法进行计算
        if not new_mode_list:
            self.start_compute_via_modeNamelist(reqDict["modelType"], reqDict["modelNames"])
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

            # # [创建]，目录
            # predictDir = Optim_Public_Predict.create_predict_dir(
            #     modelType=reqDict.get('modelType'),
            #     modelName=modeName,
            #     dsDataFileName="%s/%s" % (dsRow.dsDir, dsRow.dsFile),
            # )
            # if predictDir is None:  # 创建目录，异常.
            #     self.write(json.dumps({
            #         "errorNo": -1,
            #         "errorMsg": "创建预测目录异常！"
            #     }))
            #     return

            # [插入]，Mysql记录.
            print("dsId={}...trainId={}".format(dsRow.id, trainRow.id))
            row = Mysql_MA_Predict.insert(
                trainId=trainRow.id,
                dsId=dsRow.id,
                modelType=reqDict.get('modelType'),
                modelName=modeName,
                dsName=dsRow.dsName,
                predictState=0,     # 0未开始，1进行中，2已完成
                mylog=mylog
            )
            if not row:  # 插入Mysql，异常.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "Mysql插入失败！"
                }))
                return

        # 启动算法进行计算
        self.start_compute_via_modeNamelist(reqDict["modelType"], reqDict["modelNames"])

    def start_compute_via_modeNamelist(self, modelType, modelNames):
        """
        :param modelType:
        :param modelNames:
        :return:
        """
        # 将名称列表转换成字符串，作为算法执行的参数
        modelNames_2_str = " ".join(modelNames)
        # 检查当前是否有任务在执行
        val = os.popen('jps | grep maPredict | wc -l').read()  # 执行结果包含在val中
        if int(val) > 0:
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "当前有任务在运行，无法提交！"
            }))
            return

        res = os.system(f"nohup java -jar {conf.PREDICT_JAR_DIR}/{conf.predictTypeDict.get(modelType)}.jar {modelType} {modelNames_2_str} > {conf.PREDICT_OUT_DIR}/{conf.predictTypeDict.get(modelType)} 2>&1 &")
        if res == 0:
            self.write(json.dumps({
                "errorNo": 0,
                "errorMsg": "分析任务提交成功！"
            }))
        else:
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "分析任务提交失败！"
            }))
