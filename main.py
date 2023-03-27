import Stepper
from machine import Pin
import utime
from machine import Pin
import ds18x20
import onewire
from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
import framebuf
from time import sleep
from utime import sleep_ms
from machine import Pin, UART
import utime
status = 0
LED_R = Pin(6,Pin.OUT)
LED_G = Pin(7,Pin.OUT)
uart1 = UART(1,115200,rxbuf=2048)
#uart1.write("import sys\r\n")
#uart1.write("sys.exit(0)\r\n")
#uart1.write("import esp8266_tcp\r\n")
#uart1.write("esp8266_tcp.connectobemfa()\r\n")
uart1.read()
s1 = Stepper.create(Pin(0,Pin.OUT),Pin(1,Pin.OUT),Pin(2,Pin.OUT),Pin(3,Pin.OUT), delay=4)
spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16))
sensor_temp = machine.ADC(4)
conversion_factor = 3.3/(65535)
reading = sensor_temp.read_u16()*conversion_factor
temperature = 27-(reading -0.706)/0.001721
LED_R.value(1)
LED_G.value(0)
temppin = Pin(15)
sensor = ds18x20.DS18X20(onewire.OneWire(temppin))
roms = sensor.scan()
hour = 12
minute = 20
sec = 00
while True:
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
    if uart1.any():   # 判断是否有数据可以接收
        buffer = uart1.read()       # 读取字符串数据
        try:
            data = buffer.decode('utf-8')
        # 以UTF-8编码格式对buffer字符串进行解码
            print(data)
            if data.find("on")>0 and status == 0:
                LED_G.value(0)
                LED_R.value(0)# 若查找接收到的字符串为"开灯",则Pico板载LED点亮(未找到返回-1)
                s1.step(60,-1)
                s1.step(60,1)
                status = 1
                
            if data.find("off")>0 and status == 1:
                LED_G.value(0)
                LED_R.value(0)# 若查找接收到的字符串为"关灯",则Pico板载LED熄灭(未找到返回-1)
                s1.step(60,1)
                s1.step(60,-1)
                status = 0
            if data.find("res=1")>0:
                LED_G.value(1)
                LED_R.value(0)
            else:
                LED_G.value(0)
                LED_R.value(1)
        except UnicodeError:
            pass