import math
import socket
import time
import struct

# Задаем адрес сервера
SERVER_ADDRESS = ('192.168.1.208', 5555)

# Настраиваем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print('server is running, please, press ctrl+c to stop')

# Слушаем запросы
connection, address = server_socket.accept()
print("new connection from {address}".format(address=address))
count = 0;
while count <= 100:
    count = count + 1
    data1 = int(100 * math.sin(2*math.pi*count / 100))
    data2 = int(80  * math.sin(60*2*math.pi/360  + 2*math.pi*count / 100))
    data3 = int(60  * math.sin(130*2*math.pi/360 + 2*math.pi*count / 100))
    data4 = int(40  * math.sin(270*2*math.pi/360 + 2*math.pi*count / 100))
    connection.sendall(data1.to_bytes(2, byteorder='big', signed=True))
    connection.sendall(data2.to_bytes(2, byteorder='big', signed=True))
    connection.sendall(data3.to_bytes(2, byteorder='big', signed=True))
    connection.sendall(data4.to_bytes(2, byteorder='big', signed=True))
    print(count)
    time.sleep(1)
connection.close()
server_socket.close()
print("All data sendet!")