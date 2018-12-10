
behaviours = []


class Behaviour:

    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        global behaviours
        behaviours.append({
            'name': self.name,
            'function_name': func.__name__,
            'function': func
            })

        return func


@Behaviour("Foo")
def foo():
    pass


@Behaviour("Bar")
def bar():
    pass

