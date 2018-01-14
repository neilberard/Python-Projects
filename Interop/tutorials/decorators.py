
this = 2
my_list = [1,3,3,4]

def make_iterable(func):
    """
    Decorator -
    """
    def wrap(*args):
        for item in args:
            for i in item:
                yield func(i)
    return wrap


@make_iterable
def iterator_function(single_object):
    print single_object

iterator_function(my_list)
