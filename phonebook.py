class PhoneBook(object):
    def __init__(self):
        self.numbers = {}

    def add(self, name, phone):
        self._add(name, phone)

    def _add(self, name, phone):
        self.numbers[name] = phone

    def lookup(self, name):
        return self.numbers[name]

    def names(self):
        return set(self.numbers.keys())

    def close(self):
        pass
