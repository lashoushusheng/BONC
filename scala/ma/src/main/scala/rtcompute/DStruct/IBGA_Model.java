package rtcompute.DStruct;

//原nblab接口
public interface IBGA_Model<T>{
    public Integer train_task_commit(String inputDataFilePath, String params, String modelSavePath);
    //参数：输入数据路径及参数、模型保存文件夹路径，返回值：错误码
    public T[] predict(String predictDataFilePath, String modelSavePath, String resultSavePath);
    //预测分析:参数：待分析数据路径，模型保存路径,分析保存路径；返回值：错误码
}

