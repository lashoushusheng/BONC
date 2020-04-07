from CConfig import conf


class Client_Soft_Params_Dfd1(object):
    """
    """
    modelType = "产品质量软测量"
    modelName = "1#质量软测量-A"
    modelNames = ["1#质量软测量-A", "1#质量然测量-B"]

    trainDsName = "多氟多_1#_质量软测#训练数据"
    trainDsDesc = "多氟多_1#_质量软测#, 训练"
    trainDsFile = "多氟多_1#_质量软测#训练数据.csv"
    trainDsParamFile = "质量软测量_1#_参数.csv"

    predDsName = "多氟多_1#_质量软测#在线数据"
    predDsDesc = "多氟多_1#_质量软测#, 预测分析"
    predDsFile = "1号软测量预测数据.csv"

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
                    "enCode": "A(%)",
                    "cnCode": "A(%)"
                },
                {
                    "enCode": "B(%)",
                    "cnCode": "B(%)"
                }
            ]
        },
        {
            "enStep": "decisionCol",
            "cnStep": "强相关操作变量",
            "data": [
                {
                    "enCode": "BFIC_3001_F03_MV",
                    "cnCode": "进AHF换热器蒸汽调节"
                },
                {
                    "enCode": "BFIC_3002_F03_MV",
                    "cnCode": "进AHF换热器AHF调节"
                },
                {
                    "enCode": "BFIC_3005_F03_MV",
                    "cnCode": "1#罗茨风机出风量调"
                },
                {
                    "enCode": "BFIC_3003_F03_MV",
                    "cnCode": "AHF换热器出口HF压调"
                },
                {
                    "enCode": "BFIC_3006_F03_MV",
                    "cnCode": "2#罗茨风机出风量调"
                },
                {
                    "enCode": "BFIC_3021_F03_MV",
                    "cnCode": "2#炉2#罗茨风机出口风量调阀"
                },
                {
                    "enCode": "BFIC0302_F03",
                    "cnCode": "AHF换热器进口AHF流量"
                },
                {
                    "enCode": "BFIC0305_F03",
                    "cnCode": "二次风机流量"
                },
                {
                    "enCode": "BMIC_C302_F03_MV",
                    "cnCode": "2#空气风机转速控制"
                },
                {
                    "enCode": "BPIA0303_F03",
                    "cnCode": "AHF换热器进口蒸汽压"
                },
                {
                    "enCode": "BPIA0304_F03",
                    "cnCode": "AHF换热器出口HF压力"
                },
                {
                    "enCode": "BTI0301_F03",
                    "cnCode": "进AHF换热器蒸汽温度"
                },
                {
                    "enCode": "PIA0302_F03",
                    "cnCode": "蒸汽减压阀后压力"
                },
            ]
        }
    ]
