from time import sleep, time


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
    print("running Foo")
    for i in range(3):
        print(i)
    print("bye from Foo")


@Behaviour("Loop")
def loop():
    while True:
        print("Looping -> " + str(time()))
        sleep(5)

