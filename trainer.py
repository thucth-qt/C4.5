class Trainer:
    def __init__ (self, model, data_loader):
        self.model=model
        self.data_loader = data_loader

    def train(self, is_k_fold=False):
        model = self.model
        if not is_k_fold:
            model.load_data(attributes=self.data_loader.attributes,
                                 data=self.data_loader.datas[0], classes=self.data_loader.classes)
            model.generate_tree()
            acc = self.validate(model, self.data_loader.vals[0])
            return model, acc
        else:
            scores=[]
            best_model=None
            best_acc=-1
            for data, val in zip(self.data_loader.datas, self.data_loader.vals):
                model = self.model
                model.load_data(attributes=self.data_loader.attributes,
                                     data=data, classes=self.data_loader.classes)
                model.generate_tree()
                acc = self.validate(val)
                scores.append(acc)
                if acc>best_acc:
                    best_acc=acc
                    best_model=model
            k_fold_acc = scores.mean()
            return best_model, best_acc, k_fold_acc

    def validate(self, model, val):
        hit=0
        for example in val:
            data = example[:-1]
            label = example[-1]
            predict = model.fit(data)
            if (predict == label):
                hit+=1
        return hit/len(val)
    
