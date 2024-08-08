from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp_int, create_voidp
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import yaml


# Load config
with open("../config.yaml", "r") as file:
    config = yaml.safe_load(file)
metawear_address = config["devices"][0]["mac"]

# Connect to MetaWear
device = MetaWear(metawear_address)
device.connect()
print("Connected to " + device.address + " over " + ("USB" if device.usb.is_connected else "BLE"))
#
# create LED pattern
pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.BLINK)
libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)

# play the pattern
libmetawear.mbl_mw_led_play(device.board)

# wait 5s
sleep(5.0)

# remove the LED pattern and stop playing
libmetawear.mbl_mw_led_stop_and_clear(device.board)
sleep(2.0)

print("Done")
# disconnect
device.disconnect()
sleep(1.0)
