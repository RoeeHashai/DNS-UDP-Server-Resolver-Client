import sys
import socket

PORT = sys.argv[1]
PATH = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(PORT)))

while True:
    data, addr = s.recvfrom(1024)
    data = data.decode().strip()
    best_match = None
    best_match_length = 0

    with open(PATH, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            domain = tokens[0]
            record_type = tokens[2]

            if domain == data and record_type != 'NS':
                best_match = line
                break

            elif record_type == 'NS' and data.endswith(domain):
                if len(domain) > best_match_length:
                    best_match = line
                    best_match_length = len(domain)

    if best_match:
        s.sendto(best_match.encode(), addr)
    else:
        s.sendto('non-existent domain'.encode(), addr)