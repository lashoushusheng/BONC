from CConfig import conf


class cli_Params_holtWinters_test(object):
    """
    """
    modelType = "三次平滑指数预警分析"
    modelName = "三次平滑指数预警-训练模型"
    # modelName = "test1"
    modelNames = ["三次平滑指数预警-训练模型", "test1"]

    trainDsName = "三次平滑指数预警分析-训练数据"
    trainDsDesc = "三次平滑指数预警分析, 训练"
    trainDsFile = "三次平滑指数预警分析_训练数据.csv"
    trainDsParamFile = "三次平滑指数预警分析_参数.csv"

    predDsName = "三次平滑指数预警分析-在线数据"
    predDsDesc = "三次平滑指数预警分析, 预测分析"
    predDsFile = "三次平滑指数预警分析_在线数据.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\三次平滑指数预警分析\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\三次平滑指数预警分析\predic_data"
    else:
        trainDsDir = r"/root/works/idata/ma16_data/origin_data/三次平滑指数预警分析/train_data"
        predDsDir = r"/root/works/idata/ma16_data/origin_data/三次平滑指数预警分析/predic_data"

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
                    "cnCode": "周期",
                    "enCode": "Period",
                    "enUnit": 5
                }
            ]
        }
    ]


