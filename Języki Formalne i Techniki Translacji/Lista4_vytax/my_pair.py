class Pair:
    def __init__(self, name, arg=None, labels=None):
        if labels is None: labels = []
        self.name = name
        self.arg = arg
        self.labels = labels

    def __str__(self):
        s = ''
        s += self.name
        if self.arg is not None: s += f' {self.arg}'
        return s