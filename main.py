from trainer import Trainer
from c45 import C45
from loader import Loader
from trainer import Trainer

loader = Loader(pathToData="data/All.xlsx", 
                attributes=["HK01", "HK02", "HK03", "HK04","first4semesters"], 
                class_col="Graduation", 
                val_ratio=0.2)

c1 = C45()

trainer = Trainer(c1, loader)

best_c1, best_acc, acc_kfold = trainer.train(True)

print(best_c1.fit([17, 5, 9, 11, 50]))
print(best_acc)
print(acc_kfold)


c1, acc = trainer.train(False)

print(c1.fit([17, 5, 9, 11, 50]))
print(acc)

# c1.generate_tree_dict()
# c1.printTree()
# c1.draw_tree()
