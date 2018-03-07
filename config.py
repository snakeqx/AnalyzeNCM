from pandas import Timestamp

Time_Today = Timestamp("2018-2-5 0:00:00")

Product_Types = [
    "P81A",
    "P81B"
]

# ["IQC", "ASS", "DMS", "SI", "TCO", "DOA", "FOR", "R&D", "WH", "FRU"]
# 注意顺序，列表中的最上面对应图中的柱子最下面
Target_Processes = [
    "IQC",
    "WH",
    "R&D",
    "TCO",
    "DMS",
    "ASS",
    "SI",
    "DOA"
]
