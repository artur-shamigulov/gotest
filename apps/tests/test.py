class A(object):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value + 1

    def super_hard(self):
        value = self.get_value()
        print (value)

class B(A):

    def get_value(self):
        return super(B, self).get_value() + 1

A(1).super_hard()
B(1).super_hard()