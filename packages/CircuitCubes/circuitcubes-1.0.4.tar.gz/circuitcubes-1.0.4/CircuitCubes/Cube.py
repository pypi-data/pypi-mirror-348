from .Constants import Constants
import asyncio, nest_asyncio
from bleak import BleakClient, BleakScanner

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
