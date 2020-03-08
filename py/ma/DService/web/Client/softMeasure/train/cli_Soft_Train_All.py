from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_dfd import Client_Soft_Params_Dfd1
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_MT1 import Client_Soft_Params_MT1
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_SH1 import Client_Soft_Params_SH1
from CConfig import conf


class Cli_Soft_Train_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "softMeasure"
        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        )
        print("url...", url)
        print(body)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]，多氟多
    params = Client_Soft_Params_Dfd1
    # [参数]，美腾
    # params = Client_Soft_Params_MT1
    # [参数]，石化
    # params = Client_Soft_Params_SH1

    # [API]，添加-数据源
    Cli_Soft_Train_All.process(
        urlName="train_add_dataSource",
        body={
            "dataSourceName": params.trainDsName,
            "dataSourceDesc": params.trainDsDesc,
            "dataSourceDir": params.trainDsDir,
            "dataFileName": params.trainDsFile,
            "paramsFileName": params.trainDsParamFile,
            "modelType": params.modelType
        }
    )

    # # [API], 获取-数据源列表
    # Cli_Soft_Train_All.process(
    #     urlName="train_get_dataSource_list",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )
    #
    # # [API], 选中-数据源
    # Cli_Soft_Train_All.process(
    #     urlName="train_choiced_dataSource",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #     }
    # )
    #
    # # [API], 保存-模型
    # Cli_Soft_Train_All.process(
    #     urlName="train_save_model",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #         "modelName": params.modelName,
    #         "modelParams": params.inputParams
    #     }
    # )
    #
    # # [API], 获取-模型名称列表
    # Cli_Soft_Train_All.process(
    #     urlName="train_get_modelNameList",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )
    #
    # # [API], 获取-模型参数
    # Cli_Soft_Train_All.process(
    #     urlName="train_get_modelParams",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName
    #     }
    # )
    #
    # # [API], 查询-训练结果
    # Cli_Soft_Train_All.process(
    #     urlName="train_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName
    #     }
    # )

