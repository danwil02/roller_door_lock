from lib.umqtt.simple import MQTTClient
from wifi import Wifi
from buzzer import Buzzer
from log_manager import get_logger, get_stack_trace
import json


class Mqtt:
    def __init__(self, mqtt_host: str, wifi: Wifi, user=None, password=None):
        if wifi.is_connected() == False:
            wifi.connect()
        self.logger = get_logger(__name__)
        self.mqtt_host = mqtt_host
        self.user = user
        self.password = password
        self.client_id = wifi.get_mac()
        self.mqtt_client = MQTTClient(
            client_id=self.client_id,
            server=self.mqtt_host,
            keepalive=60,
            user=self.user,
            password=self.password,
        )

    def connect(self):
        self.logger.info(f"Connecting to MQTT Broker {self.mqtt_host}")
        self.mqtt_client.connect()

    def disconnect(self):
        try:
            self.mqtt_client.disconnect()
        except OSError as e:
            self.logger.warning(str(e))
            self.logger.warning(get_stack_trace(e))

    def pub(self, topic, message):
        self.logger.info(f"Publish: topic {topic}, message {message}")
        self.mqtt_client.publish(topic, message)

    def sub(self, topic):
        self.logger.info(f"Subscribed to topic: {topic}")
        self.mqtt_client.subscribe(topic)

    def set_sub_callback(self, f):
        self.mqtt_client.set_callback(f)

    def check_msg(self):
        self.mqtt_client.check_msg()

def mqtt_test():
    print("MQTT test . . . ")
    with open("conf.local.json", "r") as f:
        json_str = " ".join(f.readlines())
    conf = json.loads(json_str)

    wifi = Wifi(conf["SSID"], conf["Password"], Buzzer())
    mqtt = Mqtt("192.168.172.2", wifi)
    print(f"MQTT connect {mqtt.connect()}")
    mqtt.pub("test", "test message")
    print("MQTT test . . . Done")

if __name__ == '__main__':
    mqtt_test()
