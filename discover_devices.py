import asyncio
from bleak import BleakScanner


async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device.details)


asyncio.run(main())
