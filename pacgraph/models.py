class Package:
    name: str
    size: int
    dependencies: [str]

    def __init__(self, name: str, size: int, dependencies: [str]):
        self.name = name
        self.size = size
        self.dependencies = dependencies

    def __repr__(self) -> str:
        return f"Package({self.name}, {self.size}, {self.dependencies}"
