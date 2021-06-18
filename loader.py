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
        random.shuffle(self.data_total)
        num_of_val = int(len(self.data_total) * self.val_ratio)
        k = int(1/self.val_ratio)
        
        for indx in range(k):
            val_slice = (indx*num_of_val, (indx+1)*num_of_val)
            if indx == k-1:
                self.vals.append(self.data_total[val_slice[0]:])
                self.datas.append(self.data_total[:val_slice[0]])
            else:
                self.vals.append(self.data_total[val_slice[0]:val_slice[1]])
                self.datas.append(
                    self.data_total[:val_slice[0]]+self.data_total[val_slice[1]:])
