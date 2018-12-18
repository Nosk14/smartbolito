import os
from random import randint
from time import sleep

import board
from neopixel import NeoPixel, RGB

NUM_LEDS = 50
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

behaviours = []
leds = NeoPixel(board.D18, NUM_LEDS, auto_write=False, pixel_order=RGB, brightness=float(os.getenv("BRIGHTNESS", "0.2")))


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
            leds[i] = (255, 0, 0)
        leds.show()
        sleep(0.5)
        turn_off()
        sleep(0.5)


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


@Behaviour("Random color trail")
def random_color_trail():
    while True:
        trail_color = _get_random_color()
        for i in range(NUM_LEDS):
            turn_off()
            leds[i] = trail_color
            leds.show()
            sleep(0.1)


@Behaviour("Sparkling")
def sparkling():
    while True:
        for i in range(NUM_LEDS):
            leds[i] = (255, 255, 255) if randint(0, 9) < 6 else (0, 0, 0)
            leds.show()
        sleep(0.01)


@Behaviour("Misco")
def misco():
    while True:
        leds.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        leds.show()
        sleep(0.3)


@Behaviour("Jones")
def jones():
    while True:
        for i in range(NUM_LEDS):
            turn_off()
            leds[i] = (randint(0, 255), randint(0, 255), randint(0, 255))
            leds.show()
            sleep(i/1000)


@Behaviour("Psycho")
def psycho():
    while True:
        for i in range(NUM_LEDS):
            turn_off()
            leds[i] = (randint(0, 255), randint(0, 255), randint(0, 255))
            leds.show()
            sleep(i/1000) if i < 40 else sleep(0.25)

