#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import shutil
import traceback
import pandas as pd

from CConfig import conf


class Optim_Public_Train():
    """
    """
    @classmethod
    def create_train_dir(cls, modelType, modelName, modelParams, dsDataFileName, dsParamFileName):
        """
            创建训练目录.
            目录结构：modelType/modelName/train_data
            训练输入目录： modelType/modelName/train_input
            训练输出目录： modelType/modelName/train_result
            数据源-数据文件： modelType/modelName/train_input/dsDataFileName
            数据源-参数文件:  modelType/modelName/train_input/dsParamFileName
        """
        try:
            # 创建，[modelType]目录.
            modelTypePath = "%s/%s" % (conf.TRAIN_PATH, modelType)
            if os.path.exists(modelTypePath) is False:
                os.mkdir(modelTypePath)

            # 创建，[modelName]目录.
            modelNamePath = "%s/%s" % (modelTypePath, modelName)
            if os.path.exists(modelNamePath) is False:
                os.mkdir(modelNamePath)

            # 创建，[训练输入]目录.
            trainInputPath = "%s/%s" % (modelNamePath, conf.TRAIN_INPUT_DIR)
            if os.path.exists(trainInputPath) is False:
                os.mkdir(trainInputPath)

            # 创建，[训练输出结果]目录.
            trainResultPath = "%s/%s" % (modelNamePath, conf.TRAIN_RESULT_DIR)
            if os.path.exists(trainResultPath) is False:
                os.mkdir(trainResultPath)

            # 复制, [原始数据]文件. (dsDataFileName, dsParamFileName)
            print("[dsDataFileName]...{}...{}".format(dsDataFileName, trainInputPath))
            shutil.copy(dsDataFileName, trainInputPath)

            print("[dsParamFileName]...{}...{}".format(dsParamFileName, trainInputPath))
            shutil.copy(dsParamFileName, trainInputPath)

            # 生成, [模型参数Json]文件.
            destDataPath = "%s/%s_模型参数.json" % (trainInputPath, modelName)
            print("[destDataPath]...", destDataPath)
            with open(destDataPath, "w") as fp:
                fp.write(json.dumps(modelParams))

            # 返回.
            return modelNamePath
        except Exception as e:
            print(traceback.print_exc())
            return None


    @classmethod
    def convert_modelParams_4ml(cls, modelType, modelParams):
        """
            将模型参数转换为 算法API可用参数.
        """
        if not isinstance(modelParams, list):
            print("modelParams should be list_type............")
            return

        optColParams = None         # 优化目标
        observedColParams = None    # 工况变量
        decisionColParams = None    # 强相关操作变量
        # add by sjp for greyPredict
        adjustParam = None

        params4ml = {}
        if modelType.find("优化分析") >= 0:
            optColParams = modelParams[0]
            observedColParams = modelParams[1]
            decisionColParams = modelParams[2]

            # [优化目标]，处理
            params4ml['optCol'] = {}    # 字典.
            for x in optColParams.get("data", []):
                vKey = x.get("enCode", None)
                vOpAttr = x.get("op_attribute", None)
                vOpW = x.get("op_w", None)
                params4ml['optCol'][vKey] = {
                    "op_attribute": vOpAttr,
                    "op_w": vOpW,
                }
        elif modelType.find("软测量") >= 0:
            optColParams = modelParams[0]
            decisionColParams = modelParams[1]

            # [优化目标]，处理
            params4ml['optCol'] = []    # 列表.
            for x in optColParams.get("data", []):
                vKey = x.get("enCode", None)
                params4ml['optCol'].append(vKey)

        elif modelType.find("生产预警") >= 0:
            optColParams = modelParams[0]
            adjustParam = modelParams[1]

            # [优化目标]，处理, 根据算法参数处理，适用于只有一个目标
            for x in optColParams.get("data", []):
                vKey = x.get("enCode", None)
                maxvalue = x.get("maxvalue", None)
                minvalue = x.get("minvalue", None)
                params4ml['optCol'] = vKey
                params4ml['maxvalue'] = maxvalue
                params4ml['minvalue'] = minvalue

            # [可调参数],处理
            for x in adjustParam.get("data", []):
                if x.get("enCode", None) == "freq":
                    params4ml['freq'] = x.get("enUnit", None)
                elif x.get("enCode", None) == "History_DataLength":
                    params4ml['History_DataLength'] = x.get("enUnit", None)
                elif x.get("enCode", None) == "Predict_DataLength":
                    params4ml['Predict_DataLength'] = x.get("enUnit", None)

        # 工况变量
        if observedColParams:
            params4ml['observedCol'] = {}
            for x in observedColParams.get("data", []):
                vKey = x.get("enCode", None)
                vBias = x.get("bias", None)
                params4ml['observedCol'][vKey] = {
                    "bias": vBias,
                }
        # 强相关操作变量
        if decisionColParams:
            params4ml['decisionCol'] = []
            for x in decisionColParams.get("data", []):
                vKey = x.get("enCode", None)
                params4ml['decisionCol'].append(vKey)

        print("params4ml...........", json.dumps(params4ml))
        return json.dumps(params4ml)


    @classmethod
    def fetch_train_result(cls, fileDir, mylog, paramOriJson=None):
        """
        """
        fname = None
        for file in os.listdir(fileDir):
            print(".........", file)
            if os.path.splitext(file)[-1] == ".csv":
                fname = file
                break
        if fname is None:
            mylog.error("Could not find fname={} error.".format(fname))

        resultPath = "%s/%s" % (fileDir, fname)
        mylog.info("resultPath...........{}".format(resultPath))
        # pandas.dataFrame.
        df = pd.read_csv(resultPath, engine='python')

        # df.rename(columns={'A(%)': 'A'}, inplace = True)

        dataJsonStr = df.to_json(
            force_ascii=False
        )
        dataJsonDcit = json.loads(
            dataJsonStr
        )

        # paramOriJson.原始参数
        if paramOriJson:
            paramOriDict = json.loads(paramOriJson)
            dataJsonDcit['paramDesc'] = paramOriDict

        mylog.debug("...{}...".format(type(dataJsonDcit)), dataJsonDcit)
        return dataJsonDcit

    @classmethod
    def save_train_result_2_csv(cls, fileDir, modelName, mylog):
        """
        """
        fname = None
        for file in os.listdir(fileDir):
            print(".........", file)
            if os.path.splitext(file)[-1] == ".csv":
                fname = file
                break
        if fname is None:
            mylog.info("Could not find fname={} error.".format(fname))

        resultPath = "%s/%s" % (fileDir, fname)
        mylog.info("resultPath...........{}".format(resultPath))
        # pandas.dataFrame.
        df = pd.read_csv(resultPath, engine='python').rename(columns={"gw_id": "工况"}).drop(['concat_col_gw', 'op'],
                                                                                           axis=1)
        # print(df)
        df.to_csv(f"/root/works/web/bigdata-algorithm/apache-tomcat-7.0.78/webapps/algorithm/trainResult/{modelName}_训练结果.csv", index=False)
        return f"algorithm/trainResult/{modelName}_训练结果.csv"
