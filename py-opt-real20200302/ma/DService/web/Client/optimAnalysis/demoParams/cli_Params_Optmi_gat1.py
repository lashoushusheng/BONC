from CConfig import conf


class Cli_Optmi_Params_Gat1():
    """
    """
    modelType = "优化分析"
    modelName = "高安屯"

    trainDsName = "电力行业-燃气电厂历史数据"
    trainDsDesc = "高安屯，训练数据"
    trainDsFile = "高安屯_GAD_train_1.csv"
    trainDsParamFile = "高安屯_训练_参数.csv"

    predDsName = "电力行业-燃气电厂在线数据"
    predDsDesc = "高安屯，预测分析数据"
    predDsFile = "GAD_predict1.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\predic_data"
    else:
        trainDsDir = r"/root/works/idata/ma16_data/origin_data/优化分析1/train_data"
        predDsDir = r"/root/works/idata/ma16_data/origin_data/优化分析1/predic_data"

    # inputParamJsonFile = "../a.json"
    inputParams = [
        {
            "enStep": "optCol",
            "cnStep": "优化目标",
            "data": [
                {
                    "enCode": "V_P",
                    "cnCode": "循环水系统总功率",
                    "op_attribute": "-1",
                    "op_w": "1"
                }
            ]
        },
        {
            "enStep": "observedCol",
            "cnStep": "工况变量",
            "data": [
                {
                    "enCode": "V_P_qj",
                    "cnCode": "汽机功率",
                    "bias": "50"
                },
                {
                    "enCode": "V_P_Iqq",
                    "cnCode": "凝汽器真空",
                    "bias": "1.6"
                },
                {
                    "enCode": "V_F",
                    "cnCode": "进凝汽器的蒸汽量",
                    "bias": "150"
                },
                {
                    "enCode": "V_T",
                    "cnCode": "#1压气机入口温度/环境温度",
                    "bias": "9"
                }
            ]
        },
        {
            "enStep": "decisionCol",
            "cnStep": "强相关操作变量",
            "data": [
                {
                    "enCode": "V_I7",
                    "cnCode": "#7机力塔风机电机电流"
                },
                {
                    "enCode": "V_I5",
                    "cnCode": "#5机力塔风机电机电流"
                },
                {
                    "enCode": "V_I4",
                    "cnCode": "#4机力塔风机电机电流"
                },
                {
                    "enCode": "V_I6",
                    "cnCode": "#6机力塔风机电机电流"
                },
                {
                    "enCode": "V_I8",
                    "cnCode": "#8机力塔风机电机电流"
                },
                {
                    "enCode": "V_I2",
                    "cnCode": "#2机力塔风机电机电流"
                },
                {
                    "enCode": "V_I1",
                    "cnCode": "#1机力塔风机电机电流"
                },
                {
                    "enCode": "V_I3",
                    "cnCode": "#3机力塔风机电机电流"
                },
                {
                    "enCode": "V_Ib1",
                    "cnCode": "#1循环水大泵电机电流"
                },
                {
                    "enCode": "V_Ib2",
                    "cnCode": "#2循环水大泵电机电流"
                },
                {
                    "enCode": "V_Ib3",
                    "cnCode": "#3循环水大泵电机电流"
                },
                {
                    "enCode": "V_Ib4",
                    "cnCode": "循环水小泵电机电流"
                }
            ]
        }
    ]