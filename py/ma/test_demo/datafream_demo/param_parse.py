import pandas as pd
import json

# fpath = "/root/works/idata/ma16_data/origin_data/产品质量软测量/train_data/质量软测量_2#_参数.csv"
fpath = "/root/works/idata/ma16_data/origin_data/生产预警分析/train_data/生产预警merge_data_参数.csv"

df = pd.read_csv(fpath)

# 生成参数params字典.
paramDict = {}
paramOriDict = {}

dfcolumnsDict = {}

for item in df.columns.values.tolist():
    item_encode = item.split("(")[0].strip("\n")
    dfcolumnsDict[item_encode] = item

for i in df.index:
    df_2_Dict = {}
    for k, v in dfcolumnsDict.items():
        df_2_Dict[k] = str(df.loc[i][v]).strip()

    if df_2_Dict.get("enUnit") == "nan":
        df_2_Dict["enUnit"] = ""

    # print(df_2_Dict)

    if not df_2_Dict.get("isParam") or not df_2_Dict.get("belongCate"):
        continue

    if df_2_Dict.get("isParam") =='nan' or int(float(df_2_Dict.get("isParam"))) != 1:   # 非空，非参数，跳过
        continue

    vlist = df_2_Dict.get("belongCate").strip().split("/")
    if len(vlist) <= 0:     # 空数据，跳过.
        continue

    for x in vlist:
        vv = paramDict.get(str(x), [])
        if str(x) == "optCol":
            vv.append({
                "cnCode": df_2_Dict.get("cnCode"),
                "enCode": df_2_Dict.get("enCode"),
                "enUnit": df_2_Dict.get("enUnit"),
                "maxvalue": df_2_Dict.get("maxvalue"),
                "minvalue": df_2_Dict.get("minvalue"),
                "freq": df_2_Dict.get("freq", 0)
            })

            # 插入原始列表.
            paramOriDict[df_2_Dict.get("enCode")] = {
                "cnCode": df_2_Dict.get("cnCode"),
                "enCode": df_2_Dict.get("enCode"),
                "enUnit": df_2_Dict.get("enUnit"),
                "maxvalue": df_2_Dict.get("maxvalue"),
                "minvalue": df_2_Dict.get("minvalue"),
                "freq": df_2_Dict.get("freq")
            }

        else:
            vv.append({
                "cnCode": df_2_Dict.get("cnCode"),
                "enCode": df_2_Dict.get("enCode"),
                "enUnit": df_2_Dict.get("enUnit")
            })

            # 插入原始列表.
            paramOriDict[df_2_Dict.get("enCode")] = {
                "cnCode": df_2_Dict.get("cnCode"),
                "enCode": df_2_Dict.get("enCode"),
                "enUnit": df_2_Dict.get("enUnit")
            }
        # 插入列表.
        paramDict[x] = vv

# if paramDict is None:
#     return None

# 打印调试.
print("paramDict......", json.dumps(paramDict))
# print("paramOriDict......", json.dumps(paramOriDict))

# return (
#     json.dumps(paramDict),
#     json.dumps(paramOriDict)
# )
