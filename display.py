
from PiicoDev_SSD1306 import *

class Display:
    def __init__(self) -> None:
        self.display = create_PiicoDev_SSD1306()

    def display_setup_state(self, msg, msg2=None,msg3=None):
        self.display.fill(0)
        self.display.text("Setting up . . .", 0,0, 1) # literal string
        self.display.text(msg, 0,15, 1) # string variable
        if msg2 is not None:
            self.display.text(msg2, 0,30, 1)
        if msg3 is not None:
            self.display.text(msg3, 0,45, 1)
        self.display.show()

    def update_display(self, tempC, locked_state):
        self.display.fill(0)
        self.display.text("Temperature", 0,0, 1) # literal string
        self.display.text("{:.2f}".format(tempC), 0,15, 1) # string variable
        self.display.text("Lock Status", 0,30, 1) # print a variable
        self.display.text(f"{locked_state}", 0,45, 1) # use formatted-print
        self.display.show()

    def test(self):
        self.display.hline(10,10, 80, 1) # horizontal line 80px long from (10,10)
        self.display.show()
        sleep_ms(500)

        self.display.vline(10,10, 35, 1) # vertical line 35px long from (10,10)
        self.display.show()
        sleep_ms(500)

        self.display.line(10,45, 90,10, 1) # two-point line from (10,45) to (90,10)
        self.display.show()
        sleep_ms(500)

        myString = "this is me"
        myNumber = 123.4567

        self.display.text("Hello, World!!!!!!!!!!!!!!", 0,0, 1) # literal string
        self.display.text(myString, 0,15, 1) # string variable
        self.display.text(str(myNumber), 0,30, 1) # print a variable
        self.display.text("{:.2f}".format(myNumber), 0,45, 1) # use formatted-print
        self.display.show()
        sleep_ms(10000)

        self.display.rect(10, 10, 20, 50, 1) # unfilled rectangle
        self.display.fill_rect(50, 10, 50, 40, 1) # filled rectangle (white)
        self.display.fill_rect(60, 20, 30, 20, 0) # filled rectangle (black)
        self.display.show()
        sleep_ms(3000)
        self.display.fill(0)
        self.display.show()

if __name__ == "__main__":
    d = Display()
    d.test()
