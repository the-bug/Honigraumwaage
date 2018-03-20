import hal.scale as scale
import hal.keypad as keypad
import time
from sending import sendWeight
    
hiveMark = ""
restart = False
def main():
    global hiveMark
    global restart
    restart = False
    hiveMark = ""
    print("Starte")
    with scale.Scale() as myScale:
        def print_key(key):
            global hiveMark
            global restart
            if key == 'D':
                weight = myScale.getWeight()
                print('Sende Gewicht %d mit Nummer %s' %(weight, hiveMark))                
                sendWeight(weight, hiveMark)
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
