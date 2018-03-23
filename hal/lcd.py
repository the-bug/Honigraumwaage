import lcddriver

"""
Base class for interatcting with a two lined lcd Display.
lcddriver is from http://tutorials-raspberrypi.de/wp-content/uploads/scripts/hd44780_i2c.zip
"""

class Lcd(object):

    def __init__(self, firstRow = "", secoundRow = ""):
        self.firstRow = firstRow
        self.secoundRow = secoundRow
        self.show()

    def _setUp(self):
        self.lcd = lcddriver.lcd()
        self.clear()        

    def clear(self):
        self.lcd.lcd_clear()

    def show(self):
        self._setUp()
        self.lcd.lcd_display_string(self.firstRow, 1)
        self.lcd.lcd_display_string(self.secoundRow, 2)

    def _prepareRow(self, row):
        newRow = "{:12s}".format(row[:min(len(row),16)])
        # Debbuging purpose
        if(len(row) > 16 or False):
            print(len(row), len(newRow))
            print row
            print newRow
        return newRow        

    def showFirstRow(self, firstRow):
        self.firstRow = self._prepareRow(firstRow)
        self.show()

    def showSecoundRow(self, secoundRow):
        self.secoundRow = self._prepareRow(secoundRow)
        self.show()
        

class HonigraumwaageLcd(Lcd):

    def __init__(self):    
        super(HonigraumwaageLcd, self).__init__()
        self.weight = ""
        self.mark = ""
        self.sendingStatus = ""
    
    def showWeight(self, weight):
        self.weight = weight
        self._showWeightAndMark()

    def showMark(self, mark):
        self.mark = mark
        self._showWeightAndMark()

    def _showWeightAndMark(self):
        firstLine = "{:3s} {:3s} {:3s} {:4s}".format("Nr:", self.mark, "Kg:", self.weight)
        self.showFirstRow(firstLine)

    def showStatus(self, statusMessage):
        self.showSecoundRow(statusMessage)
        

if __name__ == "__main__":
    lcd = HonigraumwaageLcd()
    lcd.showWeight("12.5")
    lcd.showMark("121")
    lcd.showStatus("Alles tool!")
    
    
