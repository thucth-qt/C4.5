from c45 import C45

c1 = C45("data/All.xlsx")
c1.load_data(["HK01", "HK02", "HK03", "HK04"], "Graduation")
c1.generateTree()
c1.generate_tree_dict()
# c1.printTree()
c1.draw_tree()
