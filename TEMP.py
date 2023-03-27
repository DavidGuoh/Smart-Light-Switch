import utime
from machine import Pin
import ds18x20
import onewire

sensor_temp = machine.ADC(2)
conversion_factor = 3.3/(65535)
reading = sensor_temp.read_u16()*conversion_factor
temperature = 27-(reading -0.706)/0.001721
    
temppin = Pin(2)
sensor = ds18x20.DS18X20(onewire.OneWire(temppin))
roms = sensor.scan()
while True:
    sensor.convert_temp()
    utime.sleep(1)
    for rom in roms:
        print(sensor.read_temp(rom))
