from c45 import C45

c1 = C45("data/All.xlsx")
c1.load_data(["HK01", "HK02", "HK03", "HK04", "HK05", "HK06"], "Graduation")
c1.generateTree()
c1.printTree()
