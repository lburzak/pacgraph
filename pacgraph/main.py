import pacman
from pacgraph.graph import show_packages_graph

packages = pacman.get_installed_packages()

show_packages_graph(packages, max_packages=200)
