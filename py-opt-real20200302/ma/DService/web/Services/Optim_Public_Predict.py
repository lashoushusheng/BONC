#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
import traceback
import pandas as pd

from CConfig import conf


class Optim_Public_Predict():
    """
    """
    @classmethod
    def create_predict_dir(cls, modelType, modelName, dsDataFileName):
        """
            创建预测目录. 目录结构：modelType/modelName/predict_data
            预测输入目录： modelType/modelName/predict_input
            预测输出目录： modelType/modelName/predict_result
            数据源-数据文件： modelType/modelName/predict_input/dsDataFileName
        """
        try:
            # 创建，[modelType]目录.
            modelTypePath = "%s/%s" % (conf.PREDICT_PATH, modelType)
            if os.path.exists(modelTypePath) is False:
                os.mkdir(modelTypePath)

            # 创建，[modelName]目录.
            modelNamePath = "%s/%s" % (modelTypePath, modelName)
            if os.path.exists(modelNamePath) is False:
                os.mkdir(modelNamePath)

            # 创建，预测输入目录.
            predictInputPath = "%s/%s" % (modelNamePath, conf.PREDICT_INPUT_DIR)
            if os.path.exists(predictInputPath) is False:
                os.mkdir(predictInputPath)

            # 创建，预测输出目录.
            predictResultPath = "%s/%s" % (modelNamePath, conf.PREDICT_RESULT_DIR)
            if os.path.exists(predictResultPath) is False:
                os.mkdir(predictResultPath)

            # 复制, [原始数据]文件. (dsDataFileName)
            print("[dsDataFileName]...{}...{}".format(dsDataFileName, predictInputPath))
            shutil.copy(dsDataFileName, predictInputPath)

            # 返回.
            return modelNamePath
        except Exception as e:
            print(traceback.print_exc())
            return None


    @classmethod
    def fetch_predict_result(cls, fileDir, mylog):
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

        df = pd.read_csv(resultPath, engine='python')

        dataJsonStr = df.to_json(
            force_ascii=False
        )
        dataJson = json.loads(
            dataJsonStr
        )

        mylog.debug("...{}...".format(type(dataJson)), dataJson)
        return dataJson, fname


    @classmethod
    def compute_fetch_predict_result(cls, inputFile, resultDir, paramOriJson, mylog):
        """
            预测结果、输入结果，规整格式，返回给前端.
        """
        # 结果文件，转dataFrame.
        fname = None
        for file in os.listdir(resultDir):
            if os.path.splitext(file)[-1] == ".csv":
                fname = file
                break
        if fname is None:
            mylog.error("Could not find result-file in dir={} error.".format(resultDir))
        resultPath = "%s/%s" % (resultDir, fname)
        print("resultPath...{}".format(inputFile))
        dfOutput = pd.read_csv(resultPath, engine='python')
        # print(dfOutput)
        # print("*" * 100)

        # 输入文件规整.
        dfInput = pd.read_csv(inputFile, engine='python')
        print("inputFile...{}".format(inputFile))
        dfInput['time'] = dfInput['time'].apply(
            lambda x: int(time.mktime(time.strptime(x, '%Y/%m/%d %H:%M')))
        )
        # print(dfInput)
        # print("*" * 100)

        print("paramOriJson...{}".format(paramOriJson))
        oriParamDict=json.loads(paramOriJson)

        # merge，结果、输入文件.
        vResultList = []
        # 逐行处理.
        for index, oRow in dfOutput.iterrows():
            # 取结果文件[time]关键字.
            # print("2222222222222...oRow...", oRow)
            print("2222222222222...time...", oRow['time'])
            oTime = oRow['time']

            # 按time索引，过滤匹配input记录.
            iRow = dfInput[dfInput['time'] == oTime]
            # print("2222222222222...iRow...", iRow)

            if len(iRow) > 0:
                iRow = iRow.iloc[0]   # 只取第1行.
                vResultItemDict = {
                    "time": None,
                    "gw_id": None,
                    "optCol": [],
                    "paramCol": [],
                }
                # 逐列计算.
                for oClmnName in dfOutput.columns:
                    # print("2222222222222...{} | {} | {}".format(oClmnName, oRow.get(oClmnName), iRow.get(oClmnName)))
                    if oClmnName == "time":    # 时间参数.
                        vResultItemDict["time"] = {
                            "resultValue": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(oRow.get(oClmnName)))),
                            "inValue": oRow.get(oClmnName),
                        }
                    elif oClmnName == "gw_id":    # 工况变量.
                        vResultItemDict["gw_id"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oClmnName == "op":    # .
                        vResultItemDict["op"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oRow.get(oClmnName) and iRow.get(oClmnName):
                        v = oriParamDict.get(oClmnName, None)
                        if v is None:
                            continue

                        # 目标列，插入列表.
                        if v["belongCate"] == "optCol":
                            vResultItemDict["optCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                                "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                                "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                            })
                        # 参数列，插入列表.
                        elif v["belongCate"].find("observedCol") >= 0:
                            vResultItemDict["paramCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                                "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                                "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                            })

                print("2222222222222...{}".format(json.dumps(vResultItemDict)))

                # 插入, 结果集列表.
                if vResultItemDict['time']:
                    vResultList.append(vResultItemDict)
            # break

        print("2222222222222...vResultList_len={}".format(len(vResultList)))
        return vResultList

    @classmethod
    def real_compute_fetch_predict_result(cls, result1_Dir, result2_Dir, paramOriJson, mylog):
        """
            预测结果、输入结果，规整格式，返回给前端.
        """
        # 源文件，转dataFrame.
        src_fname = None
        for file in os.listdir(result1_Dir):
            if os.path.splitext(file)[-1] == ".csv":
                src_fname = file
                break

        if src_fname is None:
            mylog.error("Could not find result-file in dir={} error.".format(result1_Dir))
        src_Path = "%s/%s" % (result1_Dir, src_fname)
        print("resultPath...{}".format(src_Path))
        size = os.path.getsize(src_Path)
        if size == 0:
            return [{"time": {}, "gw_id": {}, "optCol": [], "paramCol":[]}]
        dfInput = pd.read_csv(src_Path, engine='python')
        # print(dfInput)
        # print("*" * 100)

        # 结果，转dataFrame.
        res_fname = None
        for file in os.listdir(result2_Dir):
            if os.path.splitext(file)[-1] == ".csv":
                res_fname = file
                break

        if res_fname is None:
            mylog.error("Could not find result-file in dir={} error.".format(result2_Dir))
        res_Path = "%s/%s" % (result2_Dir, res_fname)
        print("resultPath...{}".format(res_Path))
        size = os.path.getsize(res_Path)
        if size == 0:
            return [{"time": {}, "gw_id": {}, "optCol": [], "paramCol":[]}]
        dfOutput = pd.read_csv(res_Path, engine='python')
        # print(dfOutput)
        # print("*" * 100)

        print("paramOriJson...{}".format(paramOriJson))
        oriParamDict = json.loads(paramOriJson)

        # merge，结果、输入文件.
        vResultList = []
        # 逐行处理.
        for index, oRow in dfOutput.iterrows():
            # 取结果文件[time]关键字.
            print("2222222222222...oRow...", oRow)
            print("time", oRow['time'])
            oTime = oRow['time']
            print(oRow)

            # 按time索引，过滤匹配input记录.
            iRow = dfInput[dfInput['time'] == oTime]
            # print("2222222222222...iRow...", iRow)

            if len(iRow) > 0:
                iRow = iRow.iloc[0]  # 只取第1行.
                vResultItemDict = {
                    "time": None,
                    "gw_id": None,
                    "optCol": [],
                    "paramCol": [],
                }
                # 逐列计算.
                for oClmnName in dfOutput.columns:
                    # print("2222222222222...{} | {} | {}".format(oClmnName, oRow.get(oClmnName), iRow.get(oClmnName)))
                    if oClmnName == "time":  # 时间参数.
                        vResultItemDict["time"] = {
                            "resultValue": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(oRow.get(oClmnName)))),
                            "inValue": oRow.get(oClmnName),
                        }
                    elif oClmnName == "gw_id":  # 工况变量.
                        vResultItemDict["gw_id"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oClmnName == "op":  # .
                        vResultItemDict["op"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oClmnName in ["CZ3_OP1", "CZ3_OP2", "CZ3_OP3"]:
                        v = oriParamDict.get(oClmnName, None)
                        if v is None:
                            continue
                        # 目标列，插入列表.
                        if v["belongCate"] == "optCol":
                            vResultItemDict["optCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                            })

                    # elif oRow.get(oClmnName) and iRow.get(oClmnName):
                    else:
                        v = oriParamDict.get(oClmnName, None)
                        if v is None:
                            continue

                        # # 目标列，插入列表.
                        # if v["belongCate"] == "optCol":
                        #     vResultItemDict["optCol"].append({
                        #         "enCode": oClmnName,
                        #         "cnCode": v["cnCode"],
                        #         "unit": v["enUnit"],
                        #         "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                        #         "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                        #         "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                        #     })
                        # 参数列，插入列表.
                        if v["belongCate"].find("observedCol") >= 0:
                            vResultItemDict["paramCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                                "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                                "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                            })

                print("2222222222222...{}".format(json.dumps(vResultItemDict)))

                # 插入, 结果集列表.
                if vResultItemDict['time']:
                    vResultList.append(vResultItemDict)
            # break

        print("2222222222222...vResultList_len={}".format(len(vResultList)))
        return vResultList

