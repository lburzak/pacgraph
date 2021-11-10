class Package:
    name: str
    size: int
    dependencies: [str]
    is_explicitly_installed: bool

    def __init__(self, name: str, size: int, dependencies: [str], is_explicitly_installed: bool):
        self.name = name
        self.size = size
        self.dependencies = dependencies
        self.is_explicitly_installed = is_explicitly_installed

    def __repr__(self) -> str:
        return f"Package({self.name}, {self.size}, {self.dependencies}"
