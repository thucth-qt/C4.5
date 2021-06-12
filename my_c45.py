import pandas as pd

class MyC45:
    def __init__(self, data_path):
        #file excel
        xlsx = pd.ExcelFile(data_path,)
        sheet1 = xlsx.parse(0)

        col0 = sheet1.iloc[:,0][:10]
        row0 = sheet1.iloc[0,:][:10]


        # print(col0)
        # print(row0)
        # print(sheet1.heads())
        print(type(sheet1.iloc[0,:]).HK01)
