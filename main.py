""" Bottle sorter """

import serial
from time import sleep
import finder

# variables
port   = 'COM4'
camera = 1

output = ''

# inti things here
belt_controller = serial.Serial(port, 9600)
bottle_finder = finder.BottleFinder(1)

def listen():
    """ returns data from belt controller """
    return int(belt_controller.readline().decode('UTF-8'))

def analyze():
    """ kicks bottle to separate from other things """
    output = bottle_finder.detect_bottle()

    if output:
        print("Bottle found")
        belt_controller.write(b'b')
        print('kicked')
        return

    print("Bottle not detected")
    belt_controller.write(b'n')


# main loop
run = 1
while run:
    incoming_data = listen()
    print(incoming_data)
    #print(type(incoming_data))

    if incoming_data == 1:
        print("Object Detected")
        sleep(1)
        analyze()