import pandas as pd
import os
import time
import json
from DService.web.Services import mylog
import numpy as np

# df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
# print(df)
#
# for index, row in df.iterrows():
#     print(index)
#     print(row)
#     print(type(row))

paramOriJson = {"BFIC_3021_F03_MV": {"cnCode": "2#炉2#罗茨风机出口风量调阀", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC0304_F03": {"cnCode": "一次风机流量", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BMII_C301_F03": {"cnCode": "1#空气风机电流", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BFIC0305_F03": {"cnCode": "二次风机流量", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BMIC_C301_F03_MV": {"cnCode": "1#空气风机转速控制", "belongCate": "observedCol/decisionCol", "enUnit": "rpm"}, "BFIC_3020_F03_MV": {"cnCode": "2#炉1#罗茨风机出口风量调阀", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3005_F03_MV": {"cnCode": "1#罗茨风机出风量调", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3001_F03_MV": {"cnCode": "进AHF换热器蒸汽调节", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "BFIC0302_F03": {"cnCode": "AHF换热器进口AHF流量", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "BFIC_3003_F03_MV": {"cnCode": "AHF换热器出口HF压调", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BFIC_3007_F03_MV": {"cnCode": "进下料旋转阀冷却水调", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BFIQ0306_F03": {"cnCode": "进下料旋转阀冷却水F", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BMIC_L303_F03_MV": {"cnCode": "氟化铝下料回转阀速控", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BPIA0303_F03": {"cnCode": "AHF换热器进口蒸汽压", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BMII_C302_F03": {"cnCode": "2#空气风机电流指示", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BTIR0302_F03": {"cnCode": "AHF换热器出口HF温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "PIA0302_F03": {"cnCode": "蒸汽减压阀后压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIA0308_F03": {"cnCode": "2#空气风机出口压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BFIC_3006_F03_MV": {"cnCode": "2#罗茨风机出风量调", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BTIR0304_F03": {"cnCode": "AHF换热器底部酸温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BMIC_C302_F03_MV": {"cnCode": "2#空气风机转速控制", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BMIIL303_F03": {"cnCode": "下料回转阀电流", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BPIA0304_F03": {"cnCode": "AHF换热器出口HF压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIA0307_F03": {"cnCode": "1#空气风机出口压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIR0305_F03": {"cnCode": "混合三通进口HF压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIR0321_F03": {"cnCode": "2级除尘器进口压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0311_F03": {"cnCode": "硫化床底部压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0312_F03": {"cnCode": "硫化床中部压力", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0314_F03": {"cnCode": "一级气流反应器进口压", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BTI0301_F03": {"cnCode": "进AHF换热器蒸汽温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTI0319_F03": {"cnCode": "下料回转阀冷却回水温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTI0320_F03": {"cnCode": "氟化铝进冷却炉温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTI0321_F03": {"cnCode": "氟化铝出冷却炉温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0303_F03": {"cnCode": "混合三通进口HF温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0305_F03": {"cnCode": "膨胀弯头热气体温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0306_F03": {"cnCode": "混合三通混合气体温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0307_F03": {"cnCode": "硫化床下部温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0308_F03": {"cnCode": "硫化床上部温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0309_F03": {"cnCode": "一级气流反应器出口温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0310_F03": {"cnCode": "二级气流反应器下口温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0311_F03": {"cnCode": "三级气流反应器出口温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0316_F03": {"cnCode": "2级除尘器下口温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0313_F03": {"cnCode": "四级气流反应器出口气", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BTIR0314_F03": {"cnCode": "四级气流反应器下口温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0315_F03": {"cnCode": "2级除尘器出口气体温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "BTIR0312_F03": {"cnCode": "三级气流反应器下口温", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "FEED_SK04_F03": {"cnCode": "流量实际值", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "TI0318_F03": {"cnCode": "冷却水主管温度", "belongCate": "observedCol/decisionCol", "enUnit": "℃"}, "SETPOINT04_F03": {"cnCode": "流量设定", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3002_F03_MV": {"cnCode": "进AHF换热器AHF调节", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "CZ3_OP1": {"cnCode": "AHF实际单耗", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP2": {"cnCode": "氢铝实际单耗", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP3": {"cnCode": "天然气实际单耗", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}}
result1 = r"/root/works/idata/ma16_data/优化分析/多氟多2点/\result_1"
result2 = r"/root/works/idata/ma16_data/优化分析/多氟多2点/\result_2"


def real_compute_fetch_predict_result(result1_Dir, result2_Dir, paramOriJson, mylog):
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
        return [{"time": {}, "gw_id": {}, "optCol": [], "paramCol": []}]
    dfInput = pd.read_csv(src_Path, engine='python')
    # print(dfInput)
    # print("*" * 100)

    # for col in dfInput.columns:
    #     print(col)

    # 结果，转dataFrame.
    res_fname = None
    for file in os.listdir(result2_Dir):
        if os.path.splitext(file)[-1] == ".csv":
            res_fname = file
            break

    if res_fname is None:
        mylog.error("Could not find result-file in dir={} error.".format(result2_Dir))
    res_Path = "%s/%s" % (result2_Dir, res_fname)
    print("resultPath...{}".format(src_Path))
    size = os.path.getsize(res_Path)
    if size == 0:
        return [{"time": {}, "gw_id": {}, "optCol": [], "paramCol": []}]
    dfOutput = pd.read_csv(res_Path, engine='python')
    # print(dfOutput)
    # print("*" * 100)

    # for oClmnName in dfOutput.columns:
    #     print(oClmnName)

    oriParamDict = json.loads(paramOriJson)
    # print("paramOriJson...{}".format(oriParamDict))

    # merge，结果、输入文件.
    vResultList = []
    # 逐行处理.
    for index, oRow in dfOutput.iterrows():
        # 取结果文件[time]关键字.
        # print("2222222222222...oRow...", oRow)
        # print("time", oRow['time'])
        oTime = oRow['time']
        print(oTime)

        # 按time索引，过滤匹配input记录.
        iRow = dfInput[dfInput['time'] == oTime]
        print("iRow")
        print(iRow)

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
                # elif oClmnName == "CZ3_OP1" or oClmnName == "CZ3_OP2":
                elif oClmnName in ["CZ3_OP1", "CZ3_OP2"]:
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

    #         print("2222222222222...{}".format(json.dumps(vResultItemDict)))
    #
            # 插入, 结果集列表.
            if vResultItemDict['time']:
                vResultList.append(vResultItemDict)
        # break

    print("2222222222222...vResultList_len={}".format(len(vResultList)))
    return vResultList


if __name__ == '__main__':
    aa = real_compute_fetch_predict_result("1", "2", json.dumps(paramOriJson), mylog)
    # print(aa)
    res_dict = {"result": aa}
    print(json.dumps(res_dict))

    # print(paramOriJson.get("BPIR0305_F03", None))
    # print(paramOriJson.get("BPIA0304_F03", None))
