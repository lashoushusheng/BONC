#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import chardet
import pandas as pd


class Optim_Public():
    """
    """
    @classmethod
    def verify_request(cls, reqData, paramList):
        """
            校验, 请求数据.
        """
        if not reqData:
            return (-1, "请求异常，数据不能为空！", None)

        reqDict = json.loads(reqData)

        for param in paramList:
            val = reqDict.get(param, None)
            if not val:
                return (-1, "请求异常，[{}]关键词, 不能为空！".format(param), None)

        return (0, "", reqDict)



    @classmethod
    def create_params_json(cls, fileDir, fileName):
        """
            更加数据源参数文件，生成数据源参数Json字符串.
        """
        fpath = "%s/%s" % (fileDir, fileName)

        # 判断文件字符集.
        with open(fpath, "rb") as f:
            msg = f.read()
            result = chardet.detect(msg)
            charset = result['encoding']
            print("charset...", charset)
        if charset == 'GB2312':
            df = pd.read_csv(fpath, engine='python')
        else:
            df = pd.read_csv(fpath, engine='python', encoding='utf-8')

        # df = df.dropna(axis=1)     # 删除空行.
        # df.fillna(0)
        # 取列名.
        print("columns.....", df.columns)
        # print(clm1, type(clm1))

        # 生成参数params字典.
        paramDict = {}
        paramOriDict = {}

        # 取列名.
        clmCnCode = str(df.columns[0])                      # 中文名
        vClmCnCode = clmCnCode.split("(")[0].strip("\n")
        clmEnCode = str(df.columns[1])                      # 英文名
        vClmEnCode = clmEnCode.split("(")[0].strip("\n")
        clmIsParam = str(df.columns[2])                     # 是否是参数,1是/0不是
        vClmIsParam = clmIsParam.split("(")[0].strip("\n")
        clmCate = str(df.columns[3])                        # 归属类别
        vClmCate = clmCate.split("(")[0].strip("\n")
        clmUnit = str(df.columns[4])                        # 单位
        vClmUnit = clmUnit.split("(")[0].strip("\n")
        clmMaxvalue = str(df.columns[5])  # 上限值
        vClmMaxvalue = clmMaxvalue.split("(")[0].strip("\n")
        clmMinvalue = str(df.columns[6])  # 下限值
        vClmMinvalue = clmMinvalue.split("(")[0].strip("\n")

        print("columns...{}...{}...{}...{}...{}".format(
            vClmCnCode, vClmEnCode, vClmIsParam, vClmCate, vClmUnit, vClmMaxvalue, vClmMinvalue
        ))

        # 遍历行.
        for i in df.index:
            vCnCode = str(df.loc[i][clmCnCode]).strip()
            vEnCode = str(df.loc[i][clmEnCode]).strip()
            vIsParam = str(df.loc[i][clmIsParam]).strip()
            vCate = str(df.loc[i][clmCate]).strip()
            vUnit = str(df.loc[i][clmUnit]).strip()
            vMaxvalue = str(df.loc[i][clmMaxvalue]).strip()
            vMinvalue = str(df.loc[i][clmMinvalue]).strip()

            if vUnit == "nan":
                vUnit = ""

            if not vIsParam or not vCate:
                continue
            # print("{}...{}".format(type(vIsParam), vIsParam))

            if vIsParam =='nan' or int(float(vIsParam)) != 1:   # 非空，非参数，跳过
                continue

            vlist = vCate.strip().split("/")
            if len(vlist) <= 0:     # 空数据，跳过.
                continue

            for x in vlist:
                print("{}...{}...{}...{}".format(x, vCnCode, vEnCode, vUnit))
                vv = paramDict.get(str(x), [])
                if str(x) == "optCol":
                    vv.append({
                        vClmCnCode: vCnCode,
                        vClmEnCode: vEnCode,
                        vClmUnit: vUnit,
                        vClmMaxvalue: vMaxvalue,
                        vClmMinvalue: vMinvalue
                    })

                    # 插入原始列表.
                    paramOriDict[vEnCode] = {
                        vClmCnCode: vCnCode,
                        vClmCate: vCate,
                        vClmUnit: vUnit,
                        vClmMaxvalue: vMaxvalue,
                        vClmMinvalue: vMinvalue
                    }

                else:
                    vv.append({
                        vClmCnCode: vCnCode,
                        vClmEnCode: vEnCode,
                        vClmUnit: vUnit
                    })

                    # 插入原始列表.
                    paramOriDict[vEnCode] = {
                        vClmCnCode: vCnCode,
                        vClmCate: vCate,
                        vClmUnit: vUnit
                    }
                # 插入列表.
                paramDict[x] = vv

        if paramDict is None:
            return None

        # 打印调试.
        print("paramDict......", json.dumps(paramDict))
        print("paramOriDict......", json.dumps(paramOriDict))

        return (
            json.dumps(paramDict),
            json.dumps(paramOriDict)
        )


    # @classmethod
    # def create_dataSource_dir(cls, useType, dataSourceName, dataSourceDir, dataFileName, paramsFileName):
    #     """
    #         创建数据源目录.
    #     """
    #     try:
    #         # [创建]，[dataSource]数据源目录.
    #         dsPath = "%s/%s" % (conf.DATA_SOURCE_PATH, dataSourceName)
    #         if os.path.exists(dsPath) is False:
    #             os.mkdir(dsPath)
    #
    #         # [复制]，数据、参数文件.
    #         srcDataPath = "%s/%s" % (dataSourceDir, dataFileName)
    #         destDataPath = "%s/%s" % (dsPath, dataFileName)
    #         with open(srcDataPath, "rb") as sourceFP:
    #             with open(destDataPath, "wb") as destFP:
    #                 destFP.write(sourceFP.read())
    #
    #         if useType == 1:  # 模型训练，需要参数文件.
    #             srcParamsPath = "%s/%s" % (dataSourceDir, paramsFileName)
    #             destParamPath = "%s/%s" % (dsPath, paramsFileName)
    #             with open(srcParamsPath, "rb") as sourceFP:
    #                 with open(destParamPath, "wb") as destFP:
    #                     destFP.write(sourceFP.read())
    #
    #         return 1
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         return None
