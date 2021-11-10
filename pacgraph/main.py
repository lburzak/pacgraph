import pacman
from pacgraph.graph import show_packages_graph

packages = pacman.get_packages()

show_packages_graph(packages)
