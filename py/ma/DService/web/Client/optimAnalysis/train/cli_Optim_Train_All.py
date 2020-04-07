import json

from CConfig import conf
from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_dfd_2 import Cli_Optmi_Params_Dfd_2
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_dfd_1 import Cli_Optmi_Params_Dfd_1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_gat1 import Cli_Optmi_Params_Gat1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_mt1 import Cli_Optmi_Params_MT1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_cjyyh2 import Cli_Optmi_Params_Cjyyh2


class Cli_Optmi_Train_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "optimAnalysis"
        # url = "http://%s:%s/analysis_api/v1/%s/%s" % (
        #     conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        # )

        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            "s3.nsloop.com", 22795, modelType, urlName
        )
        print("url...", url)

        # 发送请求.
        Client_Public.mock_request(url, body)

    @classmethod
    def jsonFile2Str(cls, fileName):
        """
        """
        with open(fileName, encoding='utf-8') as f:
            lines = f.readlines()
            lineStr = '\n'.join(lines)
            # print(type(lineStr), lineStr)
            jsonDict = json.loads(lineStr)
            # print(jsonDict)
        return jsonDict


if __name__ == "__main__":
    # [参数]，常减压
    # params = Cli_Optmi_Params_Cjyyh1
    # params = Cli_Optmi_Params_Cjyyh2
    # [参数]，多氟多
    params = Cli_Optmi_Params_Dfd_2
    # [参数]，高安屯
    # params = Cli_Optmi_Params_Gat1
    # [参数]，美腾
    # params = Cli_Optmi_Params_MT1

    # # [API], 添加-数据源
    # Cli_Optmi_Train_All.process(
    #     urlName="train_add_dataSource",
    #     body={
    #         "dataSourceName": params.trainDsName,
    #         "dataSourceDesc": params.trainDsDesc,
    #         "dataSourceDir": params.trainDsDir,
    #         "dataFileName": params.trainDsFile,
    #         "paramsFileName": params.trainDsParamFile,
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 获取-数据源列表
    # Cli_Optmi_Train_All.process(
    #     urlName="train_get_dataSource_list",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )
    #
    # # [API], 选中-数据源
    # Cli_Optmi_Train_All.process(
    #     urlName="train_choiced_dataSource",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #     }
    # )

    # # [API], 保存-模型
    # Cli_Optmi_Train_All.process(
    #     urlName="train_save_model",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #         "modelName": params.modelName,
    #         "modelParams": params.inputParams
    #     }
    # )

    # # [API], 获取-模型名称列表
    # Cli_Optmi_Train_All.process(
    #     urlName="train_get_modelNameList",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 获取-模型参数
    # Cli_Optmi_Train_All.process(
    #     urlName="train_get_modelParams",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName
    #     }
    # )

    # [API], 查询-训练结果
    Cli_Optmi_Train_All.process(
        urlName="train_query_result",
        body={
            "modelType": params.modelType,
            "modelName": params.modelName
        }
    )




