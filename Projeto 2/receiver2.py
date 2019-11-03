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
msg_completa = []
erros_indice = []
pacotes_recebidos = 0

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

            if msg[0] == prox_msg:#Checa se a mensagem foi recebida
                if pacotes_recebidos == 5:#Checa se ja foram enviados 5 pacotes
                #Recebe o pacote que tinha dado erro no primeiro envio e o coloca em sua posicao na lista
                    payload = bytearray(msg)
                    msg_completa.insert(erros_indice[0], payload[4:])
                    erros_indice.pop(0)
                    pacotes_recebidos = pacotes_recebidos - 1
                else:
                    payload = bytearray(msg)
                    msg_completa.append(payload[4:])
                if len(msg_completa) == 5:#Checa se todos os 5 pacotes ja foram recebidos com sucesso
                #Concatena todos os pacotes e os escreve no arquivo
                    payload = msg_completa[0] + msg_completa[1] + msg_completa[2] + msg_completa[3] + msg_completa[4]
                    msg_completa.clear()
                    pacotes_recebidos = 0
                    arquivo.write(payload)
                    pacotes_recebidos = -1
                if msg[0] == '1':
                    prox_msg = '0'
                else:
                    prox_msg = '1'

                resp = 'ACK ' + prox_msg
                if random.randint(0, 20) != 13:
                    sock.sendto(resp.encode(), address)

            else:#Caso o pacote nao tenha sido recebido salva se o indice onde ele deveria ter sido inserido para posterior insercao
                erros_indice.append(pacotes_recebidos)

            pacotes_recebidos = pacotes_recebidos + 1



sock.close()
