simport socket
import sys
import os
import time
import random

host = '127.0.0.1'
port = 5000
endereco_local = (host, port)
mensagem = ''
prox_msg = '0'
tamanho_janela = 5
receber = True
msg_completa = []
erros_indice = []
pacotes_recebidos = 0
index_esperado = 0

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
            #print(msg[0])
            print(msg)
            print(pacotes_recebidos)
            print(len(msg_completa))
            index_msg = msg[0]

            # O algoritmo tem que ignorar pacote fora da janela, ou seja:
            # - que ja tenha sido escrito no arquivo ou
            # - que estejam muito alem do esperado (5 unidades alem do esperado) 

            # Se a mensagem que chega eh a esperada, escreve o payload no arquivo
            if (index_esperado == index_msg):
                payload = bytearray(msg)
                arquivo.write(payload[4:])
                index_esperado += 1
                if (index_esperado == 10):
                    index_esperado = 0
            else:
                # Coloca a mensagem num buffer. Quando a mensagem certa chegar, organizar o buffer e
                escrever no arquivo
            
            # Envia o ACK da mensagem, a nao ser que o frame que chega esteja fora da janela
            resp = 'ACK ' + index_msg
            sock.sendto(resp.encode(), address)
            if random.randint(0, 20) != 13:
                sock.sendto(resp.encode(), address)
            time.sleep(1)


            pacotes_recebidos = pacotes_recebidos + 1



sock.close()
