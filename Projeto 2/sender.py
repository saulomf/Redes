import socket
import sys
import time

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
    msg = header + ', ' + mensagem
    sent = sock.sendto(msg.encode(), dest)
    tempo = time.time()
    sock.settimeout(5)
    resp = ''
    try: 
        resp = sock.recvfrom(4096)
    except socket.timeout:
        print('Nenhum dado recebido. Reenviando...')
        time.sleep(1)
        continue
    print(resp)
    if resp <> '':
        if header == '1':
            header = '0'
        else:
            header = '1'
    time.sleep(1)
        




