from anytree import Node, RenderTree

# base
cw = Node("Chetwood")

# pod
mortgages = Node("Mortgages", parent=cw)
savings = Node("Savings", parent=cw)
payments = Node("Payments", parent=cw)
core = Node("Core", parent=cw)

# services
avm = Node("AVM", parent=mortgages)
fraud = Node("Fraud", parent=mortgages)

sjc = Node("Savings-Journal-Svc", parent=savings)
sps = Node("Savings-Person-Svc", parent=savings)
sds = Node("Savings-Deposit-Svc", parent=savings)
sys = Node("Savings-Payment-Svc", parent=savings)

ces = Node("Core-Email-Svc", parent=core)
cps = Node("Core-Payments-Svc", parent=core)
css = Node("Core-Secret-Svc", parent=core)

for pre, fill, node in RenderTree(cw):
    print("%s%s" % (pre, node.name))

from ete3 import Tree, TreeStyle, TextFace


ts = TreeStyle()
ts.show_leaf_name = True
ts.title.add_face(TextFace("Chetwood Services", fsize=20), column=0)

t = Tree()
A = t.add_child(name="A") # Adds a new child to the current tree root
                           # and returns it
B = t.add_child(name="B") # Adds a second child to the current tree
                           # root and returns it
C = A.add_child(name="C") # Adds a new child to one of the branches
D = C.add_sister(name="D") # Adds a second child to same branch as
                             # before, but using a sister as the starting
                             # point
R = A.add_child(name="R") # Adds a third child

t.render("tree_view.png", w=183, units="mm", tree_style=ts)
