from CConfig import conf
from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_dfd1 import Client_Soft_Params_Dfd1
from DService.web.Client.softMeasure.demoParams.cli_Params_Soft_MT1 import Client_Soft_Params_MT1

class Cli_Optmi_Predict_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "softMeasure"
        # url = "http://%s:%s/analysis_api/v1/%s/%s" % (
        #     conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        # )
        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            "s3.nsloop.com", 22795, modelType, urlName
        )

        print("url...", url)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]，多氟多
    params = Client_Soft_Params_Dfd1
    # [parameter]
    # params = Client_Soft_Params_MT1

    # # [API], 添加-数据源
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_add_dataSource",
    #     body={
    #         "dataSourceName": params.predDsName,
    #         "dataSourceDesc": params.predDsDesc,
    #         "dataSourceDir": params.predDsDir,
    #         "dataFileName": params.predDsFile,
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 获取-数据源列表
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_get_dataSource_list",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 停止当前任务
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_current_task_stop",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 分析任务提交
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_task_commit",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName,
    #         "predictDataSourceName": params.predDsName,
    #     }
    # )

    # [API], 多个分析任务提交
    Cli_Optmi_Predict_All.process(
        urlName="predict_multiple_task_commit",
        body={
            "modelType": params.modelType,
            "modelNames": params.modelNames,
            "predictDataSourceName": params.predDsName,
        }
    )

    # [API], 分析值与实测值对比
    Cli_Optmi_Predict_All.process(
        urlName="predict_Result_Compare",
        body={
            "modelType": params.modelType,
            "modelNames": params.modelNames
        }
    )

    # # [API], 查询-分析结果
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName,
    #         "predictDataSourceName": params.predDsName,
    #     }
    # )

    # # [API], 查询-多个分析结果
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_multiple_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelNames": params.modelNames,
    #         "predictDataSourceName": params.predDsName
    #     }
    # )

