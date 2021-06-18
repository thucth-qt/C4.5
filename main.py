from c45 import C45
from loader import Loader

loader = Loader("data/All.xlsx")
loader.load_data(["HK01", "HK02", "HK03", "HK04","first4semesters"], "Graduation")

c1 = C45(attributes=loader.attributes, data=loader.data, classes=loader.classes)
c1.generateTree()







# c1.generate_tree_dict()
# c1.printTree()
# c1.draw_tree()
