from machine import Pin, UART
import utime
uart1 = UART(1,baudrate=115200,rx=Pin(5),tx=Pin(4))   #ESP01S出厂时的波特率为115200(OR UART0:0,1,0)
LED = Pin(10, Pin.OUT)
LED.value(1)
utime.sleep(1)
LED.value(0)
# 定义树莓派Pico+ESP01S无线模块连接到WiFi函数
# 向树莓派Pico的ESP01S无线模块发送AT命令，连接到本地可用的WiFi
def ConnectToWiFi():
    uart1.write("AT+RST\r\n")         # 复位ESP01S无线模块
    utime.sleep(2)
 
    uart1.write("AT+CWMODE=1\r\n")    # 使用Station模式
    utime.sleep(3)
      
    uart1.write("AT+CIPMUX=0\r\n")    # 0:使用单连接模式
    utime.sleep(1)
    
    uart1.write('''AT+CWJAP="China_No.1","guo123456"\r\n''')
    # 连接网络热点，ssid：H3C_202, psw：abcde12345
    utime.sleep(10)    # 延时10s
    
    # uart1.write("AT+CWLAP")    # 不是必须
    # utime.sleep(1)
    uart1.write('''AT+CIPSTART="UDP","192.168.43.119",5000,5000,2\r\n''')
    # 192.168.124.2为本人智能手机使用的IP地址
    # 192.168.124.6为Pico+ESP01使用的IP地址
    utime.sleep(4)
ConnectToWiFi()
# 执行循环主程序
while True:
    if uart1.any():   # 判断是否有数据可以接收
        buffer = uart1.readline()       # 读取字符串数据
        data = buffer.decode('utf-8')   # 以UTF-8编码格式对buffer字符串进行解码
        print(data)
    if data.find("开灯")>0:    # 若查找接收到的字符串为"开灯",则Pico板载LED点亮(未找到返回-1)
        LED.value(1)
    if data.find("关灯")>0:   # 若查找接收到的字符串为"关灯",则Pico板载LED熄灭(未找到返回-1)
        LED.value(0)
