from CConfig import conf
from DService.web.Client.cli_Public import Client_Public
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_dfd_1 import Cli_Optmi_Params_Dfd_1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_cjyyh2 import Cli_Optmi_Params_Cjyyh2
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_gat1 import Cli_Optmi_Params_Gat1
from DService.web.Client.optimAnalysis.demoParams.cli_Params_Optmi_mt1 import Cli_Optmi_Params_MT1


class Cli_Optmi_Predict_All():
    @classmethod
    def process(cls, urlName, body):
        """
        """
        modelType = "optimAnalysis"
        url = "http://%s:%s/analysis_api/v1/%s/%s" % (
            conf.DATA_SERVICE_IP, conf.DATA_SERVICE_PORT, modelType, urlName
        )
        print("url...", url)

        # 发送请求.
        Client_Public.mock_request(url, body)


if __name__ == "__main__":
    # [参数]，常减压
    # params = Cli_Optmi_Params_Cjyyh2
    # [参数]，多氟多
    params = Cli_Optmi_Params_Dfd_1
    # 高安屯
    # params = Cli_Optmi_Params_Gat1
    # 美腾
    # params = Cli_Optmi_Params_MT1

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

    # # [API], 分析任务提交
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_task_commit",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName,
    #         "predictDataSourceName": params.predDsName,
    #     }
    # )

    # [API], 查询-分析结果
    # Cli_Optmi_Predict_All.process(
    #     urlName="predict_query_result",
    #     body={
    #         "modelType": params.modelType,
    #         "modelName": params.modelName,
    #         "predictDataSourceName": params.predDsName
    #     }
    # )
