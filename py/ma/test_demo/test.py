predictNameDict = {
    "优化分析": "maPredict_opt_stream",
    "产品质量软测量": "maPredict_soft_stream",
    "生产预警分析": "maPredict_grey_stream",
    "三次平滑指数预警分析": "maPredict_holtWinters_stream"
}

print(predictNameDict.get("三次平滑指数预警分"))
