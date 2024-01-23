class Array:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.address = 0
        self.initialized = [False for _ in range(size)]