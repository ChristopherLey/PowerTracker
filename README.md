# PowerTracker Dev

Documentation for the Metawear SDK can be found [here](https://mbientlab.com/documents/metawear/cpp/latest/globals.html).

## Configuration
The device specific configuration can be found in the `config.h` file. This file contains the device MAC address and the device name.

## Monitoring
The bluetooth device can be monitored using the 
```bash
sudo btmon
```
command. This will display all bluetooth traffic on the device.

### Updating environment
To update the environment, run the following command:
```bash
conda env export | grep -v '^prefix: ' > environment.yml
```
