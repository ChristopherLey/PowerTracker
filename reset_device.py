from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp_int, create_voidp
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import yaml


# Load config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
metawear_address = config["devices"][0]["mac"]

# Connect to MetaWear
device = MetaWear(metawear_address)
device.connect()
print("Connected to " + device.address + " over " + ("USB" if device.usb.is_connected else "BLE"))
# Stops data logging
libmetawear.mbl_mw_logging_stop(device.board)
# Clear the logger of saved entries
libmetawear.mbl_mw_logging_clear_entries(device.board)
# Remove all macros on the flash memory
libmetawear.mbl_mw_macro_erase_all(device.board)
# Restarts the board after performing garbage collection
libmetawear.mbl_mw_debug_reset_after_gc(device.board)
print("Erase logger, state, and macros")
libmetawear.mbl_mw_debug_disconnect(device.board)
device.disconnect()
print("Disconnected")
