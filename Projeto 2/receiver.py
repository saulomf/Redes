import socket
import sys

host = '127.0.0.1'
port = 5000
endereco_local = (host, port)
mensagem = ''
prox_msg = '0'

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

sock.bind(endereco_local)

while True:
    msg, address = sock.recvfrom(4096)
    print(msg)
    if msg[0] == '1':
        prox_msg = '0'
    else:
        prox_msg = '1'
    resp = 'ACK ' + prox_msg
    sock.sendto(resp.encode(), address)
