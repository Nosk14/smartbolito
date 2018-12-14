import board
from time import sleep, time
from neopixel import NeoPixel, GRB
from random import randint

NUM_LEDS = 50

behaviours = []
leds = NeoPixel(board.D18, NUM_LEDS, auto_write=False, pixel_order=GRB)


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


def turn_off():
    leds.fill((0, 0, 0))
    leds.show()


@Behaviour("Alarm")
def alarm():
    while True:
        for i in range(NUM_LEDS):
            leds[i] = (0, 255, 0)
        leds.show()
        sleep(1)
        turn_off()
        sleep(1)


@Behaviour("Random")
def random_colors():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    while True:
        i = randint(0, NUM_LEDS-1)
        c = randint(0, len(colors)-1)
        leds[i] = colors[c]
        leds.show()
        sleep(0.25)

