from pyvis.network import Network

from pacgraph.models import Package

MIN_NODE_SIZE = 5
MAX_NODE_SIZE = 60


def normalize_node_size(size, min_size, max_size):
    return MIN_NODE_SIZE + (size - min_size) * (MAX_NODE_SIZE - MIN_NODE_SIZE) / (max_size - min_size)


def show_packages_graph(packages: list[Package]):
    if len(packages) > 200:
        print("too many packages, showing top 200")
        packages.sort(key=lambda package: package.size, reverse=True)
        packages = packages[:200]

    # TODO: Remove frame and make it 100vw/100vh
    net = Network(width='98vw', height='98vh')

    package_sizes = [package.size for package in packages]
    min_size = min(package_sizes)
    max_size = max(package_sizes)

    for index, package in enumerate(packages):
        net.add_node(index, label=package.name, size=normalize_node_size(package.size, min_size, max_size))

    net.show('nodes.html')
