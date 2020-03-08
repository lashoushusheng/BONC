#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import shutil
import traceback
import pandas as pd

from CConfig import conf


def save_train_result_2_csv(fileDir, modelName, mylog):
    """
    """
    fname = None
    for file in os.listdir(fileDir):
        print(".........", file)
        if os.path.splitext(file)[-1] == ".csv":
            fname = file
            break
    if fname is None:
        print("Could not find fname={} error.".format(fname))

    resultPath = "%s/%s" % (fileDir, fname)
    # mylog.info("resultPath...........{}".format(resultPath))
    # pandas.dataFrame.
    df = pd.read_csv(resultPath, engine='python').rename(columns={"gw_id": "工况"}).drop(['concat_col_gw', 'op'], axis=1)
    # print(df)
    df.to_csv(fileDir + f"/{modelName}_训练结果.csv", index=False)


if __name__ == '__main__':
    save_train_result_2_csv(r"/root/works/idata/ma16_data/优化分析/多氟多1点/train_result/\result_2", "多氟多1点", None)