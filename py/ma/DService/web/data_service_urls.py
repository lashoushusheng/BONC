from DService.web.Services.train import Train_Model_Save, Train_DataSource_Choiced, Train_DataSource_List_Get, Train_ModelNameList_Get, \
    Train_Model_Params_Get
from DService.web.Services.train import Train_DataSource_Add, Train_Result_Query, Train_Result_Export
from DService.web.Services.predict import Predict_Task_Commit, Predict_DataSource_Add, Predict_DataSource_List_Get, \
    Predict_ModelNameList_Get, Predict_Result_Query, Predict_multiple_Result_Query, Predict_multiple_Task_Commit, Predict_Current_Task_Stop

__all__ = ['urls_pattern']

urls_pattern = []

# [优化分析].
urls_pattern_optimAnalysis = [
    # [训练]. 添加-数据源.
    ('/analysis_api/v1/optimAnalysis/train_add_dataSource', Train_DataSource_Add.Train_Add_DataSource_Handler),
    # [训练] 获取-数据源列表.
    ('/analysis_api/v1/optimAnalysis/train_get_dataSource_list', Train_DataSource_List_Get.Train_Get_DataSource_List_Handler),
    # [训练] 选中-数据源.
    ('/analysis_api/v1/optimAnalysis/train_choiced_dataSource', Train_DataSource_Choiced.Train_Choiced_DataSource_Handler),
    # [训练] 保存模型.
    ('/analysis_api/v1/optimAnalysis/train_save_model', Train_Model_Save.Train_Save_Model_Handler),
    # [训练] 获取-模型参数.
    ('/analysis_api/v1/optimAnalysis/train_get_modelParams', Train_Model_Params_Get.Train_Get_Model_Params_Handler),
    # [训练] 获取-模型名称列表.
    ('/analysis_api/v1/optimAnalysis/train_get_modelNameList', Train_ModelNameList_Get.Train_Get_ModelNameList_Handler),
    # [训练] 查询-训练结果.
    ('/analysis_api/v1/optimAnalysis/train_query_result', Train_Result_Query.Train_Query_Result_Handler),

    ('/analysis_api/v1/optimAnalysis/train_export_result', Train_Result_Export.Train_Export_Result_Handler),

    # [预测]. 添加-数据源.
    ('/analysis_api/v1/optimAnalysis/predict_add_dataSource', Predict_DataSource_Add.Predict_Add_DataSource_Handler),
    # [预测]. 获取-数据源列表.
    ('/analysis_api/v1/optimAnalysis/predict_get_dataSource_list', Predict_DataSource_List_Get.Predict_Get_DataSource_List_Handler),
    # [预测]. 停止当前任务
    ('/analysis_api/v1/optimAnalysis/predict_current_task_stop', Predict_Current_Task_Stop.Predict_Current_Task_Stop_Handler),
    # [预测]. 分析任务提交.
    ('/analysis_api/v1/optimAnalysis/predict_task_commit', Predict_Task_Commit.Predict_Commit_Task_Handler),
    # [预测]. 查询-分析结果.
    ('/analysis_api/v1/optimAnalysis/predict_query_result', Predict_Result_Query.Predict_Query_Result_Handler),
]
urls_pattern += urls_pattern_optimAnalysis

# [产品质量软测量]
url_pattern_softMeasure = [
    # [训练]. 添加-数据源.
    ('/analysis_api/v1/softMeasure/train_add_dataSource', Train_DataSource_Add.Train_Add_DataSource_Handler),
    # [训练] 获取-数据源列表.
    ('/analysis_api/v1/softMeasure/train_get_dataSource_list', Train_DataSource_List_Get.Train_Get_DataSource_List_Handler),
    # [训练] 选中-数据源.
    ('/analysis_api/v1/softMeasure/train_choiced_dataSource', Train_DataSource_Choiced.Train_Choiced_DataSource_Handler),
    # [训练] 保存模型.
    ('/analysis_api/v1/softMeasure/train_save_model', Train_Model_Save.Train_Save_Model_Handler),
    # [训练] 获取-模型参数.
    ('/analysis_api/v1/softMeasure/train_get_modelParams', Train_Model_Params_Get.Train_Get_Model_Params_Handler),
    # [训练] 获取-模型名称列表.
    ('/analysis_api/v1/softMeasure/train_get_modelNameList', Train_ModelNameList_Get.Train_Get_ModelNameList_Handler),
    # [训练] 查询-训练结果.
    ('/analysis_api/v1/softMeasure/train_query_result', Train_Result_Query.Train_Query_Result_Handler),

    # [预测]. 添加-数据源.
    ('/analysis_api/v1/softMeasure/predict_add_dataSource', Predict_DataSource_Add.Predict_Add_DataSource_Handler),
    # [预测]. 获取-数据源列表.
    ('/analysis_api/v1/softMeasure/predict_get_dataSource_list', Predict_DataSource_List_Get.Predict_Get_DataSource_List_Handler),
    # [预测]. 分析任务提交.
    ('/analysis_api/v1/softMeasure/predict_task_commit', Predict_Task_Commit.Predict_Commit_Task_Handler),
    # [预测]. 多个分析任务提交.
    ('/analysis_api/v1/softMeasure/predict_multiple_task_commit', Predict_multiple_Task_Commit.Predict_Commit_multiple_Task_Handler),
    # [预测]. 获取-模型名称列表.
    ('/analysis_api/v1/softMeasure/Predict_Get_Model_NameList', Predict_ModelNameList_Get.Predict_Get_ModelName_List_Handler),
    # [预测]. 查询-分析结果.
    ('/analysis_api/v1/softMeasure/predict_query_result', Predict_Result_Query.Predict_Query_Result_Handler),
    # [预测] 查询-多个分析结果
    ('/analysis_api/v1/softMeasure/predict_multiple_query_result', Predict_multiple_Result_Query.Predict_Query_multiple_Result_Handler),
# Predict_Query_multiple_Result_Handler
]
urls_pattern += url_pattern_softMeasure

# [灰色预测生产预警]
url_pattern_greyPredict = [
    # [训练]. 添加-数据源.
    ('/analysis_api/v1/greyPredict/train_add_dataSource', Train_DataSource_Add.Train_Add_DataSource_Handler),
    # [训练] 获取-数据源列表.
    ('/analysis_api/v1/greyPredict/train_get_dataSource_list', Train_DataSource_List_Get.Train_Get_DataSource_List_Handler),
    # [训练] 选中-数据源.
    ('/analysis_api/v1/greyPredict/train_choiced_dataSource', Train_DataSource_Choiced.Train_Choiced_DataSource_Handler),
    # [训练] 保存模型.
    ('/analysis_api/v1/greyPredict/train_save_model', Train_Model_Save.Train_Save_Model_Handler),
    # [训练] 获取-模型参数.
    ('/analysis_api/v1/greyPredict/train_get_modelParams', Train_Model_Params_Get.Train_Get_Model_Params_Handler),
    # [训练] 获取-模型名称列表.
    ('/analysis_api/v1/greyPredict/train_get_modelNameList', Train_ModelNameList_Get.Train_Get_ModelNameList_Handler),
    # [训练] 查询-训练结果.
    ('/analysis_api/v1/greyPredict/train_query_result', Train_Result_Query.Train_Query_Result_Handler),

    # [预测]. 添加-数据源.
    ('/analysis_api/v1/greyPredict/predict_add_dataSource', Predict_DataSource_Add.Predict_Add_DataSource_Handler),
    # [预测]. 获取-数据源列表.
    ('/analysis_api/v1/greyPredict/predict_get_dataSource_list', Predict_DataSource_List_Get.Predict_Get_DataSource_List_Handler),
    # [预测]. 分析任务提交.
    ('/analysis_api/v1/greyPredict/predict_task_commit', Predict_Task_Commit.Predict_Commit_Task_Handler),
    # [预测]. 多个分析任务提交.
    ('/analysis_api/v1/greyPredict/predict_multiple_task_commit', Predict_multiple_Task_Commit.Predict_Commit_multiple_Task_Handler),
    # [预测]. 获取-模型名称列表.
    ('/analysis_api/v1/greyPredict/Predict_Get_Model_NameList', Predict_ModelNameList_Get.Predict_Get_ModelName_List_Handler),
    # [预测]. 查询-分析结果.
    ('/analysis_api/v1/greyPredict/predict_query_result', Predict_Result_Query.Predict_Query_Result_Handler),
    # [预测] 查询-多个分析结果
    ('/analysis_api/v1/greyPredict/predict_multiple_query_result', Predict_multiple_Result_Query.Predict_Query_multiple_Result_Handler),
# Predict_Query_multiple_Result_Handler
]
urls_pattern += url_pattern_greyPredict


