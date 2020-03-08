from CConfig import conf


class Cli_Optmi_Params_Dfd_2():
    """
    """
    modelType = "优化分析"
    modelName = "多氟多2点_all"

    trainDsName = "多氟多2点_训练数据"
    trainDsDesc = "多氟多2点_训练数据，训练测试"
    trainDsFile = "多氟多2点_训练数据.csv"
    trainDsParamFile = "多氟多2点_训练数据_参数.csv"

    predDsName = "多氟多2点_在线数据"
    predDsDesc = "多氟多2点_训练数据，预测分析测试"
    predDsFile = "多氟多2点_在线数据.csv"

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
                    "enCode": "CZ3_OP1",
                    "cnCode": "AHF实际单耗",
                    "op_attribute": "0",
                    "op_w": "0.2"
                },
                {
                    "enCode": "CZ3_OP2",
                    "cnCode": "氢铝实际单耗",
                    "op_attribute": "0",
                    "op_w": "0.4"
                },
                {
                    "enCode": "CZ3_OP3",
                    "cnCode": "天然气实际单耗",
                    "op_attribute": "0",
                    "op_w": "0.4"
                }

            ]
        },
        {
            "enStep": "observedCol",
            "cnStep": "工况变量",
            "data": [
                {
                    "enCode": "BFIC_3021_F03_MV",
                    "cnCode": "2#炉2#罗茨风机出口风量调阀",
                    "bias": "5"
                },
                {
                    "enCode": "BFIC0304_F03",
                    "cnCode": "一次风机流量",
                    "bias": "300"
                },
                {
                    "enCode": "BMII_C301_F03",
                    "cnCode": "1#空气风机电流",
                    "bias": "5"
                },
                {
                    "enCode": "BFIC0305_F03",
                    "cnCode": "二次风机流量",
                    "bias": "630"
                },
                {
                    "enCode": "BMIC_C301_F03_MV",
                    "cnCode": "1#空气风机转速控制",
                    "bias": "5"
                },
                {
                    "enCode": "BFIC_3020_F03_MV",
                    "cnCode": "2#炉1#罗茨风机出口风量调阀",
                    "bias": "10"
                },
                {
                    "enCode": "BFIC_3005_F03_MV",
                    "cnCode": "1#罗茨风机出风量调",
                    "bias": "5"
                },
                {
                    "enCode": "BMIC_L303_F03_MV",
                    "cnCode": "氟化铝下料回转阀速控",
                    "bias": "10"
                },
                {
                    "enCode": "BMII_C302_F03",
                    "cnCode": "2#空气风机电流指示",
                    "bias": "15"
                },
                {
                    "enCode": "BPIA0308_F03",
                    "cnCode": "2#空气风机出口压力",
                    "bias": "5"
                },
                {
                    "enCode": "BFIC_3006_F03_MV",
                    "cnCode": "2#罗茨风机出风量调",
                    "bias": "5"
                },
                {
                    "enCode": "BMIC_C302_F03_MV",
                    "cnCode": "2#空气风机转速控制",
                    "bias": "5"
                },
                {
                    "enCode": "BMIIL303_F03",
                    "cnCode": "下料回转阀电流",
                    "bias": "1"
                },
                {
                    "enCode": "BPIA0307_F03",
                    "cnCode": "1#空气风机出口压力",
                    "bias": "5"
                },
                {
                    "enCode": "BPIRA0311_F03",
                    "cnCode": "硫化床底部压力",
                    "bias": "5"
                },
                {
                    "enCode": "BPIRA0312_F03",
                    "cnCode": "硫化床中部压力",
                    "bias": "40"
                },
                {
                    "enCode": "BTIR0307_F03",
                    "cnCode": "硫化床下部温度",
                    "bias": "50"
                },
                {
                    "enCode": "BTIR0308_F03",
                    "cnCode": "硫化床上部温度",
                    "bias": "5"
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
                    "enCode": "BFIC0302_F03",
                    "cnCode": "AHF换热器进口AHF流量"
                },
                {
                    "enCode": "BFIC_3003_F03_MV",
                    "cnCode": "AHF换热器出口HF压调"
                },
                {
                    "enCode": "BPIA0303_F03",
                    "cnCode": "AHF换热器进口蒸汽压"
                },
                {
                    "enCode": "BTIR0302_F03",
                    "cnCode": "AHF换热器出口HF温度"
                },
                {
                    "enCode": "PIA0302_F03",
                    "cnCode": "蒸汽减压阀后压力"
                },
                {
                    "enCode": "BTIR0304_F03",
                    "cnCode": "AHF换热器底部酸温度"
                },
                {
                    "enCode": "BPIA0304_F03",
                    "cnCode": "AHF换热器出口HF压力"
                },
                {
                    "enCode": "BPIR0305_F03",
                    "cnCode": "混合三通进口HF压力"
                },
                {
                    "enCode": "BTI0301_F03",
                    "cnCode": "进AHF换热器蒸汽温度"
                },
                {
                    "enCode": "BTIR0303_F03",
                    "cnCode": "混合三通进口HF温度"
                },
                {
                    "enCode": "BTIR0305_F03",
                    "cnCode": "膨胀弯头热气体温度"
                },
                {
                    "enCode": "BTIR0306_F03",
                    "cnCode": "混合三通混合气体温度"
                },
                {
                    "enCode": "FEED_SK04_F03",
                    "cnCode": "流量实际值"
                },
                {
                    "enCode": "SETPOINT04_F03",
                    "cnCode": "流量设定"
                },
                {
                    "enCode": "BFIC_3002_F03_MV",
                    "cnCode": "进AHF换热器AHF调节"
                }
            ]
        }
    ]
