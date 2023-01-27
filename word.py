class Word:
    def __init__(self, line):
        parts = line.strip().split(' ')
        self.head = parts[0]
        self.tags = parts[1].split(':')
        self.comment = None
        if len(parts) > 2:
            comment = ' '.join(parts[2:]).replace('#', '', 1).strip()
            if '"' not in comment and ':' not in comment:
                self.comment = comment
