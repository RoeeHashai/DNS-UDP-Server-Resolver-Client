import sys
import socket
import datetime
from collections import deque

PORT = sys.argv[1]
DNS_SERVER_IP = sys.argv[2]
DNS_SERVER_PORT = int(sys.argv[3])
TTL = int(sys.argv[4])

queue = deque() # (domain, timeToExpire)
cache = {} # {domain: ("IP:PORT\IP\non-existent domain", A\NS\NE)}
time_delta = datetime.timedelta(seconds=int(TTL))

# Create a UDP socket and bind it to the specified port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(PORT)))

while True:
    print("[Cache] Before request: ", cache)
    print("[Queue] Before request: ", queue)
    # Receive the domain name from the client decode it and strip it
    data, addr = s.recvfrom(1024)
    data = data.decode().strip()
    print(f"[Request] Received {data} from {addr}")
    
    # clear old data from cache
    cur_time = datetime.datetime.now()
    while queue and queue[0][1] < cur_time:
        cache.pop(queue.popleft()[0], None)
        
    print("[Cache] After clearing: ", cache)
    print("[Queue] After clearing: ", queue)
    # check if data in cache and send it if able to send it without resolving
    if data in cache and cache[data][1] != 'NS':
        print(f"[Cache] Found {data} in cache, not resolving")
        domain, (ip, record_type) = data, cache[data]
        print(f"[Cache] Sending {ip} to {addr}")
        s.sendto(ip.encode(), addr)
        continue
    
    # data not in cache, needs to be resolved
    best_match = None
    for key, (ip, record_type) in cache.items():    # check if the domain is in cache
        if record_type == 'NS' and data.endswith(key) and (best_match is None or len(key) > len(best_match)):
            best_match = key
          
    ip, port = DNS_SERVER_IP, DNS_SERVER_PORT
    if best_match:                                  # if a suffix was found, use it to resolve
        ip, port = cache[best_match][0].split(':')
        port = int(port)
        print(f"[Cache] Found {best_match} in cache, resolving {data} with {best_match}")
    
    # send domain to DNS server and loop until resolved
    resolved = False
    while not resolved:
        print(f"[Resolving] Sending {data} to {ip}:{port}")
        s.sendto(data.encode(), (ip, port))
        response, _ = s.recvfrom(1024)
        if(response.decode().strip() == 'non-existent domain'):
            cache[data] = ('non-existent domain', 'NE')
            queue.append((data, datetime.datetime.now() + time_delta))
            print(f"[Resolving] Sending 'non-existent domain' to {addr}")
            s.sendto('non-existent domain'.encode(), addr)
            break
        domain, ip, record_type = response.decode().strip().split(',')
        # add to cache and queue the new data
        queue.append((domain, datetime.datetime.now() + time_delta))
        cache[domain] = (ip, record_type)
        if record_type == 'A':
            resolved = True
            print(f"[Resolving] Sending {ip} to {addr}")
            s.sendto(ip.encode(), addr)
        else:
            ip, port = ip.split(':')
            port = int(port)
