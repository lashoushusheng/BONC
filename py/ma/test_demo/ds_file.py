#-*- encoding=utf8 -*-
import time
import os

file = "/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data/2号软测量预测数据.csv"
# def fileTime(file):
#     return
#     [
# 　　　　time.ctime(os.path.getatime(file)),
# 　　　　time.ctime(os.path.getctime(file)),
# 　　　　time.ctime(os.path.getmtime(file))
#     ]

# times = fileTime("d")

#times = fileTime("ccc")
# print(times)
dir = "/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B/predict_result/predict_result"
dir1 = "/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B"


def check_result(dir):

    while not os.path.isdir(dir):
        print("正在分析中!")

    Files = os.listdir(dir)
    while not Files or len(Files)<4:
        print("正在分析中!")

    for k in range(len(Files)):
        # 提取文件夹内所有文件的后缀
        Files[k] = os.path.splitext(Files[k])[1]


if __name__ == '__main__':
    # print(time.ctime(os.path.getatime(file)))
    # print(os.path.isdir(dir))
    # while not os.path.isdir(dir):
    #     print(os.path.isdir(dir))

    import os
    dir = '/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B/predict_result/\predict_result'
    Files = os.listdir(dir)
    if not Files or len(Files)<4:
        print("not exit")

    #
    # print(len(Files))
    # while not Files:
    #     for k in range(len(Files)):
    #         # 提取文件夹内所有文件的后缀
    #         # Files[k] = os.path.splitext(Files[k])[1]
    #         print(Files[k])


