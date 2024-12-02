import sys
import socket

# Retrieve the port number and path from command line arguments
PORT = sys.argv[1]
PATH = sys.argv[2]

# Create a UDP socket and bind it to the specified port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(PORT)))

while True:
    # Receive the domain name from the client decode it and strip it
    data, addr = s.recvfrom(1024)
    data = data.decode().strip()
    best_match = None
    best_match_length = 0

    # Open the file and read each line to find the best match
    with open(PATH, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            tokens = line.split(',')
            domain = tokens[0]
            record_type = tokens[2]

            # check if the record type is A and the domain is the same as the data
            if domain == data:
                best_match = line
                break
            
            # if the record is a suffix of the domain length keep the longest match
            elif record_type == 'NS' and data.endswith(domain):
                if len(domain) > best_match_length:
                    best_match = line
                    best_match_length = len(domain)

    if best_match:      # if the requested name or the best NS match was found send it
        s.sendto(best_match.encode(), addr)
    else:               # if the requested name was not found send 'non-existent domain'
        s.sendto('non-existent domain'.encode(), addr)