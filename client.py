import sys
import socket

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = input()
    s.sendto(data.encode(), (SERVER_IP, SERVER_PORT))
    response, _ = s.recvfrom(1024)
    res = response.decode().strip().split(',')
    print(res[0])