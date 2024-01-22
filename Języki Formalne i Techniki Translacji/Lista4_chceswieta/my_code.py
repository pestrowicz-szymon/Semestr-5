class Code:
    def __init__(self, name, arg=None, labels=None):
        if labels is None:
            labels = []
        self.name = name
        self.arg = arg
        self.labels = labels
    
    def __str__(self):
        s = ''
        if len(self.labels) > 0:
            for label in self.labels:
                s += f'{label} '
            s += ': '
        s += self.name
        if self.arg is not None:
            s += f' {self.arg}'
        return s