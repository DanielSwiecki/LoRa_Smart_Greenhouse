from machine import Pin, UART
import time
import math




class SGP30:
    
    def __init__(self, uart:UART, reset_pin:Pin):
        self.uart0 = uart
        self.reset_pin = reset_pin
        

    def get_absolute_humidity(self, temperature, humidity):
        absolute_humidity = 216.7 * ((humidity / 100.0) * 6.112 * math.exp((17.62 * temperature) / (243.12 + temperature)) / (273.15 + temperature))  # [g/m^3]
        absolute_humidity_scaled = int(1000.0 * absolute_humidity)  # [mg/m^3]
        return absolute_humidity_scaled
    

    def set_humidity(self, value:int):
        
        message = f'h{value}\n'
        message_bytes = message.encode('utf-8')
        
        self.uart0.write(message_bytes)
        time.sleep(0.2)

    def read_values(self, ):
        tvoc = -1
        eco2 = -1
        
        for _ in range(10):
            time.sleep(0.5)
            msg = self.uart0.readline()
            if msg is None or len(msg) < 3: continue
            msg = msg.decode().strip()
            if msg[0] == 't': tvoc=float(msg[1:])
            if msg[0] == 'e': eco2=float(msg[1:])
            if tvoc > -1 and eco2 > -1:
                break
        
        return (tvoc, eco2)


    def read(self, temperature, humidity):
        abs_humidity = self.get_absolute_humidity(temperature, humidity)
        self.reset_pin.off()
        time.sleep(0.5)
        self.reset_pin.on()
        time.sleep(0.5)
        self.set_humidity(abs_humidity)
        self.set_humidity(abs_humidity)
        self.set_humidity(abs_humidity)
        time.sleep(30)
        values = self.read_values()
        return values

