import pandas as pd
import random

class Loader:
    def __init__(self, pathToData:str, attributes: list, class_col:str, val_ratio:int=0.1):
        self.filePathToData = pathToData
        self.val_ratio = val_ratio
        self.attributes = attributes
        self.class_col = class_col
        self.classes=None
        self.num_attributes = len(attributes)
        self.data_total=None
        self.vals = []
        self.datas = []

        self.load_data()
        self.split_dataset()
    
    def load_data(self):
        df = pd.read_excel(self.filePathToData, sheet_name=0, index_col=None, header=0, usecols=self.attributes+[self.class_col])
        self.data_total = df.values.tolist()
        self.classes = list(set(df.iloc[:, -1]))

    def split_dataset(self):
        # random.shuffle(self.data_total)
        val_ = int(self.val_ratio*10)
        data_ = 10 - val_
        part_ = len(self.data_total)//(val_+data_)
        data_pad = self.data_total+self.data_total
        for part in range(val_+data_ -1):
            self.vals.append(data_pad[part*part_:(part+val_)*part_])
            self.datas.append(data_pad[(part+val_)*part_:(part+val_+data_)*part_])