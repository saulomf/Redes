import socket
import sys
import time
import random

host = "127.0.0.1"
port_receiver = 5000
dest = (host, port_receiver)
mensagem = 'Redes de Computadores'
inicio = 'INICIO'
fim = 'FIM'
ack_inicio = True

bit = '0'
index = 0
buffer_size = 2048

try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

try:
    arquivo_imagem = open("unb.jpg", "r")
except:
    print("Erro na abertura do arquivo. Encerrando...")

conteudo = arquivo_imagem.read(buffer_size)
while (ack_inicio):
    sock.sendto(inicio.encode(), dest)
    sock.settimeout(5)
    try: 
        resp, address = sock.recvfrom(1024)
    except socket.timeout:
        print('Nenhum dado recebido. Reenviando...')
        time.sleep(1)
        continue
    if resp == 'ACK INICIO':
        break

while (conteudo):
    header = bit + '$*$'
    sent = sock.sendto(header.encode() + conteudo, dest)
    tempo = time.time()
    sock.settimeout(5)
    resp = ''

    try: 
        resp, address = sock.recvfrom(1024)
    except socket.timeout:
        print('Nenhum dado recebido. Reenviando...')
        #time.sleep(1)
        continue

    print(resp)
    if resp <> '':
        if resp[4] == bit:
            continue
        if bit == '1':
            bit = '0'
        else:
            bit = '1'
    conteudo = arquivo_imagem.read(buffer_size)
    #time.sleep(1)

sent = sock.sendto(fim.encode(), dest)
sock.close()

        




