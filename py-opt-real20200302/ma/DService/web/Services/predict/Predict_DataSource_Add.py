#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from DModel.Mysql_MA_DataSource import Mysql_MA_DataSource
from DService.web.Services import DataServiceBaseHandler, mylog
from DService.web.Services.Optim_Public import Optim_Public
import pandas as pd
from DPublic.MysqlDB import Base, db_session, engine
from Real_data.Dfd_data_struct import dfd_columns


class Predict_Add_DataSource_Handler(DataServiceBaseHandler):
    """
        数据源-添加
    """
    def post(self):
        """
        """
        self.set_post_header()          # [设置]，请求头.
        reqData = self.request.body     # [取]，请求参数.
        mylog.info("[Predict_Add_DataSource.Request]...[%s]/[%s]" % (type(reqData), reqData))


        # [校验]，请求参数.
        errno, errMsg, reqDict = self.verify_request(
            reqData=reqData
        )
        mylog.info("[Predict_Add_DataSource.Verify]...errno=[%s]...errMsg=[%s]...reqDict=[%s]" % (
            errno, errMsg, reqDict
        ))
        if errno < 0:   # 校验异常，返回.
            self.write(json.dumps({"errorNo": errno, "errorMsg": errMsg}))
            return

        # [Mysql]，判断[ma_data_source]记录是否存在.
        row = Mysql_MA_DataSource.find_one_by_name(
            dsName = reqDict.get('dataSourceName')
        )
        if row:  # 记录已存在，返回
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "该数据源已存在！"
            }))
            return

        # [Mysql]，插入[ma_data_source]记录.
        row = Mysql_MA_DataSource.insert(
            modelType=reqDict.get('modelType'),
            dsName=reqDict.get('dataSourceName'),
            dsDesc=reqDict.get('dataSourceDesc'),
            useType=2,      # 用途类型。1训练，2预测
            dsDir=reqDict.get('dataSourceDir'),
            dsFile=reqDict.get('dataFileName'),
            mylog=mylog
        )
        if not row:   # 插入Mysql，异常.
            self.write(json.dumps({
                "errorNo": -1,
                "errorMsg": "Mysql插入失败！"
            }))
            return

        # [返回], 返回给前端数据.
        data = json.dumps({
            "errorNo": 0,
            "errorMsg": "成功"
        })

        print(data)
        self.write(data)

    def verify_request(self, reqData):
        """
            校验, 请求数据.
        """
        result = Optim_Public.verify_request(
            reqData=reqData,
            paramList=["dataSourceName", "dataSourceDir", "dataFileName", "modelType"]
        )
        if result[0] < 0:   # 如果errorNo < 0， 返回.
            return result

        reqDict = json.loads(reqData)

        # 数据源目录, 检查目录是否存在.
        dataSourceDir = reqDict.get('dataSourceDir')
        if os.path.exists(dataSourceDir)  is False:
            return (-1, "请求异常，[dataSourceDir]路径不存在！[{}]".format(dataSourceDir), None)

        # 数据源文件，检查文件是否存在.
        dataFileName = reqDict.get('dataFileName')
        fpath = "%s/%s" %(dataSourceDir, dataFileName)
        if os.path.exists(fpath) is False:
            return (-1, "请求异常，[dataFileName]路径不存在！[{}]".format(fpath), None)

        return result
