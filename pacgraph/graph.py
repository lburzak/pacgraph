from typing import Optional

from pyvis.network import Network

from pacgraph.models import Package

MIN_NODE_SIZE = 5
MAX_NODE_SIZE = 60


def show_packages_graph(packages: list[Package], max_packages: Optional[int] = None):
    if max_packages is not None and len(packages) > max_packages:
        print(f"too many packages, showing top {max_packages}")
        packages.sort(key=lambda package: package.size, reverse=True)
        packages = packages[:max_packages]

    package_sizes = [package.size for package in packages]
    scaler = MinMaxScaler(package_sizes, (MIN_NODE_SIZE, MAX_NODE_SIZE))

    package_name_to_node_id = {}

    # TODO: Remove frame and make it 100vw/100vh
    net = Network(width='98vw', height='98vh')

    for index, package in enumerate(packages):
        package_name_to_node_id[package.name] = index
        net.add_node(index, label=package.name, size=scaler.scale(package.size),
                     color="red" if package.is_explicitly_installed else None)

    for package in packages:
        package_node_id = package_name_to_node_id[package.name]

        for dependency in package.dependencies:
            if dependency in package_name_to_node_id:
                dependency_node_id = package_name_to_node_id[dependency]
                net.add_edge(package_node_id, dependency_node_id)

    net.show('nodes.html')


class MinMaxScaler:
    min_value: int
    max_value: int
    bottom_bound: int
    top_bound: int

    def __init__(self, values: [int], bounds: tuple[int, int]) -> None:
        self.min_size = min(values)
        self.max_size = max(values)
        self.bottom_bound = bounds[0]
        self.top_bound = bounds[1]

    def scale(self, size):
        return self.bottom_bound + (size - self.min_size) * (self.top_bound - self.bottom_bound) / (
                self.max_size - self.min_size)
