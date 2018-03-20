import hal.scale as scale
import hal.keypad as keypad
import time
from sending import Sending
import logging

    
hiveMark = ""
restart = False
def main():
    logging.basicConfig(filename='Honigraumwaage.log',level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' )    
    
    global hiveMark
    global restart
    
    restart = False
    hiveMark = ""
    
    print("Starte")
    
    sending = Sending()
    
    with scale.Scale() as myScale:
        def print_key(key):
            global hiveMark
            global restart
            if key == 'D':
                weight = myScale.getWeight()
                print('Sende Gewicht %d mit Nummer %s' %(weight, hiveMark))                
                sendingStatus = sending.sendWeight(weight, hiveMark)
                if sendingStatus:
                    print "Senden OK"
                else:
                    print "Beim Senden ist etwas schiefgegangen"                        
                hiveMark = ""                
            elif key == 'C':
                hiveMark = ""   
                print("Setzte Nummer zurück")                                
            elif key == 'A':
                print("Starte Anwendung neu")
                hiveMark = ""
                restart = True
            else:
                hiveMark += key
                print(hiveMark)
                
        with keypad.Keypad(print_key) as myKeypad:
            while not restart:
                val = myScale.getWeight()
                print "Gewicht: %d" %(val)
                time.sleep(1)

    if restart:
        print("restart")
        main()
    

if __name__ == "__main__":
    main()
