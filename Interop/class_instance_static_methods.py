from Interop import classes

class MyClass(object):
    x = 5

    def method(self):
        """effects only the instance of the class"""
        return 'instance method called', self

    @classmethod
    def classmethod(cls):
        """effects the class and instances of that class"""
        cls.x = 10
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'

obj = MyClass()
obj2 = MyClass()
print MyClass.method(obj)

obj.classmethod()

print obj2.x