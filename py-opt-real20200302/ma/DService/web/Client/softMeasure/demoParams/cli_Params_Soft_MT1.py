from CConfig import conf


class Client_Soft_Params_MT1(object):
    """
    """
    modelType = "产品质量软测量"
    modelName = "美腾_soft333333"
    modelNames = ["美腾"]

    trainDsName = "美腾_2#_质量软测#训练数据"
    trainDsDesc = "美腾_2#_质量软测#, 训练"
    trainDsFile = "F1_P1_对齐5min.csv"
    trainDsParamFile = "美腾洗煤灰分软测量_训练参数.csv"

    predDsName = "美腾_2#_质量软测#在线数据"
    predDsDesc = "美腾_2#_质量软测#, 预测分析"
    predDsFile = "mt_predict_soft.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\质量软测量\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\质量软测量\predic_data"
    else:
        trainDsDir = r"/root/works/idata/ma16_data/origin_data/产品质量软测量/train_data"
        predDsDir = r"/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data"

    inputParams = [
        {
            "enStep": "optCol",
            "cnStep": "优化目标",
            "data": [
                {
                    "enCode": "F1_P1_Ash",
                    "cnCode": "精煤灰分",
                    "enUnit": "%",
                    "maxvalue": "11.0",
                    "minvalue": "9.0"
                },
                {
                    "enCode": "F1_P2_Ash",
                    "cnCode": "混煤灰分",
                    "enUnit": "%",
                    "maxvalue": "24.0",
                    "minvalue": "18.0"
                }
            ]
        },
        {
            "enStep": "decisionCol",
            "cnStep": "强相关操作变量",
            "data": [
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


