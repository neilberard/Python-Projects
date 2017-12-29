"""Creating a class with property decorator"""


class MyProperty(object):
    def __init__(self):
        self.value = 5
        pass

    @property
    def value_a(self):
        return self.value

    @value_a.setter
    def value_a(self, value):
        self.value = value

    @value_a.deleter
    def value_a(self):
        self.value = None
        print 'deleting'



this = MyProperty()

del this.value_a
print this.value_a
