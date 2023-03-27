from machine import Pin, UART
import utime
LED = Pin(15,Pin.OUT)
uart1 = UART(1,115200,rxbuf=2048)
uart1.write("import sys\r\n")
uart1.write("sys.exit(0)\r\n")
uart1.write("import esp8266_tcp\r\n")
uart1.write("esp8266_tcp.connectobemfa()\r\n")
uart1.read()
while True:
    if uart1.any():   # 判断是否有数据可以接收
        buffer = uart1.read()       # 读取字符串数据
        try:
            data = buffer.decode('utf-8')
        # 以UTF-8编码格式对buffer字符串进行解码
            print(data)
            if data.find("on")>0:    # 若查找接收到的字符串为"开灯",则Pico板载LED点亮(未找到返回-1)
                LED.value(1)
            if data.find("off")>0:   # 若查找接收到的字符串为"关灯",则Pico板载LED熄灭(未找到返回-1)
                LED.value(0)
        except UnicodeError:
            pass
#uart1.write("sys.exit(0)\r\n")