from CConfig import conf
from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.holtWinters.demoParams.cli_Params_holtWinters_test import cli_Params_holtWinters_test


class Cli_holtWinters_Predict_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "holtWinters"
        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        )
        print("url...", url)
        print(body)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]，SH
    params = cli_Params_holtWinters_test

    # # [API], 添加-数据源
    # Cli_holtWinters_Predict_All.process(
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
    # Cli_holtWinters_Predict_All.process(
    #     urlName="predict_get_dataSource_list",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # # [API], 停止当前任务
    # Cli_holtWinters_Predict_All.process(
    #     urlName="predict_current_task_stop",
    #     body={
    #         "modelType": params.modelType
    #     }
    # )

    # [API], 多个分析任务提交
    Cli_holtWinters_Predict_All.process(
        urlName="predict_multiple_task_commit",
        body={
            "modelType": params.modelType,
            "modelNames": params.modelNames,
            "predictDataSourceName": params.predDsName,
        }
    )



