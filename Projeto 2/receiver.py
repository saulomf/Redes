import socket
import sys

host = '127.0.0.1'
port = 5000
port_sender = 5001
local_address = (host, port)
mensagem = ''

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

sock.bind(local_address)

while True:
    msg = sock.recvfrom(4096)
    print(msg)
