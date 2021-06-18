import pandas as pd

class Loader:
    def __init__(self, pathToData):
        self.filePathToData = pathToData
        self.attributes=None
        self.data=None
        self.classes=None
        self.num_attributes=None
    
    def load_data(self, attributes: list, class_col):
        df = pd.read_excel(self.filePathToData, sheet_name=0, index_col=None, header=0, usecols=attributes+[class_col])
        self.attributes = attributes
        self.data = df.values.tolist()
        self.classes = list(set(df.iloc[:, -1]))
        self.num_attributes = len(attributes)
