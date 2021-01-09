####
    #
    # Written by 
    #   Andrew Miller (andrewmiller0728@gmail.com)
    #   January 6, 2021
    #
    # Code modified from 
    #   "CircuitPython Animated Holiday Wreath Lights"
    # By 
    #   Kattni Rembor
    #   https://learn.adafruit.com/circuitpython-animated-holiday-wreath-lights/code
    #
    # APIs and documentation can be found at
    #   https://circuitpython.readthedocs.io/projects/magtag/en/latest/index.html#
    #   https://circuitpython.readthedocs.io/en/6.0.x/docs/index.html
    #
####


import time
import board
import digitalio
import neopixel

from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import (AMBER, BLUE, GOLD, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW)
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimateOnce, AnimationSequence
from adafruit_magtag.magtag import MagTag


###   Neopixel Strip   ###
 # Defines both the board pin and number of pixels on the strip

stripPin = board.D10
stripCnt = 30


###   Display Screen   ###
 # Defines brightness values (0-100%) for board & strip and the refresh delay value

boardBrightness = 0.75
stripBrightness = 0.5
refreshDelay = 60


###   Animation - Color Cycle   ###
 # Defines the colors to be used in the cycle and the speed at which to switch

cycleColors = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
cycleSpeed = 100


###   Animation - Comet   ###
 # Defines the colors, speeds, and tail lengths for the comet animation

cometColorA = WHITE
cometColorB = GOLD
cometColorC = RED

boardCometSpeed = 0.25
stripCometSpeed = 0.0625

boardCometTailLen = 3
stripCometTailLen = 15


###   Hardware Set-Up   ###
 # Sets up the MagTag board and Neopixels

magtag = MagTag()
boardPixels = magtag.peripherals.neopixels
boardPixels.brightness = boardBrightness
magtag.peripherals.neopixel_disable = False
stripPixels = neopixel.NeoPixel(stripPin, stripCnt, brightness=stripBrightness, auto_write=False)


###   Animation Sequences & Groups   ###
 # Creates and organizes the animations

animations = AnimationSequence(
    AnimationGroup(
        Solid(boardPixels, WHITE),
        ColorCycle(stripPixels, cycleSpeed, cycleColors),
        sync=True,
    ),
    AnimationSequence(
        AnimateOnce(
            AnimationGroup(
                Solid(boardPixels, WHITE),
                Comet(stripPixels, stripCometSpeed, cometColorA, tail_length=stripCometTailLen),
            ),
            AnimationGroup(
                Solid(boardPixels, WHITE),
                Comet(stripPixels, stripCometSpeed, cometColorB, tail_length=stripCometTailLen),
            ),
            AnimationGroup(
                Solid(boardPixels, WHITE),
                Comet(stripPixels, stripCometSpeed, cometColorC, tail_length=stripCometTailLen),
            )
        )
    ),
    AnimationGroup(
        Solid(boardPixels, WHITE),
        Solid(stripPixels, AMBER)
    ),
    AnimationGroup(
        Solid(boardPixels, AMBER),
        Solid(stripPixels, 0),
    ),
    auto_clear=True,
)


###   Background & Text   ###
 # Draws the background image and static text

magtag.set_background("/led.bmp")

magtag.add_text(text_color=0x000000, text_position=(5, 10), text_scale=2)
magtag.set_text("Light Selector:", auto_refresh=False)

magtag.add_text(text_color=0x000000, text_position=(25, 65))
magtag.set_text("A: Rainbow Cycle\n"
                "B: Comet\n"
                "C: Amber\n"
                "D: Dim",
                index=1,
                auto_refresh=False)

magtag.add_text(text_color=0x000000, text_position=(0, 120))
magtag.set_text("    A           B           C           D", index=2)

magtag.add_text(text_color=0x000000, text_position=(250, 10))
magtag.set_text("{} V".format("-4.20"), index=3)


###   Main Loop   ###
 # Loops continuously while the program is running

timeStart = time.time()
timeDelta = time.time() - timeStart

while True:

    # Update battery level every <refreshDelay> seconds or on button press
    timeDelta = time.time() - timeStart
    if timeDelta > refreshDelay:
        timeStart = time.time()
        magtag.set_text("{} V".format(round(magtag.peripherals.battery, 2)), index=3)

    # Animate lights
    if magtag.peripherals.button_a_pressed:
        animations.activate(0)
    elif magtag.peripherals.button_b_pressed:
        animations.activate(1)
    elif magtag.peripherals.button_c_pressed:
        animations.activate(2)
    elif magtag.peripherals.button_d_pressed:
        animations.activate(3)
    animations.animate()
    
    # Sleep CPU
    time.sleep(0.005)
