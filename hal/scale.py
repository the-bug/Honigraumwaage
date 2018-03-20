import RPi.GPIO as GPIO
from hx711 import HX711

"""
Scale is hardware abstraction layer for a HX711 with an attached bathroom scale.
Instatiation yields the setup.
Than Just call getWeight.
"""
class Scale:

    def __init__(self):
        self._referenceUnit = -25
    
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(self._referenceUnit)
        self.reset()
        
    def _cleanUp(self):
        print("Scale._cleanUp")
        GPIO.cleanup()
        
    def __enter__(self):
        return self
     
    def __exit__(self, exc_type, exc_value, traceback):
        print("Scale.__exit__")
        self._cleanUp()
        
    def __enter__(self):
        return self

    def reset(self):
        self.hx.reset()
        self.hx.tare()        
        
    def getWeight(self):
        #self.hx.power_up()
        returnValue = self.hx.get_weight(5)
        #self.hx.power_down()
        return returnValue

if __name__ == "__main__":

    import time
    
    with Scale() as myScale:
        while True:
            val = myScale.getWeight()
            print "val: %d" %(val)
            time.sleep(0.5)
