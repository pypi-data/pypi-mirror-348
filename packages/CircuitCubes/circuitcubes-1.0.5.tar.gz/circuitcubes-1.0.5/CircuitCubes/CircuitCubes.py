import asyncio, nest_asyncio
from bleak import BleakClient, BleakScanner
import sys

class Constants:
    def __init__(self): 
        self.BLUETOOTH_ADDRESS = '' # Address is unique to each Cube. All other values are the same for all Cubes.

        self.CIRCUITCUBE_SERV = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        self.TX_CHAR = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' # Write-without-response. 
        self.RX_CHAR = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' # Notify. 
        self.RX_CLIENT_CHAR_CONFIG_DESC = '00002902-0000-1000-8000-00805f9b34fb' # Handle 34. 

        self.GAP_SERV = '00001800-0000-1000-8000-00805f9b34fb'
        self.DEVICE_NAME_CHAR = '00002a00-0000-1000-8000-00805f9b34fb' # Read. 
        self.APPEARANCE_CHAR = '00002a01-0000-1000-8000-00805f9b34fb' # Read. 
        self.PERIPHERAL_PRIVACY_CHAR = '00002a02-0000-1000-8000-00805f9b34fb' # Read. 

        self.GATT_SERV = '00001801-0000-1000-8000-00805f9b34fb' 
        self.SERVICE_CHANGED_CHAR = '00002a05-0000-1000-8000-00805f9b34fb' # Indicate. 
        self.GATT_CLIENT_CHAR_CONFIG_DESC = '00002902-0000-1000-8000-00805f9b34fb' # Handle 11. 

        self.DEVICE_INFORMATION_SERV = '0000180a-0000-1000-8000-00805f9b34fb'
        self.SYSTEM_ID_CHAR = '00002a23-0000-1000-8000-00805f9b34fb' # Read. 
        self.MODEL_NUMBER_STR_CHAR = '00002a24-0000-1000-8000-00805f9b34fb' # Read. 
        self.SERIAL_NUMBER_STR_CHAR = '00002a25-0000-1000-8000-00805f9b34fb' # Read. 
        self.FIRMWARE_REV_STR_CHAR = '00002a26-0000-1000-8000-00805f9b34fb' # Read. 
        self.HARDWARE_REV_STR_CHAR = '00002a27-0000-1000-8000-00805f9b34fb' # Read. 
        self.SOFTWARE_REV_STR_CHAR = '00002a28-0000-1000-8000-00805f9b34fb' # Read. 
        self.MANUFACTURER_STR_CHAR = '00002a29-0000-1000-8000-00805f9b34fb' # Read. 
        self.IEEE_REGULATORY_LIST_CHAR = '00002a2a-0000-1000-8000-00805f9b34fb' # Read. 
        self.PLUGNPLAY_ID_CHAR = '00002a50-0000-1000-8000-00805f9b34fb' # Read. 

        self.UNKNOWN_SERV = 'f000ffc0-0451-4000-b000-000000000000'
        self.UNKNOWN_CHAR_1 = 'f000ffc1-0451-4000-b000-000000000000' # write-without-response, write, notify. 
        self.UNKNOWN_DESC_1 = '00002902-0000-1000-8000-00805f9b34fb' # Handle 4099.
        self.UNKNOWN_DESC_2 = '00002901-0000-1000-8000-00805f9b34fb' # Handle: 4100.
        self.UNKNOWN_CHAR_2 = 'f000ffc2-0451-4000-b000-000000000000' # write-without-response, write, notify. 
        self.UNKNOWN_DESC_3 = '00002902-0000-1000-8000-00805f9b34fb' # Handle 4103. 
        self.UNKNOWN_DESC_4 = '00002901-0000-1000-8000-00805f9b34fb' # Handle: 4104.

        self.constantsList = [self.BLUETOOTH_ADDRESS, # 0.
                         self.CIRCUITCUBE_SERV, self.TX_CHAR, self.RX_CHAR, self.RX_CLIENT_CHAR_CONFIG_DESC, # 1,2,3,4.
                         self.GAP_SERV, self.DEVICE_NAME_CHAR, self.APPEARANCE_CHAR, self.PERIPHERAL_PRIVACY_CHAR, # 5,6,7,8.
                         self.GATT_SERV, self.SERVICE_CHANGED_CHAR, self.GATT_CLIENT_CHAR_CONFIG_DESC, # 9,10,11.
                         self.DEVICE_INFORMATION_SERV, self.SYSTEM_ID_CHAR, self.MODEL_NUMBER_STR_CHAR, self.SERIAL_NUMBER_STR_CHAR, # 12,13,14,15.
                         self.FIRMWARE_REV_STR_CHAR, self.HARDWARE_REV_STR_CHAR, self.SOFTWARE_REV_STR_CHAR, # 16,17,18.
                         self.MANUFACTURER_STR_CHAR, self.IEEE_REGULATORY_LIST_CHAR, self.PLUGNPLAY_ID_CHAR, # 19,20,21.
                         self.UNKNOWN_SERV, self.UNKNOWN_CHAR_1, self.UNKNOWN_DESC_1, self.UNKNOWN_DESC_2, self.UNKNOWN_CHAR_2, self.UNKNOWN_DESC_3, self.UNKNOWN_DESC_4] # 22,23,24,25,26,27,28.

    def get_constant(self, index): # Index ranges from 0 to 28 since there are 29 items. 
        return self.constantsList[index] 
    
    def set_address(self, address): 
        self.BLUETOOTH_ADDRESS = address

    def __len__(self): 
        return len(self.constantsList)

class Cube:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.address = kwargs.get('address', '')
        self.jupyter = kwargs.get('jupyter', False)
        from IPython import get_ipython
        self.jupyter = not(get_ipython() is None)
        print(self.verbose * self.jupyter * '\nRunning in Jupyter notebook. ')
        self.constants_class = Constants()
        self.constants = self.constants_class.get_constant
        self.connect(self.address)
        self.constants_class.set_address(self.address)

    async def async_connect(self, address):
        try: 
            if address != '': 
                print(f'\nConnecting to Circuit Cube with address {address}. ')
                self.client = BleakClient(address)
            else: 
                print(self.verbose * '\nScanning for Circuit Cube. ')
                devices = await BleakScanner.discover()
                if len(devices) == 0: 
                    raise ConnectionError('\nNo BLE devices found. ')
                cubeDevice = [j for j in devices if 'Tenka' in str(j)]
                if not cubeDevice:
                    raise ConnectionError('\nNo Circuit Cube found. ')
                address = str(cubeDevice[0])[:17]
                print(self.verbose * f'\nConnecting to Circuit Cube with address {address}. ')
                self.client = BleakClient(address)
            self.address = address
            await self.client.connect()
        except Exception as e: 
            print(f'\n{e}')
            quit()

    def connect(self, address=''): 
        if self.jupyter: 
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.async_connect(address))
                return loop.run_until_complete(asyncio.gather(task)) 
        else: 
            asyncio.run(self.async_connect(address))

    async def async_device_information(self): # Read some device information from known GATT characteristics. 
        print('\nDevice information: ')
        try:
            device_name = await self.client.read_gatt_char(self.constants(6))
            device_name = device_name.decode('utf-8')
            print(f'    Name: {device_name}. ')

            device_appearance = await self.client.read_gatt_char(self.constants(7))
            device_appearance = int.from_bytes(device_appearance, 'big')
            print(f'    Appearance code: {device_appearance}. ')

            serial_number = await self.client.read_gatt_char(self.constants(15))
            serial_number = serial_number.decode('utf-8')
            print(f'    Serial number: {serial_number}. ')

            firmware = await self.client.read_gatt_char(self.constants(16))
            firmware = firmware.decode('utf-8')
            print(f'    Firmware: {firmware}. ')

            hardware = await self.client.read_gatt_char(self.constants(17))
            hardware = hardware.decode('utf-8')
            print(f'    Hardware: {hardware}. ')

            software = await self.client.read_gatt_char(self.constants(18))
            software = software.decode('utf-8')
            print(f'    Software: {software}. ')

            TX = self.constants(2) 
            RX = self.constants(3)
            await self.client.write_gatt_char(TX, bytes('b', 'utf-8'))
            voltage = await self.client.read_gatt_char(RX)
            print(f'    Battery voltage: {voltage.decode("utf-8")}. ')
        except Exception as e: 
            print(f'\n{e}')
            quit()
            import traceback
            traceback.print_exc()
    
    def device_information(self): 
        if self.jupyter: 
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.async_device_information())
                return loop.run_until_complete(asyncio.gather(task)) 
        else: 
            asyncio.run(self.async_device_information())

    def motor_command(self, letter, velocity): 
        if letter == 'A': 
            motor = 0 
        elif letter == 'B': 
            motor = 1
        elif letter == 'C': 
            motor = 2
        sign = '-' if velocity < 0 else '+'
        magnitude = abs(velocity*2)
        if magnitude > 200: 
            raise ValueError('\nVelocity must be between 0 and 100. ')
        if magnitude == 0: 
            magnitude = 0
        else: 
            magnitude = 55+abs(velocity) # Add to 55 since motor does nothing below 55. 
        command_string = f'{sign}{magnitude:03}{chr(ord('a') + motor)}'
        print(self.verbose * f'\nCommand string: {command_string}. ')
        return command_string
    
    async def async_run_motor(self, letter, velocity, time, **kwargs): 
        smooth = kwargs.get('smooth', False)
        TX = self.constants(2) 
        await self.client.write_gatt_char(TX, self.motor_command(letter, velocity).encode())
        await asyncio.sleep(time)
        if not smooth: 
            await self.client.write_gatt_char(TX, self.motor_command(letter, 0).encode())

    def run_motor(self, letter, velocity, time, **kwargs):
        if self.jupyter: 
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.async_run_motor(letter, velocity, time, **kwargs))
                return loop.run_until_complete(asyncio.gather(task))
        else: 
            asyncio.run(self.async_run_motor(letter, velocity, time, **kwargs))

    async def async_run_motors(self, letters, velocities, time, **kwargs): 
        smooth = kwargs.get('smooth', False)
        TX = self.constants(2)
        for letter, velocity in zip(letters, velocities): 
            command = self.motor_command(letter, velocity)
            await self.client.write_gatt_char(TX, command.encode())
        await asyncio.sleep(time)
        if not smooth: 
            for letter in letters: 
                command = self.motor_command(letter, 0)
                await self.client.write_gatt_char(TX, command.encode())

    def run_motors(self, letters, velocities, time, **kwargs):  
        if self.jupyter: 
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.async_run_motors(letters, velocities, time, **kwargs))
                return loop.run_until_complete(asyncio.gather(task))
        else: 
            asyncio.run(self.async_run_motors(letters, velocities, time, **kwargs))

    async def async_halt(self): 
        print('\nStopping all motors. ')
        TX = self.constants(2)
        for letter in ['A', 'B', 'C']: 
            command = self.motor_command(letter, 0)
            await self.client.write_gatt_char(TX, command.encode())

    def halt(self): 
        if self.jupyter: 
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.async_halt())
                return loop.run_until_complete(asyncio.gather(task))
        else: 
            asyncio.run(self.async_halt())

    def disconnect(self): 
        if self.jupyter: 
            print(self.verbose * '\nDisconnecting Circuit Cube. ')
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            if loop.is_running(): 
                task = asyncio.create_task(self.client.disconnect())
                return loop.run_until_complete(asyncio.gather(task))
        else: 
            print(self.verbose * '\nDisconnecting Circuit Cube. ')
            quit()

    def get_constants(self, index): 
        print(self.verbose * self.constants(index))
        return self.constants(index)
    
    def help(self):
        print('\n Visit https://github.com/simon-code-git/circuitcubes. ')
