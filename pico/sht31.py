from machine import Pin, I2C
import time


def read_sht31(i2c: I2C):
    
    # SHT3x-DIS address
    sht31_address = 0x44

    # Measurement command
    measurement_command = b'\x2c\x06'

    # Write the command to the sensor
    i2c.writeto(sht31_address, measurement_command)

    # Wait for the measurement to complete
    time.sleep(0.005)  # Wait for 5 ms

    # Read the temperature data
    # data = i2c.readfrom_mem(sht31_address, 0x00, 6)  # Read 2 bytes of temperature data

    # Read the humidity data
    
    # Read the data back from the SHT31
    raw_data = i2c.readfrom_mem(sht31_address, 0x00, 6)
    
    # Convert each byte to a binary string and print
    for byte in raw_data:
        binary_string = bin(byte)
        print(f'{binary_string} == {byte}')

    i2c.writeto(sht31_address, b'\x30\xA2')
    
    humidity = ((raw_data[1] << 8) | raw_data[2]) / 1024 * 100
    temp = ((raw_data[3] << 8) | raw_data[4]) / 512 * 175 - 45
    
    print(f'hum: {humidity}, temp: {temp}')
    # Print the raw data
    # print(f"Temperature data: {temperature_data}")
    # print(f"Humidity data: {humidity_data}")

    # Note: This example assumes the sensor is connected to the default address (0x44) and that the ADDR pin is connected to VSS.




# devices = i2c.scan()
# if len(devices) > 0:
#     print('Number of I2C devices found=',len(devices))
#     for device in devices:
#         print("Device Hexadecimal Address= ",hex(device))

# read_sht31(i2c)



import machine
import time

class SHT3x:
    def __init__(self, i2c:I2C, address=0x44):
        self.address = address
        self.i2c = i2c
        self._error = None
        self._last_update_millisec = 0
        self._update_interval_millisec = 5000  # Default update interval in milliseconds
        self._timeout_millisec = 2000  # Default timeout in milliseconds
        self._operation_enabled = False

    def begin(self):
        # self.i2c.init()
        pass

    def update_data(self):
        if self._last_update_millisec == 0 or (time.ticks_ms() - self._last_update_millisec >= self._update_interval_millisec):
            self.send_command(0x2C, 0x06)
            if self._error == None:
                try:
                    data = self.i2c.readfrom_mem(self.address, 0x00, 6)
                    if len(data) == 6:
                        raw_temperature = (data[0] << 8) | data[1]
                        raw_humidity = (data[3] << 8) | data[4]
                        temperature_celsius = ((raw_temperature * 0.00267033) - 45.) * 1.0
                        rel_humidity = (raw_humidity * 0.0015259) * 1.0
                        self.temperature_celsius = temperature_celsius
                        self.rel_humidity = rel_humidity
                        self._error = None
                    else:
                        self._error = "Data corrupted"
                except Exception as e:
                    print('Err ' + str(e))
                    self._error = str(e)
            else:
                print('Error')

    def get_temperature(self, degree='C'):
        temperature = self.temperature_celsius
        if degree == "F":
            temperature = (temperature * 1.8) + 32
        elif degree == "K":
            temperature += 273.15
        return round(temperature, 2)

    def get_rel_humidity(self):
        return round(self.rel_humidity, 2)

    def set_mode(self, mode):
        pass  # Implement based on the modes supported by your SHT3x device

    def set_address(self, address):
        self.address = address

    def set_update_interval(self, update_interval_millisec):
        self._update_interval_millisec = update_interval_millisec

    def set_timeout(self, timeout_millisec):
        self._timeout_millisec = timeout_millisec

    def soft_reset(self):
        self.send_command(0x30, 0xA2)

    def hard_reset(self):
        pass  # Implement based on your hardware setup

    def heater_on(self):
        self.send_command(0x30, 0x6D)

    def heater_off(self):
        self.send_command(0x30, 0x66)

    def send_command(self, msb, lsb):
        # print(f'sending data to {hex(self.address)}')
        time.sleep(0.5)
        self.i2c.writeto(self.address, bytearray([msb, lsb]))
        time.sleep(0.5)
        # print('data sent')

    def crc8(self, msb, lsb, crc):
        # Implement CRC calculation
        pass

    def get_error(self):
        return self._error

    def return_value_if_error(self, value):
        if self._error == None:
            return value
        else:
            return 0.0

    def to_return_if_error(self, value):
        self._value_if_error = value




if __name__ == '__main__':
    
    
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)  # Adjust pins as necessary

    id = i2c.scan()[0]
    print(hex(id))

    if id != 0x44: raise ConnectionError('Wrong sensor ID!')

    sensorek = SHT3x(i2c)

    while True:
        sensorek.update_data()
        temp = (sensorek.get_temperature("Nic"))
        hum = (sensorek.get_rel_humidity())
        
        print(f'Temp: {temp:.2f}\thumid: {hum:.2f}')
        # time.sleep(1)
    # print(sensorek.press)