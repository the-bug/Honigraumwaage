#!/usr/bin/python

from pad4pi import rpi_gpio

"""
Keypad is hardware abstraction layer for a 4x4 keypad used with the Honigraumwaage.
It has to be called within an with statement to free GPIO afterwards.
A callback hanbling a string as an argument is to be given in the construction.

GPIO pins and keypad layout can be adapted.
"""

class Keypad:

    def __init__(self, callback):
        matrix = [["1","2","3", "A"],
            ["4","5","6", "B"],
            ["7","8","9", "C"],
            ["*", "0", "#", "D"]]

        spalte = [12, 16, 20, 21]
        zeile = [18, 23, 24, 25]
        
        factory = rpi_gpio.KeypadFactory()
        self.keypad = factory.create_keypad(keypad=matrix, row_pins=zeile, col_pins=spalte)

        self.keypad.registerKeyPressHandler(callback)

    def _cleanUp(self):
        print("Keypad._cleanUp")
        self.keypad.cleanup()

        
    def __enter__(self):
        return self
     
    def __exit__(self, exc_type, exc_value, traceback):
        print("Keypad.__exit__")
        self._cleanUp()

if __name__ == "__main__":
    
    import time
    def print_key(key):
        if key == 'D':
            print('D was pressed')
        print(key)

    with Keypad(print_key) as myKeypad:
        while True:
            time.sleep(10)
        
    


