from trainer import Trainer
from c45 import C45
from loader import Loader

loader = Loader(path_to_data="data/All.xlsx", 
                attributes=["HK01", "HK02", "HK03", "HK04","first4semesters"], 
                class_col="Graduation", 
                val_ratio=0.2)

#k fold
c1 = C45()
trainer1 = Trainer(c1, loader)
best_k_fold_acc, best_model, best_acc, best_attrs = trainer1.train(is_k_fold=True,prune=True)

best_model.printTree()
best_model.draw_tree("tree k-fold")

#Non k fold
c2 = C45()
trainer2 = Trainer(c2, loader)
c2, acc = trainer2.train(is_k_fold=False, prune=True)

c2.printTree()
c2.draw_tree("tree non k-fold")

#predict
input = [22, 10, 20, 10, 62]
predict1 = c1.fit(input)
predict2 = c2.fit(input)

print("Input 1: {} preddict 1: {}".format(input, predict1))
print("Input 2: {} preddict 2: {}".format(input, predict2))

