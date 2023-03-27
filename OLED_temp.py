import utime
from machine import Pin
import ds18x20
import onewire
from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
import framebuf
from time import sleep
from utime import sleep_ms

spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16))
sensor_temp = machine.ADC(2)
conversion_factor = 3.3/(65535)
reading = sensor_temp.read_u16()*conversion_factor
temperature = 27-(reading -0.706)/0.001721
    
temppin = Pin(2)
sensor = ds18x20.DS18X20(onewire.OneWire(temppin))
roms = sensor.scan()
hour = 23
minute = 51
sec = 40
while True:
    try:
        sensor.convert_temp()
        utime.sleep(1)
        sec +=1
        if (sec == 60):
            sec = 0
            minute +=1
        if (minute == 60):
            minute = 0
            hour +=1
        if(hour == 24):
            hour = 0
        minutet = str(minute)
        sect = str(sec)
        hourt = str(hour)
        if (minute<10):
            minutet = "0"+str(minutet)
        if (hour<10):
            hourt = "0"+str(hourt)
        if (sec<10):
            sect = "0"+str(sect)
            
            
#        for i in range(40):
#            for j in range(56):
                
        oled.fill(0)
        oled.show()
        oled.text("Time",45,0)
        oled.show()
        oled.text(hourt+":"+minutet+":"+sect,30,15)
        oled.show()
        
        #sleep(1)
        oled.text("Room Temperature",0,30)
        oled.show()
        for rom in roms:
            true_temp = int(sensor.read_temp(rom)*10)/10
            oled.text(str(true_temp),45,50)
            oled.show()
        #sleep_ms(10)
    except KeyboardInterrupt:
        oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16))
        break
