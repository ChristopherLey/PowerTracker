from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp_int, create_voidp
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import yaml
import json
import copy
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path


class State:
    # init
    def __init__(self, device, dir_path: str = "./"):
        self.device = device
        self.acceleration_x = []
        self.acceleration_y = []
        self.acceleration_z = []
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.file_name = f"{datetime.now().strftime('%d-%m_%H-%M-%S')}_accel.csv"
        self.file_path = Path(dir_path) / self.file_name
    # callback

    def data_handler(self, ctx, data):
        values = copy.deepcopy(parse_value(data, n_elem=1))
        csv_to_write = f'{datetime.utcnow().strftime("%F %T.%f")[:-3]},{values.x},{values.y},{values.z}\n'
        with open(self.file_path, 'a') as f:
            f.write(csv_to_write)


# connect
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
metawear_address = config["devices"][1]["mac"]
try:
    d = MetaWear(metawear_address)
    d.connect()
    print("Connected to " + d.address + " over " + ("USB" if d.usb.is_connected else "BLE"))
    print(d.is_connected)
    if not d.is_connected:
        raise Exception("Not connected")
except Exception as e:
    print(e)
    exit(1)
s = State(d)

# configure
print("Configuring device")
# setup ble
libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)
# setup acc
libmetawear.mbl_mw_acc_set_odr(s.device.board, 100.0)
libmetawear.mbl_mw_acc_set_range(s.device.board, 16.0)
libmetawear.mbl_mw_acc_write_acceleration_config(s.device.board)
# get acc and subscribe
signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
libmetawear.mbl_mw_datasignal_subscribe(signal, None, s.callback)
# start acc
libmetawear.mbl_mw_acc_enable_acceleration_sampling(s.device.board)
libmetawear.mbl_mw_acc_start(s.device.board)

# sleep
sleep(20.0)

# tear down
libmetawear.mbl_mw_acc_stop(s.device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(s.device.board)
# unsubscribe
signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(signal)
# disconnect
libmetawear.mbl_mw_debug_disconnect(s.device.board)
s.device.disconnect()

# file_name =
#
#
# # recap
# plt.figure()
# plt.plot(s.acceleration_x, label="x")
# plt.plot(s.acceleration_y, label="y")
# plt.plot(s.acceleration_z, label="z")
# plt.legend()
# plt.show()




