import socket
import sys

host = "127.0.0.1"
port_receiver = 5000
dest = (host, port_receiver)
mensagem = 'Redes de Computadores'

header = '0'
index = 0

try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

while True:
    for letra in mensagem:
        msg = header + ', ' + letra
        sent = sock.sendto(msg.encode(), dest)
        header = '1'
        #resp = sock.recvfrom(4096)
        #print(resp)




