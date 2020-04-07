#!/usr/bin/python
# -*- coding: utf-8 -*-
from DModel.Mysql_MA_Result import Mysql_MA_Result
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
from DPublic.MysqlDB import Base, db_session, engine
import pandas as pd
import json


class Predict_Compare_Result_Handler(DataServiceBaseHandler):
    """
        查询-预测结果
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Compare_Result.Request]...[%s]/[%s]" % (type(reqData), reqData))

        # [校验]，请求参数.
        errno, errMsg, reqDict = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["modelType", "modelNames"]
        )
        mylog.info("[Predict_Compare_Result.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        compareRes = Mysql_MA_Result.soft_result_Compare()

        if not compareRes:  # 记录不存在，返回
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "没有结果更新！"
            }))
            return

        df = pd.read_sql("""SELECT a.modelName,a.time,a.prediction,b.Sample_TestResult,c.test_code 
        FROM soft_predict_result a,lims_data b,lim_dict c WHERE a.optColid=b.DICTIONARYID AND 
        b.DICTIONARYID=c.dictionaryid AND  a.time=b.Sampling_Date ORDER BY a.time""", engine.raw_connection())

        resultList = []
        if len(df) != 0:
            for modelName in reqDict["modelNames"]:
                resultDict = {}
                resJson = df[df['modelName'] == modelName][
                    ['time', 'prediction', 'Sample_TestResult', 'test_code']].to_json(orient='records')
                resultDict['modelName'] = modelName
                resultDict['data'] = json.loads(resJson)
                resultList.append(resultDict)
        else:
            self.write(json.dumps({
                        "errorNo": -1,
                        "errorMsg": "没有数据更新！"
                    }))

        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功",
            "Result": resultList
        })
        print(data)
        self.write(data)
