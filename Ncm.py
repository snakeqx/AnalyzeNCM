import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import config as cfg
from Header import NcmHeader as HD


class Ncm:
    def __init__(self, filename=r'./data/test.xlsx'):
        self.Is_Init_Done = False
        self.Is_Analyze_Done = False
        self.File_Name = filename
        self.Process_Name = ["IQC", "ASS", "DMS", "SI", "TCO", "DOA", "FOR", "R&D", "WH", "FRU"]
        self.Week_Name = ["Before", "LastWeek", "Future"]
        # 判断config文件中的process名称是否有误
        for _p in cfg.Target_Processes:
            if _p not in self.Process_Name:
                print("Process Name in config.py contains unexpected name(s). All availble names are:\n")
                print(self.Process_Name)
                return
        try:
            self.Data_Frame = pd.read_excel(self.File_Name,
                                            sheet_name="Sheet1",  # 强制设置为名称为Sheet1的表
                                            header=2,  # 默认excel会有两行空行
                                            index_col=None,  # 没有列名
                                            names=None,  # 没有名字
                                            skip_blank_lines=True  # 无视空行
                                            )
        except Exception as e:
            print(str(e))
            return
        # 筛选NCM标记符，只统计NCM判定为Yes的条目
        self.Data_Frame = self.Data_Frame[self.Data_Frame[HD.Is_Ncm] == "Yes"]
        # 筛选系统类型，类型选择在配置文件config.py定义
        self.Data_Frame = self.Data_Frame[self.Data_Frame[HD.System_Type].isin(cfg.Product_Types)]

        # 将每行数据按照流程名分类
        process = []
        for _i in self.Data_Frame[HD.Ncm_No]:
            if _i[0] == 'R':
                process.append(self.Process_Name[-1])  # FRU
            elif _i[4] == '0':
                process.append(self.Process_Name[0])  # IQC
            elif _i[4] == '1':
                process.append(self.Process_Name[1])  # ASS
            elif _i[4] == '2':
                process.append(self.Process_Name[2])  # DMS
            elif _i[4] == '3':
                process.append(self.Process_Name[3])  # SI
            elif _i[4] == '4':
                process.append(self.Process_Name[4])  # TCO
            elif _i[4] == '5':
                process.append(self.Process_Name[5])  # DOA
            elif _i[4] == '6':
                process.append(self.Process_Name[6])  # FOR
            elif _i[4] == '7':
                process.append(self.Process_Name[7])  # R&D
            elif _i[4] == '8':
                process.append(self.Process_Name[8])  # WH
            else:
                process.append('OTHER')
        self.Data_Frame[HD.Process_Name] = process  # 增加新列

        # 将NCM发现时间的年月摘出来，便于按月分析格式为数字"年.月"。结果是一个小数，便于排序
        month = [x.year + x.month * 0.01 for x in self.Data_Frame[HD.Find_Date]]
        self.Data_Frame[HD.Find_Month] = month  # 增加新列

        # 将NCM发现时间按config文件中指定的时间分类，分为上周，上周之前和未来。便于分析周NCM分布
        now = cfg.Time_Today
        week = []
        for w in self.Data_Frame[HD.Find_Date]:
            if (w - now).days > 0:
                week.append(self.Week_Name[2])  # Future
                print("data has \"Future\" time! Please double check! The analyze result will ignore the future data.")
            elif 0 >= (w - now).days >= -7:
                week.append(self.Week_Name[1])  # Last Week
            else:
                week.append(self.Week_Name[0])  # Before
        self.Data_Frame[HD.Week] = week  # 增加新列

        self.Is_Init_Done = True  # 结束初始化，设置标记
        self.Analyze_Process_Result = self.analyze_by_process()
        self.Analyze_Week_Result = self.analyze_by_week()
        self.Is_Analyze_Done = True  # 结束分析，设置标记

    def analyze_by_process(self):
        table = pd.pivot_table(self.Data_Frame,
                               index=[HD.Find_Month],
                               values=[HD.Quantity],
                               columns=self.Data_Frame[HD.Process_Name],
                               aggfunc=np.sum,
                               fill_value=0
                               )
        table = table[HD.Quantity]  # 只摘取Qty的子表格，否则表格结构复杂，不易后续处理
        for p in table:             # 删除不是目标流程的项目
            if p not in cfg.Target_Processes:
                del table[p]
        table = table.reindex(columns=cfg.Target_Processes) # 列重新排序，按照config中的Target_Process顺序
        return table

    def analyze_by_week(self):
        total = "Total"
        table = pd.pivot_table(self.Data_Frame,
                               index=[HD.Material_Name],
                               values=[HD.Quantity],
                               columns=self.Data_Frame[HD.Week],
                               aggfunc=np.sum,
                               fill_value=0
                               )
        table = table[HD.Quantity]  # 只摘取Qty的子表格，否则表格结构复杂，不易后续处理
        del table[self.Week_Name[2]]  # future的数据会被删除
        table[total] = table.apply(lambda x: x.sum(), axis=1)
        table.sort_values(by=total, ascending=False, inplace=True)
        table = table[(table[total] >= 3) | (table[self.Week_Name[1]] != 0)]
        del table[total]  # 排序完后删除
        return table

    def save_analyze_results(self):
        if not self.Is_Analyze_Done:
            print("Data analyze is not finished. Something is wrong")
            return
        try:
            out = pd.ExcelWriter(r'./Z3-AnalyzeResult.xlsx')
            self.Analyze_Week_Result.to_excel(out, sheet_name="Weekly")
            self.Analyze_Process_Result.to_excel(out, sheet_name="Process")
            self.Data_Frame.to_excel(out, sheet_name="Overview")
            out.save()
        except Exception as e:
            print(str(e))

    def save_analyze_plot(self):
        if not self.Is_Analyze_Done:
            print("Data analyze is not finished. Something is wrong")
            return
        try:
            ax = self.Analyze_Process_Result.plot(kind='bar', stacked=True, figsize=(15, 9))
            fig = ax.get_figure()
            fig.savefig('Z0-process.png')
            fig.clear()

            bx = self.Analyze_Week_Result.plot(kind='bar', stacked=True, figsize=(15, 9))
            fig2 = bx.get_figure()
            fig2.savefig('Z1-Weekly.png')
            fig2.clear()
        except Exception as e:
            print(str(e))
            return

