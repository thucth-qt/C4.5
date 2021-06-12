#!/usr/bin/env python
import pdb
from c45 import C45
from my_c45 import MyC45

c1 = C45("data/graduation.csv", "data/attribute.txt")
c1.fetchData()
c1.preprocessData()
c1.generateTree()
c1.printTree()


# c2 = MyC45("data/graduation.xlsx")


