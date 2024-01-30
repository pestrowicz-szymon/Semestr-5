class LabelGenerator:
    def __init__(self):
        self.label_number = 0

    def get_label(self, off_by_one=False):
        self.label_number += 1
        s = 'l'
        if off_by_one:
            s += '-'
        s += f'{self.label_number}'
        return s