
# dict = {'a': 1, 'b': 2}
# # print(dict)
# print(dict.pop("a"))

# dict["c"] = dict.pop("a")
#
# print(dict)
# modelType = "产品质量软测量"
# dataSourceName = "质量软测量_2#001"
#
# sql = """SELECT a.modelType modelType, a.modelName modelName"""
# sql += """ FROM ma_predict a WHERE a.modelType='%s' AND a.dsName='%s' ORDER BY a.updateTime DESC
#     """ % (modelType, dataSourceName)
#
# print(sql)

modelType = "产品质量软测量"
dataSourceName = "多氟多_2#_质量软测#在线数据"
# modelNames=["质量软测量_2#", "质量软测量_2#001", "质量软测量_2#003", "质量软测量_2#004"]
modelNames=["质量软测量_2#"]

modelNames_t = None
if len(modelNames) == 1:
 modelNames_t = f"('{modelNames[0]}')"
else:
 modelNames_t = tuple(modelNames)

print(modelNames_t)




# tup1 = tuple(modelNames)
# print(tup1)

# print(list(tup1))
# modelNames_tuple = tuple(modelNames)

# sql = """SELECT a.modelType modelType, a.modelName modelName, a.predictDir predictDir FROM ma_predict a
#  WHERE a.modelType='%s' AND a.dsName='%s' AND a.modelName IN %s ORDER BY a.updateTime DESC""" \
#  % (modelType, dataSourceName, modelNames_tuple)
#
# print(sql)
