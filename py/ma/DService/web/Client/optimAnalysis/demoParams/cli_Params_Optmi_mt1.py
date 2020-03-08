from CConfig import conf


class Cli_Optmi_Params_MT1():
    """
    """
    modelType = "优化分析"
    modelName = "美腾"

    trainDsName = "煤炭行业-选煤厂历史数据"
    trainDsDesc = "美腾，训练数据"
    trainDsFile = "美腾洗煤_厂区二.csv"
    trainDsParamFile = "美腾洗煤_训练_参数.csv"

    predDsName = "煤炭行业-选煤厂在线数据"
    predDsDesc = "美腾，预测分析数据"
    predDsFile = "mt_predict.csv"

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
                    "enCode": "op_jx",
                    "cnCode": "经济效益",
                    "op_attribute": "1",
                    "op_w": "1"
                }
            ]
        },
        {
            "enStep": "observedCol",
            "cnStep": "工况变量",
            "data": [
                {
                    "enCode": "gk_1",
                    "cnCode": "分选系统（一）第3套 分选密度",
                    "bias": "0.03"
                },
                {
                    "enCode": "gk_2",
                    "cnCode": "分选系统（一）第4套 分选密度",
                    "bias": "0.03"
                },
                {
                    "enCode": "gk_3",
                    "cnCode": "皮带机第1套 瞬时带煤量",
                    "bias": "400"
                },
                {
                    "enCode": "gk_4",
                    "cnCode": "皮带机第10套 瞬时带煤量",
                    "bias": "900"
                },
                {
                    "enCode": "gk_5",
                    "cnCode": "皮带机第13套 瞬时带煤量",
                    "bias": "600"
                },
                {
                    "enCode": "gk_6",
                    "cnCode": "皮带机第14套 瞬时带煤量",
                    "bias": "600"
                },
                {
                    "enCode": "gk_7",
                    "cnCode": "皮带机第17套 瞬时带煤量",
                    "bias": "400"
                },
                {
                    "enCode": "gk_8",
                    "cnCode": "皮带机第20套 瞬时带煤量",
                    "bias": "1000"
                },
                {
                    "enCode": "gk_9",
                    "cnCode": "皮带机第22套 在线测灰",
                    "bias": "7"
                },
                {
                    "enCode": "gk_10",
                    "cnCode": "分选系统（四）第11套密度（分选）",
                    "bias": "0.3"
                },
                {
                    "enCode": "gk_11",
                    "cnCode": "分选系统（四）第12套密度（分选）",
                    "bias": "0.3"
                },
                {
                    "enCode": "gk_12",
                    "cnCode": "分选系统（四）第14套密度（分选）",
                    "bias": "0.3"
                },
                {
                    "enCode": "gk_13",
                    "cnCode": "分选系统（四）第15套密度（分选）",
                    "bias": "0.2"
                },
                {
                    "enCode": "gk_14",
                    "cnCode": "分选系统（四）第17套密度（分选）",
                    "bias": "0.2"
                },
                {
                    "enCode": "gk_15",
                    "cnCode": "分选系统（四）第18套密度（分选）",
                    "bias": "0.2"
                },
                {
                    "enCode": "gk_19",
                    "cnCode": "皮带机第2套 瞬时带煤量",
                    "bias": "900"
                },
                {
                    "enCode": "gk_20",
                    "cnCode": "皮带机第4套 瞬时带煤量",
                    "bias": "600"
                },
                {
                    "enCode": "gk_21",
                    "cnCode": "煤泥掺混（二期）",
                    "bias": "0.06"
                }
            ]
        },
        {
            "enStep": "decisionCol",
            "cnStep": "强相关操作变量",
            "data": [
                {
                    "enCode": "gk_1",
                    "cnCode": "分选系统（一）第3套 分选密度"
                },
                {
                    "enCode": "gk_2",
                    "cnCode": "分选系统（一）第4套 分选密度"
                },
                {
                    "enCode": "gk_10",
                    "cnCode": "分选系统（四）第11套密度（分选）"
                },
                {
                    "enCode": "gk_11",
                    "cnCode": "分选系统（四）第12套密度（分选）"
                },
                {
                    "enCode": "gk_12",
                    "cnCode": "分选系统（四）第14套密度（分选）"
                },
                {
                    "enCode": "gk_13",
                    "cnCode": "分选系统（四）第15套密度（分选）"
                },
                {
                    "enCode": "gk_14",
                    "cnCode": "分选系统（四）第17套密度（分选）"
                },
                {
                    "enCode": "gk_15",
                    "cnCode": "分选系统（四）第18套密度（分选）"
                },
                {
                    "enCode": "kt_1",
                    "cnCode": "分选系统（二）第4套 分选密度"
                },
                {
                    "enCode": "kt_2",
                    "cnCode": "分选系统（二）第5套 分选密度"
                },
                {
                    "enCode": "kt_3",
                    "cnCode": "分选系统（二）第6套 分选密度"
                },
                {
                    "enCode": "kt_4",
                    "cnCode": "分选系统（三）第4套 分选密度"
                },
                {
                    "enCode": "kt_5",
                    "cnCode": "分选系统（三）第5套 分选密度"
                },
                {
                    "enCode": "kt_6",
                    "cnCode": "分选系统（三）第6套 分选密度"
                }
            ]
        }
    ]