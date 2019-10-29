import socket
import sys
import os
import time

host = '127.0.0.1'
port = 5000
endereco_local = (host, port)
mensagem = ''
prox_msg = '0'
receber = True

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

sock.bind(endereco_local)
if os.path.exists("recebido.jpg"):
    os.remove("recebido.jpg")

while (receber):
    msg, address = sock.recvfrom(4096)
    if msg == 'INICIO':
        resp = 'ACK INICIO'
        sock.sendto(resp.encode(), address)
        arquivo = open("recebido.jpg", "w+")
        continue
    else:
        if msg == 'FIM':
            print('Transferencia finalizada')
            receber = False
            arquivo.close()
        else:
            print(msg[0])
            if msg[0] == prox_msg:
                payload = bytearray(msg)
                arquivo.write(payload[4:])
            if msg[0] == '1':
                prox_msg = '0'
            else:
                prox_msg = '1'
            resp = 'ACK ' + prox_msg
            sock.sendto(resp.encode(), address)

sock.close()