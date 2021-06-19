import pandas as pd
import random

class Loader:
    '''
    This class is to load data and feed data into model (C4.5)
    '''
    def __init__(self, path_to_data:str, attributes: list, class_col:str, val_ratio:int=0.1):
        '''
            Input:
                path_to_data: directory containing data
                attributes: list of strings that column name. Example ["HK01", "HK02"]
                class_col: String that is Name of column contain label.
                val_ratio: val / data_total, this will divide data_total into training and validation set.

        '''
        self.filePathToData = path_to_data
        self.val_ratio = val_ratio
        self.attributes = attributes
        self.class_col = class_col
        self.classes=None
        self.num_attributes = len(attributes)
        self.data_total=None
        self.vals = []
        self.datas = []

        self.__load_data()
        self.__split_dataset()
    
    def __load_data(self):
        df = pd.read_excel(self.filePathToData, sheet_name=0, index_col=None, header=0, usecols=self.attributes+[self.class_col])
        self.data_total = df.values.tolist()
        self.classes = list(set(df.iloc[:, -1]))

    def __split_dataset(self):
        # random.shuffle(self.data_total)
        val_ = int(self.val_ratio*10)
        data_ = 10 - val_
        part_ = len(self.data_total)//(val_+data_)
        data_pad = self.data_total+self.data_total
        for part in range(val_+data_ -1):
            self.vals.append(data_pad[part*part_:(part+val_)*part_])
            self.datas.append(data_pad[(part+val_)*part_:(part+val_+data_)*part_])