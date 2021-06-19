class Trainer:
    '''
    This class is to make training data with different methods.
    main function of this class: train()
    '''
    def __init__ (self, model, data_loader):
        self.model=model
        self.data_loader = data_loader

    def train(self, is_k_fold=False, prune=False):
        '''
            Input:
                is_k_fold: if True, data will devide into k  parts, fold these parts during training, then compute average acc.
                prune: if True, we will prune last leaf, that means we will merge two branches if they are the same label.
        '''
        model = self.model
        if not is_k_fold:
            model.load_data(attributes=self.data_loader.attributes,
                                 data=self.data_loader.datas[0], classes=self.data_loader.classes)
            model.generate_tree(prune)
            acc = self.__validate(model, self.data_loader.vals[0])
            return model, acc
        else:
            best_k_fold_acc=-1
            best_model=None
            best_acc=None
            best_attrs=[]

            for num_attr in range(1,len(self.data_loader.attributes)+1):
                best_model_, best_acc_, k_fold_acc_ = self.__k_fold_validate(
                    model, self.data_loader.attributes[:num_attr], prune)
                if best_k_fold_acc < k_fold_acc_:
                    best_k_fold_acc = k_fold_acc_
                    best_model = best_model_
                    best_acc = best_acc_
                    best_attrs = self.data_loader.attributes[:num_attr]
            return best_k_fold_acc, best_model, best_acc, best_attrs

    def __validate(self, model, val):
        '''
        compute accuracy of model. 
        
        Return:
            number of true prediction / total prediction
        '''
        hit=0
        for example in val:
            data = example[:-1]
            label = example[-1]
            predict = model.fit(data)
            if (predict == label):
                hit+=1
        return hit/len(val)
    
    def __k_fold_validate(self, model, attrs, prune=False):
        scores = []
        best_model = None
        best_acc = -1
        for data, val in zip(self.data_loader.datas, self.data_loader.vals):
            model_ = model
            model_.load_data(attributes=attrs,
                            data=data, classes=self.data_loader.classes)
            model_.generate_tree(prune)
            acc = self.__validate(model_, val)
            scores.append(acc)
            if acc > best_acc:
                best_acc = acc
                best_model = model_
        k_fold_acc = sum(scores)/len(scores)
        return best_model, best_acc, k_fold_acc
