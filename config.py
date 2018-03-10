from pandas import Timestamp


Time_Today = Timestamp.now()    # 用于设定周统计中前一周的末尾，默认使用运行程序的日期
# 如果需要指定日期，使用下面代码
# Time_Today = Timestamp("2018-02-05 00:00:00")

Time_Month = 2018.02            # 用于设定月统计中的最后一月，向前递减

# 用于设定需要分析哪些系统
Product_Types = [
    # "P15A",
    # "P15G",
    # "P68 A&B",
    "P81A",
    # "N.A.",
    "P81B",
    "P81B APK",
    # "Eurokit",
    # "P68 Eurokit",
    # "P15T Eurokit",
    # "P15T",
    # "P15S",
    # "Falcon",
    # "T16", 
    # "Intevo6",
    # "T2",
    # "Intevo16",
    # "P68G",
    "P81A APK",
    # "Intevo2",
    # "T6",
    # "P15F",
    # "Brazil A",
    # "Brazil P68A&B",
    # "Brazil S",
]

# ["IQC", "ASS", "DMS", "SI", "TCO", "DOA", "FOR", "R&D", "WH", "FRU"]
# 用于分析流程统计，注意顺序，列表中的最上面对应图中的柱子最下面
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

# 用于月统计
Monthly_Process_To_Analyze = [
    # "IQC",
    # "WH",
    # "R&D",
    # "TCO",
    # "DMS",
    "ASS",
    "SI",
    "DOA"
]

Figure_Size = (16, 9)

