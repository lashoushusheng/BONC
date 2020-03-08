#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from CConfig import conf
from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DModel.Mysql_MA_Train import Mysql_MA_Train
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DService.web.Services.Optim_Public_Train import Optim_Public_Train


class Train_Query_Result_Handler(DataServiceBaseHandler):
    """
        查询-训练结果
    """
    def post(self):
        """
        """
        global trainResult0000
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Train_Query_Result.Request]...[%s]/[%s]" % (type(reqData), reqData))


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
                "errorMsg": "训练记录不存在异常！"
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

        if trainRow.modelType == "优化分析":
            # [训练结果查询]，未完成，或处理中。[0未开始，1进行中，2已完成]
            if trainRow.trainState == 0 or trainRow.trainState == 1:
                trainResult1 = None
                trainResult2 = None
                trainResult3 = None
            else:
                if conf.OS_TYPE == "window":
                    # trainResult1 = None
                    # trainResult3 = None
                    trainResult1 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/result_1", mylog=mylog)
                    trainResult2 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/result_2", paramOriJson=dsRow.paramOriJson, mylog=mylog)
                    trainResult3 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/result_3", paramOriJson=dsRow.paramOriJson, mylog=mylog)
                else:
                    trainResult1 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/\result_1", mylog=mylog)
                    trainResult2 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/\result_2", paramOriJson=dsRow.paramOriJson, mylog=mylog)
                    trainResult3 = Optim_Public_Train.fetch_train_result(
                        fileDir=trainRow.trainDir + r"/train_result/\result_3", paramOriJson=dsRow.paramOriJson, mylog=mylog)

            # [返回], 给前端数据.
            data = json.dumps({
                "errorNo": 0,
                "errorMsg": "成功",
                "dataSourceParams": json.loads(dsRow.paramsJson),
                "modelParams": json.loads(trainRow.modelParams),
                "trainState": int(trainRow.trainState),
                "trainResult1": trainResult1,
                "trainResult2": trainResult2,
                "trainResult3": trainResult3,
            })

            mylog.debug(data)
            self.write(data)

        elif trainRow.modelType == "产品质量软测量":
            if trainRow.trainState == 0 or trainRow.trainState == 1:
                trainResult = None

            else:
                trainResult = Optim_Public_Train.fetch_train_result(
                    fileDir=trainRow.trainDir + r"/train_result/\predict_xiaoguo.csv", mylog=mylog)

            # [返回], 给前端数据.
            data = json.dumps({
                "errorNo": 0,
                "errorMsg": "成功",
                "dataSourceParams": json.loads(dsRow.paramsJson),
                "modelParams": json.loads(trainRow.modelParams),
                "trainState": int(trainRow.trainState),
                "trainResult": trainResult
            })

            mylog.debug(data)
            self.write(data)

        elif trainRow.modelType == "生产预警分析":
            if trainRow.trainState == 0 or trainRow.trainState == 1:
                predictSucessSta = None
                TimeSeq = None

            else:
                predictSucessSta = Optim_Public_Train.fetch_train_result(
                    fileDir=trainRow.trainDir + r"/train_result/predictSucessSta", mylog=mylog)
                TimeSeq = Optim_Public_Train.fetch_train_result(
                    fileDir=trainRow.trainDir + r"/train_result/TimeSeq", mylog=mylog)

            # [返回], 给前端数据.
            data = json.dumps({
                "errorNo": 0,
                "errorMsg": "成功",
                "dataSourceParams": json.loads(dsRow.paramsJson),
                "modelParams": json.loads(trainRow.modelParams),
                "trainState": int(trainRow.trainState),
                "predictSucessSta": predictSucessSta,
                "TimeSeq": TimeSeq
            })

            mylog.debug(data)
            self.write(data)