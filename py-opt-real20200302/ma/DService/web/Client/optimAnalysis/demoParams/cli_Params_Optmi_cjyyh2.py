from CConfig import conf

class Cli_Optmi_Params_Cjyyh2():
    """
    """
    modelType = "优化分析"
    modelName = "sjp常减压优化分析模型"

    trainDsName = "1#常减压优化历史数据"
    trainDsDesc = "#常减压优化分析，训练测试"
    trainDsFile = "#常减压优化分析历史数据.csv"
    trainDsParamFile = "#常减压优化分析历史数据_参数.csv"

    predDsName = "1#常减压优化在线数据"
    predDsDesc = "#常减压优化分析，预测分析测试"
    predDsFile = "optmodel_0814.csv"

    if conf.DATA_SERVICE_IP == "127.0.0.1":
        trainDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\train_data"
        predDsDir = conf.ORI_DSOURCE_PATH + r"\优化分析\predic_data"
    else:
        trainDsDir = r"/root/works/idata/ma16_data/origin_data/优化分析1/train_data"
        predDsDir = r"/root/works/idata/ma16_data/origin_data/优化分析1/predic_data"

    inputParams = [
        {
            "enStep":"optCol",
            "cnStep":"优化目标",
            "data":[
                {
                    "cnCode":"重整汽油收率",
                    "enCode":"CZ3_OP1",
                    "op_attribute":"1",
                    "op_w":0.5
                },
                {
                    "cnCode":"低硫液化气收率",
                    "enCode":"CZ3_OP2",
                    "op_attribute":"1",
                    "op_w":0.5
                }
            ]
        },
        {
            "enStep":"observedCol",
            "cnStep":"工况变量",
            "data":[
                {
                    "cnCode":"换热器E701石脑油流量调节",
                    "enCode":"CZ3-FC7002",
                    "bias":"5"
                },
                {
                    "cnCode":"重整油流量调节",
                    "enCode":"CZ3-FC7007",
                    "bias":"5"
                },
                {
                    "cnCode":"富氢去PSA流量",
                    "enCode":"CZ3-FI7006",
                    "bias":"50"
                },
                {
                    "cnCode":"F702炉燃料气流量",
                    "enCode":"CZ3-FI7017",
                    "bias":"50"
                }
            ]
        },
        {
            "enStep":"decisionCol",
            "cnStep":"强相关操作变量",
            "data":[
                {
                    "cnCode":"换热器E701石脑油流量调节",
                    "enCode":"CZ3-FC7002"
                },
                {
                    "cnCode":"重整油流量调节",
                    "enCode":"CZ3-FC7007"
                },
                {
                    "cnCode":"富氢去PSA流量",
                    "enCode":"CZ3-FI7006"
                },
                {
                    "cnCode":"F702炉燃料气流量",
                    "enCode":"CZ3-FI7017"
                },
                {
                    "cnCode":"TI7001重整反应温度",
                    "enCode":"CZ3-TI7001"
                },
                {
                    "cnCode":"TI7003重整反应温度",
                    "enCode":"CZ3-TI7003"
                },
                {
                    "cnCode":"TI7005重整反应温度",
                    "enCode":"CZ3-TI7005"
                }
            ]
        }
    ]