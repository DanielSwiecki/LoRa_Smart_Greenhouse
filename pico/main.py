import utime
import machine
from sht31 import SHT3x
from sgp30 import SGP30
import time
import LoRaWANHandler
from LoRaConfig import LoRaConfig
import json
import ubinascii


pay = True
delay_sec = 20


sht_i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14), freq=100000)  # Adjust pins as necessary
sgp_uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17))
sgp_reset_pin = machine.Pin(18, mode=machine.Pin.OUT)

soil_enable_pin = machine.Pin(19, mode=machine.Pin.OUT)
soil_enable_pin.value(1)
soil_meas_pin = machine.ADC(28)
light_pin = machine.ADC(27)

led = machine.Pin(25, machine.Pin.OUT)  # Assuming the built-in LED is on GPIO25



LoRaWANHandler.getBoardID()
lh = LoRaWANHandler.LoRaWANHandler(LoRaConfig)
sht = SHT3x(sht_i2c)
sgp = SGP30(sgp_uart, sgp_reset_pin)


def get_soil():
    global soil_enable_pin, soil_meas_pin
    soil_enable_pin.value(0)
   # Dry_value=54693
   # Wet_Value=54629
    time.sleep(2)
    soil_val = soil_meas_pin.read_u16()
    soil_val = (soil_val + soil_meas_pin.read_u16()) / 2
    soil_enable_pin.value(1)
    return soil_val


def get_light():
    light_val = light_pin.read_u16()
    return light_val


def init_lora():
    global lh
    lh.otaa()


def init():
    if pay: init_lora()
    

def get_data():
    global sht
    
    data = {}
    sht.update_data()
    temperature = sht.get_temperature()
    humidity = sht.get_rel_humidity()
    soil = get_soil()
    light = get_light()
    # tvoc, eco2 = sgp.read(temperature=temperature, humidity=humidity)
    
    # temperature = 25
    # humidity = 45
    # soil = 123
    # light = 123
    tvoc = 123
    eco2 = 123


    
    data['temperature'] = temperature
    data['humidity'] = humidity
    data['voc'] = tvoc
    data['co2'] = eco2
    data['soil'] = soil
    data['light'] = light
    
    data_serialized = ''
    
    serialize_value = lambda value : "{:04X}".format(int(value))
    # serialize_value = lambda value : ubinascii.b2a_base64(int.to_bytes(int(value), 3, 'big')).rstrip(b'\n').decode('utf-8')

    
    data_serialized += serialize_value(temperature * 100) + serialize_value(humidity * 100)
    data_serialized += serialize_value(tvoc) + serialize_value(eco2)
    data_serialized += serialize_value(soil) + serialize_value(light)


    return (data, data_serialized)
    


def send_data(msg):
    global lh
    if pay: lh.send(msg, False)




init()

start_time = utime.ticks_ms()

while(True):
    start_time = utime.ticks_ms()
    led.on()
    time.sleep(0.5)
    try:
        
        data, data_serialized = get_data()
        print(data)
        send_data(data_serialized)
        
    except Exception:
        print('Some exception :{e}(')
        pass
    # data = {'temperature': 25, 'humidity': 45, 'voc': 123, 'co2': 123, 'soil': 123, 'light': 12}
    
    led.off()
    
    # data_list = []
    # for key in data.keys():
    #     data_list.append(str(data[key]))
    
    
    # data_str = json.dumps(data)
    # print(data_str)

    # time.sleep(300)
    # machine.deepsleep(300000)
    
    elapsed_time = utime.ticks_diff(utime.ticks_ms(), start_time)
    print(f'cycle time = {elapsed_time} ms')
    time.sleep(1)

    
   




