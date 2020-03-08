import json

import chardet
import pandas as pd

fpath = "/root/works/idata/ma16_data/origin_data/产品质量软测量/train_data/质量软测量_2#_参数.csv"

with open(fpath, "rb") as f:
    msg = f.read()
    print(msg.decode("utf-8"))
    result = chardet.detect(msg)
    charset = result['encoding']
    print("charset...", charset)

if charset == 'GB2312':
    df = pd.read_csv(fpath, engine='python')
else:
    df = pd.read_csv(fpath, engine='python', encoding='utf-8')

# 取列名.
print("columns.....", df.columns)

# 生成参数params字典.
paramDict = {}
paramOriDict = {}

# 取列名.
clmCnCode = str(df.columns[0])  # 中文名
vClmCnCode = clmCnCode.split("(")[0].strip("\n")
clmEnCode = str(df.columns[1])  # 英文名
vClmEnCode = clmEnCode.split("(")[0].strip("\n")
clmIsParam = str(df.columns[2])  # 是否是参数,1是/0不是
vClmIsParam = clmIsParam.split("(")[0].strip("\n")
clmCate = str(df.columns[3])  # 归属类别
vClmCate = clmCate.split("(")[0].strip("\n")
clmUnit = str(df.columns[4])  # 单位
vClmUnit = clmUnit.split("(")[0].strip("\n")
clmMaxvalue = str(df.columns[5])  # 归属类别
vClmMaxvalue = clmMaxvalue.split("(")[0].strip("\n")
clmMinvalue = str(df.columns[6])  # 单位
vClmMinvalue = clmMinvalue.split("(")[0].strip("\n")

print("columns...{}...{}...{}...{}...{}...{}...{}".format(
    vClmCnCode, vClmEnCode, vClmIsParam, vClmCate, vClmUnit, vClmMaxvalue, vClmMinvalue
))

# 遍历行.
for i in df.index:
    vCnCode = str(df.loc[i][clmCnCode]).strip()
    vEnCode = str(df.loc[i][clmEnCode]).strip()
    vIsParam = str(df.loc[i][clmIsParam]).strip()
    vCate = str(df.loc[i][clmCate]).strip()
    vUnit = str(df.loc[i][clmUnit]).strip()
    vMaxvalue = str(df.loc[i][clmMaxvalue]).strip()
    vMinvalue = str(df.loc[i][clmMinvalue]).strip()

    if vUnit == "nan":
        vUnit = ""

    if not vIsParam or not vCate:
        continue

    if vIsParam == 'nan' or int(float(vIsParam)) != 1:  # 非空，非参数，跳过
        continue

    vlist = vCate.strip().split("/")
    if len(vlist) <= 0:  # 空数据，跳过.
        continue

    for x in vlist:
        print("{}...{}...{}...{}".format(x, vCnCode, vEnCode, vUnit))
        vv = paramDict.get(str(x), [])
        if str(x) == "optCol":
            vv.append({
                vClmCnCode: vCnCode,
                vClmEnCode: vEnCode,
                vClmUnit: vUnit,
                vClmMaxvalue: vMaxvalue,
                vClmMinvalue: vMinvalue
            })

            paramOriDict[vEnCode] = {
                vClmCnCode: vCnCode,
                vClmCate: vCate,
                vClmUnit: vUnit,
                vClmMaxvalue: vMaxvalue,
                vClmMinvalue: vMinvalue

            }
        else:
            vv.append({
                vClmCnCode: vCnCode,
                vClmEnCode: vEnCode,
                vClmUnit: vUnit
            })

            paramOriDict[vEnCode] = {
                vClmCnCode: vCnCode,
                vClmCate: vCate,
                vClmUnit: vUnit
            }
        # 插入列表.
        paramDict[x] = vv

        # 插入原始列表.
        # paramOriDict[vEnCode] = {
        #     vClmCnCode: vCnCode,
        #     vClmCate: vCate,
        #     vClmUnit: vUnit
        # }

# if paramDict is None:
#     return None

# 打印调试.
print("paramDict......", json.dumps(paramDict))
print("paramOriDict......", json.dumps(paramOriDict))

