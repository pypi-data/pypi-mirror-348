import sys


sys.path.append("/Users/stephen.swannell/Projects/git/GleamsMachine/dev/pytest-coveragemarkers/pytest_coveragemarkers")


from pathlib import Path
from pytest_coveragemarkers.utils.yml_processing import load_yaml
from rich import print as show

THIS_DIR = Path(__file__).parent

print(THIS_DIR)
config = {}
load_yaml(config=config, yaml_file=str(THIS_DIR / "markers.yml"))
show(config)

# process yaml
# - check `next` values
# with this change it shouldnt impact existing coverage markers functionality and so no new version needed,

# `next` is only used by reporting - not tests
marker_names = [marker["name"] for marker in config["markers"]]

for marker in config["markers"]:
    if "next" in marker.keys():
        assert marker["next"] in marker_names

# so once we have some kind of tree lets view it.
from ete3 import Tree, TreeStyle, TextFace


ts = TreeStyle()
ts.show_leaf_name = True
ts.title.add_face(TextFace("Chetwood Services", fsize=20), column=0)

t = Tree()

for marker in config["markers"]:

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
