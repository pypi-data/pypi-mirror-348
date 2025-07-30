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