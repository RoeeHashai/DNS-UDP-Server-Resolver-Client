
# DNS-Like Server System

## Overview
This project simulates a DNS-like server system using Python. It consists of three main components: a Server, a Resolver, and a Client. The server handles DNS queries and responses, The resolver helps in determining the most efficient routing for queries based on available data, utilizing a caching mechanism to optimize query resolutions, while the client acts as the query initiator.

## Components

### Server
The server component is designed to handle incoming DNS queries. It reads from a predefined zone file and resolves DNS queries based on the records available in this file. If the server can resolve a query directly (A records), it responds immediately; otherwise, it delegates to the resolver for NS records.

- **Functionality**:
  - Listen on a specified UDP port.
  - Parse and respond to DNS queries based on a local zone file.
  - Handle A and NS record types.
  - Respond with "non-existent domain" if no relevant records are found.

### Resolver
The resolver caches DNS queries to reduce resolution time and network traffic. It checks its cache before querying the server and updates its cache with new queries' responses.

- **Functionality**:
  - Cache DNS query responses to optimize repeated queries.
  - Clear cache entries based on a specified TTL (Time To Live).
  - Split DNS information into IP address and record type for efficient caching.
  - Handle recursive DNS queries if the initial server does not resolve the query.

### Client
The client sends DNS query requests to the server and displays responses. It's designed to simulate DNS query traffic and can be used to test the responsiveness and accuracy of the server and resolver.

- **Functionality**:
  - Send DNS queries to a specified server IP and port.
  - Display the server's responses.

## How to Run

### Server
Run the server with the following command:
```bash
python3 server.py [PORT] [ZONE_FILE_PATH]
```
Example:
```bash
python3 server.py 12345 zone.txt
```

### Resolver
Run the resolver with the following command:
```bash
python3 resolver.py [PORT] [DNS_SERVER_IP] [DNS_SERVER_PORT] [TTL]
```
Example:
```bash
python3 resolver.py 11111 127.0.0.1 12345 60
```

### Client
Run the client with the following command:
```bash
python3 client.py [SERVER_IP] [SERVER_PORT]
```
Example:
```bash
python3 client.py 127.0.0.1 11111
```

## Zone File Format
The zone file should contain DNS records in the following format:
```
domain.com,IP_ADDRESS,RECORD_TYPE
```
Examples:
```
biu.ac.il,1.2.3.4,A
co.il,1.2.3.5:777,NS
example.com,1.2.3.7,A
```

## Additional Information
- Ensure Python 3.6+ is installed.
- No external libraries are required as the project uses standard Python libraries.
