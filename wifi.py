import network
import time
import ubinascii
from buzzer import Buzzer
from utime import sleep_ms
from display import Display
from log_manager import get_logger
import json


class Wifi:
    MAX_RETRIES = 10

    def __init__(self, wifi_ssid, wifi_password, buzzer: Buzzer) -> None:
        # Fill in your WiFi network name (ssid) and password here:
        # Connect to WiFi
        self.wlan = network.WLAN(network.STA_IF)
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.buzzer = buzzer
        self.logger = get_logger(__name__)
        self.mac = None

    def connect(self, display=None, watchdog=None):
        if self.wlan.isconnected() == True:
            self.logger.info("Wifi already connected")
            return
        self.buzzer.play_pip()
        self.buzzer.play_pip()

        self.wlan.active(True)
        sleep_ms(50)
        self.logger.info(f"Wifi active {self.wlan.active()}")
        self.logger.debug(f"{self.wlan}")
        self.wlan.connect(self.wifi_ssid, self.wifi_password)
        self.logger.debug(f"{self.wlan}")
        count = 0
        while self.wlan.isconnected() == False and count < self.MAX_RETRIES:
            self.logger.info(
                f"Waiting for connection to {self.wifi_ssid}, {self.wlan}... ({count+1}/{self.MAX_RETRIES})"
            )
            self.logger.info(f"Wifi active {self.wlan.active()}")
            if display is not None:
                display.display_setup_state(f"{self.wlan}",
                                            f"Wifi active {self.wlan.active()}",
                                            f"({count+1}/{self.MAX_RETRIES})")
            if watchdog is not None:
                watchdog.feed()
            self.buzzer.play_pip()
            time.sleep(1)
            count = count + 1
        if self.wlan.isconnected() == False:
            raise RuntimeError("Wifi timed out")
        self.logger.info(f"Connected to WiFi {self.wlan.ifconfig()}")

        sleep_ms(200)
        self.get_mac()
        self.logger.debug(f"{self.wlan}")
        self.buzzer.play_success_melody()

    def disconnect(self):
        self.wlan.disconnect()
        self.logger.info(f"Wifi disconnected {self.wlan.ifconfig()}")
        self.buzzer.play_fail_melody()

    def is_connected(self):
        return self.wlan.isconnected()

    def get_mac(self):
        if self.mac is None:
            self.mac = str(
                ubinascii.hexlify(self.wlan.config("mac"), ":").decode()
            )  # .replace(":", "")
            self.logger.info(f"MAC: {self.mac}")
            if "0000" in self.mac:
                raise RuntimeError(f"Invalid mac '{self.mac}'")
        return self.mac


if __name__ == "__main__":
    print("Wifi test . . .")
    b = Buzzer()
    d = Display()
    d.display_setup_state("Wifi test")

    with open("conf.local.json", "r") as f:
        json_str = " ".join(f.readlines())
    conf = json.loads(json_str)

    wifi = Wifi(conf["SSID"], conf["Password"], b)
    print("MAC", wifi.get_mac())
    wifi.connect(d)
    time.sleep(1)
    wifi.disconnect()
    print("Wifi test . . . Done")
