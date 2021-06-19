from trainer import Trainer
from c45 import C45
from loader import Loader
from trainer import Trainer

loader = Loader(pathToData="data/All.xlsx", 
                attributes=["HK01", "HK02", "HK03", "HK04","first4semesters"], 
                class_col="Graduation", 
                val_ratio=0.3)

c1 = C45()

trainer = Trainer(c1, loader)

best_k_fold_acc, best_model, best_acc, best_attrs = trainer.train(True)

print(best_model.fit([17, 5, 9, 11, 50]))
print(best_acc)
print(best_k_fold_acc)
print(best_attrs)
c1.generate_tree_dict()
c1.printTree()
c1.draw_tree("tree  k-fold")


c2, acc = trainer.train(False)

print(c2.fit([17, 5, 9, 11, 50]))
print(acc)

c2.generate_tree_dict()
c2.printTree()
c2.draw_tree("tree non k-fold")
