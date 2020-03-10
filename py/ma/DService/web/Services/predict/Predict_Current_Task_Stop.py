#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
import os


class Predict_Current_Task_Stop_Handler(DataServiceBaseHandler):
    """
        停止当前任务
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
            paramList=["modelType", "modelName"]
        )
        mylog.info("[Predict_Commit_Task.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        val = os.popen('jps | grep maPredict | wc -l').read()  # 执行结果包含在val中

        if int(val) <= 0:
            self.write(json.dumps({"errorNo": 0, "errorMsg": "当前没有任务运行"}))

        else:
            res = os.system("jps | grep maPredict | awk '{print $1}' | xargs kill -9")
            if res == 0:
                self.write(json.dumps({"errorNo": 0, "errorMsg": "stop执行成功!"}))
            else:
                self.write(json.dumps({"errorNo": -1, "errorMsg": "stop执行失败!"}))
