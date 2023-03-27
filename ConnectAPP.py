import time
from machine import Timer
import socket

#需要修改的地方
wifiName = "newhtc"                   #wifi 名称，不支持5G wifi
wifiPassword = "qq123456"       #wifi 密码
clientID = "7d54f85af42976ee3c2693e692a6bb59"            # Client ID ，密钥，巴法云控制台获取
myTopic='myled002'                     # 需要订阅的主题值，巴法MQTT控制台创建

#默认设置
serverIP = 'bemfa.com'    # mqtt 服务器地址
port = 8344

# WIFI 连接函数
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifiName, wifiPassword)
        while not sta_if.isconnected():
            pass
    print('connect  WiFi ok')


    
# tcp 客户端初始化        
def connect_and_subscribe():
  addr_info = socket.getaddrinfo(serverIP, port)
  addr = addr_info[0][-1]
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 创建TCP的套接字,也可以不给定参数。默认为TCP通讯方式
  client.connect(addr)                                 # 设置要连接的服务器端的IP和端口,并连接
  substr = 'cmd=1&uid='+clientID+'&topic='+myTopic+'\r\n'
  client.send(substr.encode("utf-8"))
  print("Connected to %s" % serverIP)
  return client
  
#心跳
def Ping(self):
    # 发送心跳
    try:
        keeplive = 'ping\r\n'
        client.send(keeplive.encode("utf-8"))
    except:
        restart_and_reconnect()

# 重新连接
def restart_and_reconnect():
  print('Failed to connect to TCP  broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
 
 #开始连接WIFI
do_connect() 

#开始连接TCP
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
 
 #开启定时器，定时发送心跳
tim = Timer(-1)
tim.init(period=30000, mode=Timer.PERIODIC, callback=Ping)

while True:
  try:
    data = client.recv(256)    if(len(data) != 0):字节时,关闭套接字
        data=data.decode('utf-8')              
        print(data.strip())
  except OSError as e:
    print('Failed to connect to  broker. Reconnecting...')
    restart_and_reconnect()
