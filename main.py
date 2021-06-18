from c45 import C45

c1 = C45("data/All.xlsx")
c1.load_data(["HK01", "HK02", "HK03", "HK04", "first4semesters"], "Graduation")
c1.split_dataset(0.1)
c1.train(k_fold=False)
c1.printTree()

c1.generate_tree_dict() 
c1.draw_tree()

# print(c1.fit([17,5,9,11,50]))