from CConfig import conf


class cli_Params_Grey_test(object):
    """
    """
    modelType = "生产预警分析"
    modelName = "生产预警分析-训练模型"
    modelNames = ["生产预警分析-训练模型"]

    trainDsName = "生产预警分析-训练数据"
    trainDsDesc = "生产预警分析, 训练"
    trainDsFile = "生产预警_训练数据.csv"
    trainDsParamFile = "生产预警_参数.csv"

    predDsName = "生产预警分析-在线数据"
    predDsDesc = "生产预警, 预测分析"
    predDsFile = "生产预警_在线数据.csv"

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
                    "enCode": "T11",
                    "cnCode": "T601汽提塔顶温度",
                    "maxvalue": 530.0,
                    "minvalue": 490.0
                }
            ]
        },
        {
            "enStep": "adjustParam",
            "cnStep": "可调参数",
            "data": [
                {
                    "cnCode": "数据更新频率",
                    "enCode": "freq",
                    "enUnit": 15
                },
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
