import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('roee'.encode(), ('localhost', 12345))
data, addr = s.recvfrom(1024)
print(data.decode())