import sys
import socket
import datetime
from collections import deque

PORT = sys.argv[1]
DNS_SERVER_IP = sys.argv[2]
DNS_SERVER_PORT = int(sys.argv[3])
TTL = int(sys.argv[4])

queue = deque() # (domain, timeToExpire)
cache = {} # {domain: ("IP:PORT", A\NS)}
time_delta = datetime.timedelta(seconds=int(TTL))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(PORT)))

while True:
    data, addr = s.recvfrom(1024)
    data = data.decode().strip()
    
    # clear old data from cache
    cur_time = datetime.datetime.now()
    while queue and queue[-1][1] < cur_time:
        del cache[queue.popleft()[0]]
        
    # check if data in cache and send it if able to reslove
    if data in cache:
        domain, (ip, record_type) = data, cache[data]
        s.sendto(f"{domain},{ip},{record_type}".encode(), addr)
        continue
    
    # data not in cache, needs to be resolved
    # check if a suffix of the domain is in cache
    best_match = None
    for key in cache.keys():
        if data.endswith(key) and (best_match is None or len(key) > len(best_match)):
            best_match = key
            
    ip, port = DNS_SERVER_IP, DNS_SERVER_PORT
    if best_match:
        ip, port = cache[best_match][0].split(':')
        port = int(port)
    
    # send domain to DNS server and loop until resolved
    resolved = False
    while not resolved:
        s.sendto(data.encode(), (ip, port))
        response, _ = s.recvfrom(1024)
        if(response.decode().strip() == 'non-existent domain'):
            s.sendto('non-existent domain'.encode(), addr)
            break
        domain, ip, record_type = response.decode().strip().split(',')
        queue.appendleft((domain, datetime.datetime.now() + time_delta))
        cache[domain] = (ip, record_type)
        if record_type != 'NS':
            resolved = True
            s.sendto(response, addr)
        else:
            ip, port = ip.split(':')
            port = int(port)