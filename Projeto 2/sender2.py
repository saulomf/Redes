import socket
import sys
import time
import random


host = "127.0.0.1"
port_receiver = 5000
dest = (host, port_receiver) # destinatario dos pacotes

inicio = 'INICIO'
fim = 'FIM'
ack_inicio = True
bit = '0'
index = 0
buffer_size = 2048
erros_indice = []
erros_imagem = []

# Criacao do socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

# Abrindo o arquivo de imagem
try:
    arquivo_imagem = open("unb.jpg", "r")
except:
    print("Erro na abertura do arquivo. Encerrando...")

# Iniciando a conexao, a imagem nao comeca a ser enviada ate a primeira
# mensagem ser respondida
while (ack_inicio):
    sock.sendto(inicio.encode(), dest)
    sock.settimeout(0.1)
    try:
        resp, address = sock.recvfrom(1024)
    except socket.timeout:
        print('Nenhum dado recebido. Reenviando...')
        time.sleep(1)
        continue
    if resp == 'ACK INICIO':
        break

# Inicio do envio da imagem
conteudo = arquivo_imagem.read(buffer_size)
while (conteudo):
    i = 0
    while i<5:
        # Header: bit de controle + delimitador
        header = bit + '$*$'
        if random.randint(0,20) != 7:
            sent = sock.sendto(header.encode() + conteudo, dest)

        # Define um timeout para o socket
        sock.settimeout(0.1)
        resp = ''


        # Espera a resposta do outro host. Se nada eh recebido, volta para o inicio
        # da iteracao e reenvia o pacote.
        try:
            resp, address = sock.recvfrom(1024)
        except socket.timeout:
            print('Nenhum dado recebido. Reenviando...')
            #time.sleep(1)
            continue

        print(resp)
        if resp != '':
            # Se o bit do ACK eh o mesmo que foi enviado, retorna para o inicio da
            # iteracao e reenvia o pacote. O bit esperado eh o bit seguinte.
            # Ex.: se enviou pacote com bit 0, aguarda ACK com bit 1.
            if resp[4] == bit:
                print('a')
                continue
            if bit == '1':
                bit = '0'
            else:
                bit = '1'
        else:#Empilha o indice e o conteudo dos pacotes que apresentaram erro
            print("chegou")
            erros_indice.append(header)
            erros_imagem.append(conteudo)

        # Le mais um pedaco da imagem
        conteudo = arquivo_imagem.read(buffer_size)
        #time.sleep(1)
        i = i+1


    while(erros_indice):#Reenvia os pacotes que apresentaram erro
        header2 = erros_indice[0]
        conteudo2 = erros_imagem[0]
        if random.randint(0,20) != 7:
            sent = sock.sendto(header2.encode() + conteudo2, dest)
        # Define um timeout para o socket
        sock.settimeout(0.1)
        resp = ''
        # Espera a resposta do outro host. Se nada eh recebido, volta para o inicio
        # da iteracao e reenvia o pacote.
        try:
            resp, address = sock.recvfrom(1024)
        except socket.timeout:
            print('Nenhum dado recebido. Reenviando...')
            time.sleep(1)
            continue

        print(resp)
        if resp == '':
            if resp[4] == bit:
                print('a')
                continue
                if bit == '1':
                    bit = '0'
                else:
                    bit = '1'
        else:#Remove da lista os pacotes que foram reenviados sem erros
            erros_indice.remove(header2)
            erros_imagem.remove(conteudo2)


# Envia a mensagem de finalizacao da transferencia
sent = sock.sendto(fim.encode(), dest)
sock.close()
