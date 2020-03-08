from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.greyPredict.demoParams.cli_Params_Grey_test import cli_Params_Grey_test
from CConfig import conf


class Cli_Grey_Train_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "greyPredict"
        # url = "http://%s:%s/analysis_api/v1/%s/%s" % (
        #     conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        # )

        # url = "http://%s:%s/analysis_api/v1/%s/%s" % (
        #     "demo.shenzhuo.vip", 23508, modelType, urlName
        # )

        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            "49.233.5.174", 7752, modelType, urlName
        )

        print("url...", url)
        print(body)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]
    params = cli_Params_Grey_test

    # # [API]，添加-数据源
    # Cli_Grey_Train_All.process(
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
    # Cli_Grey_Train_All.process(
    #     urlName="train_get_dataSource_list",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 选中-数据源
    # Cli_Grey_Train_All.process(
    #     urlName="train_choiced_dataSource",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #     }
    # )

    # # [API], 保存-模型
    # Cli_Grey_Train_All.process(
    #     urlName="train_save_model",
    #     body={
    #         "modelType": params.modelType,
    #         "dataSourceName": params.trainDsName,
    #         "modelName": params.modelName,
    #         "modelParams": params.inputParams
    #     }
    # )

    # # [API], 获取-模型名称列表
    # Cli_Grey_Train_All.process(
    #     urlName="train_get_modelNameList",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 获取-模型参数
    # Cli_Grey_Train_All.process(
    #     urlName="train_get_modelParams",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName
    #     }
    # )

    # [API], 查询-训练结果
    Cli_Grey_Train_All.process(
        urlName="train_query_result",
        body={
            "modelType": params.modelType,
            "modelName": params.modelName
        }
    )

