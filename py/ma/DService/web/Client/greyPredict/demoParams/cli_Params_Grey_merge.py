from CConfig import conf


class cli_Params_Grey_merge(object):
    """
    """
    modelType = "生产预警分析"
    # modelName = "merge-训练模型"
    # modelName = "merge-test2"
    modelName = "TI284_1塔顶温度-test"
    modelNames = ["merge-训练模型"]

    trainDsName = "merge-训练数据"
    trainDsDesc = "merge, 训练"
    trainDsFile = "merge_data_训练数据.csv"
    trainDsParamFile = "生产预警merge_data_参数.csv"

    predDsName = "merge-在线数据"
    predDsDesc = "merge, 预测分析"
    predDsFile = "merge_在线数据.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\质量软测量\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\质量软测量\predic_data"
    else:
        trainDsDir = r"/root/works/idata/ma16_data/origin_data/生产预警分析/train_data"
        predDsDir = r"/root/works/idata/ma16_data/origin_data/生产预警分析/predic_data"

    inputParams = [
        {
            "enStep": "optCol",
            "cnStep": "优化目标",
            "data": [
                {
                    "enCode": "TI1103A_values",
                    "cnCode": "TI1103A塔顶温度",
                    "maxvalue": 520.0,
                    "minvalue": 490.0,
                    "freq": 15
                }
            ]
        },
        {
            "enStep": "adjustParam",
            "cnStep": "可调参数",
            "data": [
                {
                    "cnCode": "历史数据个数",
                    "enCode": "History_DataLength",
                    "enUnit": 15
                },
                {
                    "cnCode": "预测数据个数",
                    "enCode": "Predict_DataLength",
                    "enUnit": 3
                }
            ]
        }
    ]


