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

    package_name_to_node_id = {}

    for index, package in enumerate(packages):
        package_name_to_node_id[package.name] = index
        node_size = normalize_node_size(package.size, min_size, max_size)
        net.add_node(index, label=package.name, size=node_size,
                     color="red" if package.is_explicitly_installed else None)

    for package in packages:
        package_node_id = package_name_to_node_id[package.name]

        for dependency in package.dependencies:
            if dependency in package_name_to_node_id:
                dependency_node_id = package_name_to_node_id[dependency]
                net.add_edge(package_node_id, dependency_node_id)

    net.show('nodes.html')
