import board
import os
from time import sleep, time
from neopixel import NeoPixel, GRB
from random import randint


NUM_LEDS = 50
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

behaviours = []
leds = NeoPixel(board.D18, NUM_LEDS, auto_write=False, pixel_order=GRB, brightness=float(os.getenv("BRIGHTNESS", "0.2")))


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


def _get_random_color():
    c = randint(0, len(colors) - 1)
    return colors[c]


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
    while True:
        i = randint(0, NUM_LEDS-1)
        leds[i] = _get_random_color()
        leds.show()
        sleep(0.25)


@Behaviour("Full random")
def full_random_colors():
    while True:
        for i in range(NUM_LEDS):
            leds[i] = _get_random_color()
        leds.show()
        sleep(0.5)


@Behaviour("Random blink")
def random_blink():
    while True:
        leds.fill(_get_random_color())
        leds.show()
        sleep(0.5)
        turn_off()
        sleep(0.5)


