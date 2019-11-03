import socket
import sys
import os
import time
import random

host = '127.0.0.1'
port = 5000
endereco_local = (host, port)
mensagem = ''
prox_msg = '0'
receber = True

# Criacao do socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

# Binding do socket para que fique aberto e aguardando contato
sock.bind(endereco_local)

# Deleta o arquivo a ser recebido se ele ja existir
if os.path.exists("recebido.jpg"):
    os.remove("recebido.jpg")

# Loop de recebimento de dados
while (receber):
    msg, address = sock.recvfrom(4096)

    # Condicao para abertura do arquivo: recebimento da mensagem
    # de INICIO da transferencia
    if msg == 'INICIO':
        resp = 'ACK INICIO'
        sock.sendto(resp.encode(), address)
        arquivo = open("recebido.jpg", "w+")
        continue
    else:
        # Condicao para fechamento do arquivo: recebimento
        # da mensagem de FIM da transferencia
        if msg == 'FIM':
            print('Transferencia finalizada')
            receber = False
            arquivo.close()
        else:
            # Trecho que lida com o recebimento do arquivo em si
            print(msg[0])

            # Se o pacote eh o que esta sendo esperado: adiciona
            # os dados no arquivo (descarta o header) e atualiza
            # o bit do proximo pacote esperado. Do contrario, reenvia
            # o ACK.
            if msg[0] == prox_msg:
                payload = bytearray(msg)
                arquivo.write(payload[4:])
                if msg[0] == '1':
                    prox_msg = '0'
                else:
                    prox_msg = '1'
            resp = 'ACK ' + prox_msg
            if random.randint(0, 20) != 13:
                sock.sendto(resp.encode(), address)

sock.close()
