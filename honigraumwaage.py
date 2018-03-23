import hal.scale as scale
import hal.keypad as keypad
import hal.lcd as lcd
from sending import Sending
import logging
import time

class Honigraumwaage:
    def __init__(self):
        self.lcd = lcd.HonigraumwaageLcd()
        self.lcd.showStatus("Starte")
        self.hiveMark = ""
        self.restart = False
        self.shutdown = False
        logging.basicConfig(filename='Honigraumwaage.log',level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')   
        self.sending = Sending()
        self.run()
        

    def run(self):
        self.restart = False
        self.shutdown = False
        with scale.Scale() as myScale:            

            def getFormatedWeight():
                val = myScale.getWeight()
                weight = "%3.1f" %(val)
                return weight

            #keypad callback
            def print_key(key):
                if key == 'D':
                    if self.hiveMark == "*0#":
                        self.lcd.showStatus("Fahre herrunter")
                        self.shutdown = True
                    else:
                        weight = getFormatedWeight()
                        self.lcd.showStatus("Sende %s %s" %(self.hiveMark, weight))
                        sendingStatus = self.sending.sendWeight(weight, self.hiveMark)
                        if sendingStatus:
                            self.lcd.showStatus("Senden OK")
                            self.hiveMark = ""
                            self.lcd.showMark(self.hiveMark)
                        else:
                            self.lcd.showStatus("Senden failed")
                elif key == 'C':
                    self.hiveMark = ""   
                    self.lcd.showStatus("reset numbers")
                elif key == 'A':
                    self.lcd.showStatus("reset")
                    self.hiveMark = ""
                    myScale.reset()
                    self.lcd.clear()
                else:
                    self.hiveMark += key
                    self.lcd.showMark(self.hiveMark)
                    
            with keypad.Keypad(print_key) as myKeypad:
                self.lcd.showStatus("")
                #Main Loop
                while not self.shutdown:
                    self.lcd.showWeight(getFormatedWeight())
                    time.sleep(0.4)
                    
        if self.shutdown:
            self._shutdown()

    def _shutdown(self):
        from subprocess import call
        call("sudo shutdown -h now", shell=True)
        
        
if __name__ == "__main__":
    honigraumwaage = Honigraumwaage()    
