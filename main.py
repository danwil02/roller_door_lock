from mqtt import Mqtt
from servo import Servo
from buzzer import Buzzer
from log_manager import get_logger, get_stack_trace
from PiicoDev_TMP117 import PiicoDev_TMP117, sleep_ms
from led import flash_led
import json
from wifi import Wifi
from buzzer import Buzzer
from display import Display
from machine import WDT

watchdog = WDT()

logger = get_logger(__name__)


def run():
    tempsensor = PiicoDev_TMP117()
    buzzer = Buzzer()
    servo = Servo()
    disp = Display()
    tempC = 0

    flash_led()

    logger.info("Start Setup")

    with open("conf.local.json", "r") as f:
        json_str = " ".join(f.readlines())
    conf = json.loads(json_str)

    device_name = conf["Name"]
    wifi = Wifi(conf["SSID"], conf["Password"], buzzer)
    disp.display_setup_state("WIFI connecting")
    wifi.connect(display=disp, watchdog=watchdog)
    mqtt_client = Mqtt(
        conf["MQTT"]["Host"], wifi, conf["MQTT"]["User"], conf["MQTT"]["Password"]
    )

    disp.display_setup_state("MQTT connecting")
    mqtt_client.connect()
    watchdog.feed()
    mac = wifi.get_mac()
    garage_door_lock_name = mac + "_garage_door_lock"

    def sub_callback(topic, message):
        json_response = json.loads(message)
        logger.debug(f"Subscribe {topic}, {json_response}")
        if topic == b"homebridge/from/set":
            logger.debug("Handle homebridge/from/set")
            if json_response["name"] == garage_door_lock_name:
                logger.info(f"Set servo to {json_response['value']}")
                servo.set(json_response["value"])
                disp.update_display(tempC, servo.locked)
                buzzer.play_success_melody()

    flash_led(2)
    disp.display_setup_state("MQTT setup")

    mqtt_client.set_sub_callback(sub_callback)
    mqtt_client.sub("homebridge/from/response")
    mqtt_client.sub("homebridge/from/set")
    mqtt_client.pub("homebridge/to/get", json.dumps({"name": "*"}))
    mqtt_client.pub(
        "homebridge/to/add",
        json.dumps(
            {
                "name": mac + "_temperature",
                "service_name": "temperature",
                "service": "TemperatureSensor",
            }
        ),
    )
    mqtt_client.check_msg()
    mqtt_client.pub(
        "homebridge/to/add",
        json.dumps(
            {
                "name": garage_door_lock_name,
                "service_name": "switch",
                "service": "Switch",
            }
        ),
    )
    mqtt_client.check_msg()

    logger.info("Running")
    disp.display_setup_state("Running...")
    while True:
        flash_led(1)
        logger.debug("read temperature")
        tempC = tempsensor.readTempC()
        # sensors/<measurement>/<mac>/<device_name>
        topic = f"sensors/temperature/{mac}/{device_name}"
        msg = str(tempC)

        mqtt_client.pub(topic, msg)

        mqtt_client.pub(
            "homebridge/to/set",
            json.dumps(
                {
                    "name": mac + "_temperature",
                    "service_name": "temperature",
                    "characteristic": "CurrentTemperature",
                    "value": tempC,
                }
            ),
        )
        disp.update_display(tempC, servo.locked)

        # Wait 10 seconds before next temp reading
        for i in range(0, 1000):
            mqtt_client.check_msg()
            sleep_ms(10)
            watchdog.feed()


def disp_err(msg):
    try:
        disp = Display()
        disp.display.fill(0)
        disp.display.text("Error", 0, 0, 1)  # literal string
        disp.display.text(msg, 0, 15, 1)  # string variable
        disp.display.show()

        buzzer = Buzzer()
        buzzer.play_fail_melody()
    except Exception as e:
        logger.error(str(e))
        logger.error(get_stack_trace(e))


if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            logger.error(str(e))
            logger.error(get_stack_trace(e))
            disp_err(str(e))
            # panic(e)
        # finally:
        #     logger.info("Exiting program")
        logger.info("Sleeping")
        sleep_ms(500)
