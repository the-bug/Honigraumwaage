import hal.scale as scale
import hal.keypad as keypad
from sending import Sending
import logging
import time

class Honigraumwaage:
    def __init__(self):
        print("Starte")
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
            def print_key(key):
                if key == 'D':
                    if self.hiveMark == "*0#":
                        print "Fahre herrunter"    
                        self.shutdown = True
                    else:
                        weight = myScale.getWeight()
                        print('Sende Gewicht %d mit Nummer %s' %(weight, self.hiveMark))                
                        sendingStatus = self.sending.sendWeight(weight, self.hiveMark)
                        if sendingStatus:
                            print "Senden OK"
                        else:
                            print "Beim Senden ist etwas schiefgegangen"                        
                    self.hiveMark = ""                
                elif key == 'C':
                    self.hiveMark = ""   
                    print("Setzte Nummer zurück")                                
                elif key == 'A':
                    print("Starte Anwendung neu")
                    self.hiveMark = ""
                    myScale.reset()
                else:
                    self.hiveMark += key
                    print(self.hiveMark)
                    
            with keypad.Keypad(print_key) as myKeypad:
                while not self.shutdown:
                    val = myScale.getWeight()
                    print "Gewicht: %3.1f" %(val)
                    time.sleep(1)
                    
        if self.shutdown:
            self._shutdown()

    def _shutdown(self):
        from subprocess import call
        call("sudo shutdown -h now", shell=True)
        
        
if __name__ == "__main__":
    honigraumwaage = Honigraumwaage()    
