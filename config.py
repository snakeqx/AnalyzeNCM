from pandas import Timestamp

Time_Today = Timestamp.now()
Time_Today = Timestamp("2018-02-05 00:00:00")
Time_Month = 2018.02

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

