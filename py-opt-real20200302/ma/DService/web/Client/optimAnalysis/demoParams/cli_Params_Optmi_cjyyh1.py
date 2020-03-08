from CConfig import conf

class Client_Optmi_Params_Cjyyh1():
    """
    """
    modelType = "优化分析"
    modelName = "1#常减压优化分析模型"

    trainDsName = "1#常减压优化历史数据"
    trainDsDesc = "#常减压优化分析，训练测试"
    trainDsFile = "#常减压优化分析历史数据.csv"
    trainDsParamFile = "#常减压优化分析历史数据_参数.csv"

    predDsName = "1#常减压优化在线数据"
    predDsDesc = "#常减压优化分析，预测分析测试"
    # predDsFile = "待分析数据.csv"
    predDsFile = "optmodel_0814.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\predic_data"
    else:
        trainDsDir = r"/home/chijy/idata/ma16_data/origin_data/优化分析1/train_data"
        predDsDir = r"/home/chijy/idata/ma16_data/origin_data/优化分析1/predic_data"

    # inputParamJsonFile = "../a.json"
    inputParams = [
        {
            "enStep": "optCol",
            "cnStep": "优化目标",
            "data": [
                {
                    "enCode": "CZ3_OP1",
                    "cnCode": "重整汽油收率",
                    "op_attribute": "-1",
                    "op_w": "0.4"
                },
                {
                    "enCode": "CZ3_OP2",
                    "cnCode": "低硫液化气收率",
                    "op_attribute": "-1",
                    "op_w": "0.25"
                },
                {
                    "enCode": "CZ3_OP3",
                    "cnCode": "燃料气消耗总量",
                    "op_attribute": "1",
                    "op_w": "0.1"
                },
                {
                    "enCode": "CZ3_OP4",
                    "cnCode": "氢气收率",
                    "op_attribute": "-1",
                    "op_w": "0.25"
                }
            ]
        },
        {
            "enStep": "observedCol",
            "cnStep": "工况变量",
            "data": [
                {
                    "enCode": "CZ3-FC7002",
                    "cnCode": "换热器E701石脑油流量调节",
                    "bias": "5"
                },
                {
                    "enCode": "CZ3-TI7001",
                    "cnCode": "TI7001重整反应温度",
                    "bias": "5"
                },
                {
                    "enCode": "CZ3-TI7003",
                    "cnCode": "TI7003重整反应温度",
                    "bias": "5"
                },
                {
                    "enCode": "CZ3-TI7005",
                    "cnCode": "TI7005重整反应温度",
                    "bias": "5"
                },
                {
                    "enCode": "CZ3-TI7007",
                    "cnCode": "TI7007重整反应温度",
                    "bias": "5"
                }
            ]
        },
        {
            "enStep": "decisionCol",
            "cnStep": "强相关操作变量",
            "data": [
                {
                    "enCode": "CZ3-FC7002",
                    "cnCode": "换热器E701石脑油流量调节"
                },
                {
                    "enCode": "CZ3-TI7001",
                    "cnCode": "TI7001重整反应温度"
                },
                {
                    "enCode": "CZ3-TI7003",
                    "cnCode": "TI7003重整反应温度"
                },
                {
                    "enCode": "CZ3-TI7005",
                    "cnCode": "TI7005重整反应温度"
                },
                {
                    "enCode": "CZ3-TI7007",
                    "cnCode": "TI7007重整反应温度"
                },
                {
                    "enCode": "CZ3-TI7041",
                    "cnCode": "T701稳定塔塔顶温度"
                },
                {
                    "enCode": "CZ3-TI7043",
                    "cnCode": "T701稳定塔塔底出口温度"
                },
                {
                    "enCode": "CZ3-PI7008",
                    "cnCode": "T701稳定塔塔顶压力调节"
                },
                {
                    "enCode": "CZ3-PI7101",
                    "cnCode": "T701稳定塔塔底压力"
                },
                {
                    "enCode": "CZ3-FI7017",
                    "cnCode": "F702炉燃料气流量"
                },
                {
                    "enCode": "CZ3-FI7018",
                    "cnCode": "F701炉燃料气流量"
                },
                {
                    "enCode": "CZ3-FI7019",
                    "cnCode": "F703炉燃料气流量"
                },
                {
                    "enCode": "CZ3-FI7020",
                    "cnCode": "F704炉燃料气流量"
                }
            ]
        }
    ]
