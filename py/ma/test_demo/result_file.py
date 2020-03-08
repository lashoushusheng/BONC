import os
import json
import pandas as pd


def result():
    fileDir = "/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B/predict_result/\predict_result"
    fname = None
    for file in os.listdir(fileDir):
        print(".........", file)
        if os.path.splitext(file)[-1] == ".csv":
            fname = file
            break
    if fname is None:
        print("Could not find fname={} error.".format(fname))

    resultPath = "%s/%s" % (fileDir, fname)

    print("resultPath...........{}".format(resultPath))

    df = pd.read_csv(resultPath, engine='python')

    dataJsonStr = df.to_json(
        force_ascii=False
    )
    dataJson = json.loads(
        dataJsonStr
    )

    print(dataJson)


if __name__ == '__main__':
    # result()
    # dfOutput = pd.read_csv("/root/works/src/git_test/rtc/poc_MAnalysis/py/ma/test_demo/part-00000-a608ed09-3a0e-4c1e-ae9d-6e950c254b0e-c000.csv", engine='python')
    # if dfOutput:
    #     print(dfOutput)
    # else:
    #     print("null")
    size = os.path.getsize('/root/works/src/git_test/rtc/poc_MAnalysis/py/ma/test_demo/part-00000-a608ed09-3a0e-4c1e-ae9d-6e950c254b0e-c000.csv')

    if size == 0:
        print('文件是空的')
    else:
        print('文件不是空的')

