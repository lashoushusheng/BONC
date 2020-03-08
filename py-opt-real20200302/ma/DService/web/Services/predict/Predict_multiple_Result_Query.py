#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from CConfig import conf
from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Predict import Mysql_MA_Predict
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DService.web.Services.Optim_Public_Predict import Optim_Public_Predict
import os


class Predict_Query_multiple_Result_Handler(DataServiceBaseHandler):
    """
        查询-预测结果
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Query_Result.Request]...[%s]/[%s]" % (type(reqData), reqData))

        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "modelNames", "predictDataSourceName"]
        )
        mylog.info("[Predict_Query_Result.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        # # [Mysql]，取[ma_predict]记录.
        # predictRow = Mysql_MA_Predict.find_one(
        #     modelType=reqDict["modelType"],
        #     modelName=reqDict["modelName"],
        #     dataSourceName=reqDict["predictDataSourceName"],
        # )
        # if not predictRow:  # 记录不存在，返回
        #     self.write(json.dumps({
        #         "errorNo": -1,
        #         "errorMsg": "模型预测记录不存在异常！"
        #     }))
        #     return

        # add by sjp
        predictRows = Mysql_MA_Predict.find_by_model_names(
            modelType=reqDict["modelType"],
            modelNames=reqDict["modelNames"],
            dataSourceName=reqDict["predictDataSourceName"],
        )
        if not predictRows:  # 记录不存在，返回
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "模型预测记录不存在异常！"
            }))
            return

        Result = []
        for predictRow in predictRows:
            # [Mysql]，取[ma_train]记录.
            trainRow = Mysql_MA_Train.find_one(
                modelType=reqDict["modelType"],
                modelName=predictRow.modelName
            )
            if not trainRow:  # 记录不存在，返回
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "模型训练记录不存在异常！"
                }))
                return

            # [Mysql]，取[ma_data_source]记录.
            trainDSRow = Mysql_MA_DataSource.find_one_by_id(
                dsId=trainRow.dsId,
            )
            if not trainDSRow:  # 记录不存在，返回.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "数据源记录不存在异常！"
                }))
                return
            predictDSRow = Mysql_MA_DataSource.find_one_by_id(
                dsId=predictRow.dsId,
            )
            if not predictDSRow:  # 记录不存在，返回.
                self.write(json.dumps({
                    "errorNo": -1,
                    "errorMsg": "数据源记录不存在异常！"
                }))
                return

            if trainRow.modelType == "优化分析":
                # 判断目录是否存在
                result_dir = predictRow.predictDir + r"/predict_result/\result_2"

                if not os.path.isdir(result_dir):
                    predictResult = {"time": {}, "prediction": {}}
                else:
                    Files = os.listdir(result_dir)
                    if not Files or len(Files) < 4:
                        predictResult = {}
                    else:
                        predictResult = Optim_Public_Predict.real_compute_fetch_predict_result(
                            result1_Dir=predictRow.predictDir + r"/predict_result/\result_1",
                            result2_Dir=predictRow.predictDir + r"/predict_result/\result_2",
                            paramOriJson=trainDSRow.paramOriJson,
                            mylog=mylog
                        )

                # [返回], 给前端数据.
                data = json.dumps({
                    "errorNo": 0,
                    "errorMsg": "成功",
                    "dataSourceParams": json.loads(trainDSRow.paramsJson),
                    "modelParams": json.loads(trainRow.modelParams),
                    "predictState": int(predictRow.predictState),
                    "predictResult": predictResult
                })

                print(data)
                self.write(data)

            elif trainRow.modelType == "产品质量软测量":
                # if predictRow.predictState == 0 or predictRow.predictState == 1:
                #     predictResult = None
                #     ResultFileName = None
                #
                # else:
                #     predictResult, ResultFileName = Optim_Public_Predict.fetch_predict_result(
                #         predictRow.predictDir + r"/predict_result/\predict_result",
                #         mylog=mylog
                #     )

                # 判断目录是否存在
                result_dir = predictRow.predictDir + r"/predict_result/\predict_result"

                if not os.path.isdir(result_dir):
                    predictResult = {"time": {}, "prediction": {}}
                else:
                    Files = os.listdir(result_dir)
                    if not Files or len(Files) < 4:
                        predictResult = {"time": {}, "prediction": {}}
                    else:
                        predictResult, ResultFileName = Optim_Public_Predict.fetch_predict_result(
                            result_dir,
                            mylog=mylog
                        )
                tempResult = {
                    "modelName": predictRow.modelName,
                    "dataSourceParams": json.loads(trainDSRow.paramsJson),
                    "modelParams": json.loads(trainRow.modelParams),
                    "predictState": int(predictRow.predictState),
                    "predictResult": predictResult,
                }
                Result.append(tempResult)

        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "Result": Result
        })
        print(data)
        self.write(data)
