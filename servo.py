from PiicoDev_Servo import PiicoDev_Servo, PiicoDev_Servo_Driver, sleep_ms

ENGAGED_DEG = 140
RETRACTED_DEG = 10
MIDDLE_ISH_DEG = 90

class Servo:
    def __init__(self, channel=1) -> None:
        # Initialise the Servo Driver Module
        controller = PiicoDev_Servo_Driver()
        # Simple setup: Attach a servo to channel 1 of the controller with default properties
        self.servo = PiicoDev_Servo(controller, channel)
        self.locked = None

    def toggle(self):
        if self.servo.angle < MIDDLE_ISH_DEG:
            self.servo.angle = ENGAGED_DEG
        else:
            self.servo.angle = RETRACTED_DEG

    def set(self, engage):
        if engage:
            self.servo.angle = ENGAGED_DEG
            self.locked = True
        else:
            self.servo.angle = RETRACTED_DEG
            self.locked = False

    def test(self):
        # Step the servo
        self.servo.angle = RETRACTED_DEG
        sleep_ms(1000)
        self.servo.angle = ENGAGED_DEG
        sleep_ms(5000)
        self.servo.angle = MIDDLE_ISH_DEG

def servo_test():
    print("Servo test . . . ")
    servo = Servo()
    servo.test()
    servo.set(True)
    sleep_ms(1000)
    servo.set(False)
    print("Servo test . . . Done")

if __name__ == "__main__":
    servo_test()
