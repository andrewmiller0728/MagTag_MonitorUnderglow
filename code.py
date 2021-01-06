import time
import board
import digitalio
import neopixel
from adafruit_magtag.magtag import MagTag

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.sequence import AnimationSequence, AnimateOnce
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE, GOLD


###   Neopixel Strip   ###
 # Defines both the board pin and number of pixels on the strip

stripPin = board.D10
stripCnt = 30


###   Brightness   ###
 # Defines brightness values (0-100%) for board and strip

boardBrightness = 0.75
stripBrightness = 0.5


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
        Solid(stripPixels, WHITE)
    ),
    AnimationGroup(
        Solid(boardPixels, 0),
        Solid(stripPixels, 0),
    ),
    auto_clear=True,
)


###   Background & Text   ###
 # Draws the background image and static text

magtag.set_background("/led.bmp")

magtag.add_text(text_color=0x000000, text_position=(0, 10), text_scale=2)
magtag.set_text(" Light Selector:", auto_refresh=False)

magtag.add_text(text_color=0x000000, text_position=(0, 65))
magtag.set_text("   - A: Rainbow Cycle\n"
                "   - B: Comet\n"
                "   - C: Solid White\n"
                "   - D: All Off",
                index=1,
                auto_refresh=False)
                
magtag.add_text(text_color=0x000000, text_position=(0, 120))
magtag.set_text("    A           B           C           D", index=2)


###   Main Loop   ###
 # Loops continuously while the program is running

while True:
    if magtag.peripherals.button_a_pressed:
        animations.activate(0)
    elif magtag.peripherals.button_b_pressed:
        animations.activate(1)
    elif magtag.peripherals.button_c_pressed:
        animations.activate(2)
    elif magtag.peripherals.button_d_pressed:
        animations.activate(3)
    animations.animate()
    time.sleep(0.005)