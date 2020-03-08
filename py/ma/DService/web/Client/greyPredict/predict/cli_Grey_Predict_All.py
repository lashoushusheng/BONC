from CConfig import conf
from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.greyPredict.demoParams.cli_Params_Grey_test import cli_Params_Grey_test


class Cli_Grey_Predict_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "greyPredict"
        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        )
        print("url...", url)
        print(body)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]，SH
    params = cli_Params_Grey_test

    # # [API], 添加-数据源
    # Cli_Grey_Predict_All.process(
    #     urlName="predict_add_dataSource",
    #     body={
    #         "dataSourceName": params.predDsName,
    #         "dataSourceDesc": params.predDsDesc,
    #         "dataSourceDir": params.predDsDir,
    #         "dataFileName": params.predDsFile,
    #         "modelType": params.modelType
    #     }
    # )

    # [API], 获取-数据源列表
    Cli_Grey_Predict_All.process(
        urlName="predict_get_dataSource_list",
        body={
            "modelType": params.modelType
        }
    )

    # [API], 分析任务提交
    Cli_Grey_Predict_All.process(
        urlName="predict_task_commit",
        body={
            "modelType": params.modelType,
            "modelName": params.modelName,
            "predictDataSourceName": params.predDsName,
        }
    )

    # # [API], 多个分析任务提交
    # Cli_Grey_Predict_All.process(
    #     urlName="predict_multiple_task_commit",
    #     body={
    #         "modelType": params.modelType,
    #         "modelNames": params.modelNames,
    #         "predictDataSourceName": params.predDsName,
    #     }
    # )

    # # [API], 查询-分析结果
    # Cli_Grey_Predict_All.process(
    #     urlName="predict_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName,
    #         "predictDataSourceName": params.predDsName,
    #     }
    # )

    # # [API], 查询-多个分析结果
    # Cli_Grey_Predict_All.process(
    #     urlName="predict_multiple_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelNames": params.modelNames,
    #         "predictDataSourceName": params.predDsName
    #     }
    # )

