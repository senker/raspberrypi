#!/usr/bin/env python
#
#  Light up an LED on GPIO pin 7 for thirty seconds
#

import sys
import RPi.GPIO as GPIO
import time
import random

def print_state( led_pins, pin_states ):
    if len(led_pins) != len(pin_states):
        raise Exception('Length mismatch between led_pins and pin_states')
    output = ""
    for i, j in enumerate(led_pins):
        output += "%2d=%1d " % ( j, pin_states[i] )
    print output

def generate_pin_states( led_pins, pin_states, mode=2 ):
    state_map = [ GPIO.LOW, GPIO.HIGH ]
    if mode == 0:
        pin_states = [ GPIO.LOW for x in led_pins ]
    elif mode == 1:
        pin_states = [ GPIO.HIGH for x in led_pins ]
    elif mode == 2:
        pin_states = [ state_map[random.randint(0,1)] for x in led_pins ]
    elif mode == 3:
        if pin_states[0] == GPIO.HIGH:
            state_order = [ GPIO.HIGH, GPIO.LOW ]
        else:
            state_order = [ GPIO.LOW, GPIO.HIGH ]
        ### try to turn everything on
        for state in state_order:
            for i in range(len(pin_states)):
                if pin_states[i] != state:
                    pin_states[i] = state
                    return pin_states
    elif mode == 4:
        _WIDTH = 3
        ### first check to ensure we have the desired number of pins lit up; if
        ### not, initialize all pins
        num_on = 0
        num_ideal = _WIDTH
        for i in pin_states:
            if i == GPIO.HIGH:
                num_on += 1
        if num_on != num_ideal:
            print "Initializing all pins--%d on, but %d ideal" % (num_on, num_ideal)
            pin_states[0:num_ideal] = [ GPIO.HIGH for x in range(num_ideal) ]
            pin_states[num_ideal:] = [ GPIO.LOW for x in range(len(pin_states)-num_ideal) ]

        # find the first pin that's on and turn it off; then step and turn on
        i = 0
        last_state = pin_states[-1]
        while not (pin_states[i] == GPIO.HIGH and last_state == GPIO.LOW):
            last_state = pin_states[i]
            i = (i + 1) % len(pin_states)
        pin_states[i] = GPIO.LOW
        pin_states[(i+_WIDTH) % len(pin_states)] = GPIO.HIGH
        return pin_states

    elif mode == 99:
        pin_states = []
        for i in led_pins:
            if i == 13 or i == 19:
                pin_states.append( GPIO.HIGH )
            else:
                pin_states.append( GPIO.LOW )
    else:
        pin_states = [ GPIO.HIGH for x in led_pins ]

    return pin_states

if __name__ == "__main__":
    led_pins = [ 26, 19,  6, 13, 12, 21, 20 ]
    pin_states = [ GPIO.HIGH for x in led_pins ]

    if len(sys.argv) > 1:
        led_mode = int(sys.argv[1])
    else:
        led_mode = 2

    GPIO.setmode( GPIO.BCM )
    GPIO.setup( led_pins, GPIO.OUT, initial=GPIO.LOW )

    try:
        while True:
            pin_states = generate_pin_states( led_pins, pin_states, mode=led_mode )
#           print_state( led_pins, pin_states )
            GPIO.output( led_pins, pin_states )
            time.sleep(0.25)

    except KeyboardInterrupt:
        print "Cleaning up!"
        GPIO.cleanup()
