import socket
import sys
import time
import random
import select


host = "127.0.0.1"
port_receiver = 5000
dest = (host, port_receiver) # destinatario dos pacotes

inicio = 'INICIO'
fim = 'FIM'
ack_inicio = True
enviando = False
tamanho_janela = 5
primeiro_ack = 0
timeout = 1
index = 0
buffer_size = 50
erros_indice = []
erros_imagem = []
frame_buffer = []
acked = []
timeouts = []

# Criacao do socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
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
    sock.settimeout(1)
    try:
        resp, address = sock.recvfrom(1024)
    except socket.timeout:
        print('Nenhum dado recebido. Reenviando...')
        time.sleep(1)
        continue
    if resp == 'ACK INICIO':
        enviando = True
        break

# Inicio do envio da imagem
# Cria os 10 primeiros frames que serao enviados
# Ao longo da execucao, conforme o ACK de um frame for recebido
# ele sera substituido por outro frame, mais atual.
for i in range(10):
    conteudo = arquivo_imagem.read(buffer_size)
    header = str(i) + '$*$'
    frame = header.encode() + conteudo
    frame_buffer.append(frame)

i = 0
f = 0
while (enviando):
    # Fazer um loop pra verificacao de timeouts
    #for t in range(len(timeouts)):
    #   if timeouts[t] < time.time():

    # Envia frames enquanto houver espaco na janela. Como usamos apenas um digito para 
    # identificar os frames (0-9), a janela pode ter um maximo de 5 frames. Do contrario,
    # se a janela for maior.. ???
    if (i < tamanho_janela):
        if f == 10:
            f = 0

        #if random.randint(0,20) != 7:
        sent = sock.sendto(frame_buffer[f], dest)
        print('SENT ' + str(f))

        timeouts.insert(f, time.time() + 1)
        i += 1
        f += 1 

    # Se nao houver mais espaco na janela, realiza leitura   
    else:
        print('leitura')
        #rd, wr, ed = select.select([sock], [] , [] , timeout)
        #if not rd:
        #    print("timeout; reenviando")
        #else:
        try:
            resp, address = sock.recvfrom(1024)
        except socket.timeout:
            print('Nenhum dado recebido. Reenviando...')
            time.sleep(1)
            continue

        print(resp)
        acked.append(int(resp[4]))
        # percorre os acks recebidos
        for ack in acked:
            print('ACK ' + str(ack) + '; WF: ' + str(primeiro_ack))
            # confere se o ack eh o primeiro da janela
            if ack == primeiro_ack:
                print('entrou')
                conteudo = arquivo_imagem.read(buffer_size)
                if conteudo == '':
                    #interrompe o loop se nao houver mais conteudo 
                    enviando = False
                    break
                header = str(ack) + '$*$'
                frame = header.encode() + conteudo
                frame_buffer[ack] = frame
                primeiro_ack += 1
                if (primeiro_ack == 10):
                    primeiro_ack = 0
                i -= 1
                acked.remove(ack)



    
    
# Envia a mensagem de finalizacao da transferencia
sent = sock.sendto(fim.encode(), dest)
sock.close()
