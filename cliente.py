 # Redes de Computadores - 2019/2
 # Prof. Priscila Solis Mendez
 # Projeto 1 - Cliente HTTP
 # Integrantes:
 # Daniel Oliveira ()
 # Joao Antonio Moraes (16/0126975)
 # Saulo Feitosa ()

import socket
import webbrowser
import sys
import os

host = '127.0.0.1' #endereco do host local
port = 80  # web

# Criacao do socket
print('# Criando socket')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Falha ao criar socket')
    sys.exit()

print('# Obtendo IP remoto') 
try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    print('Nome do host nao foi resolvido. Encerrando')
    sys.exit()

# Conectar ao servidor
print('# Conectando ao servidor, ' + host + ' (' + remote_ip + ')')
s.connect((remote_ip , port))

# Envio de requisicao
print('# Enviando requisicao ao servidor')
request = b"GET /redes.html HTTP/1.0\r\n\r\n"

try:
    s.sendall(request)
except socket.error:
    print('Envio falhou. Encerrando')
    sys.exit()

# Recebendo dados
print('# Recebendo dados do servidor')
reply = s.recv(4096)

print (reply) 

# Salvando arquivo html
arquivo_html = open ("redes.html", "w")
arquivo_html.write(reply.decode('utf-8'))
arquivo_html.close()

# Abrindo html para renderizacao
url = 'file:///'+os.getcwd()+'/redes.html'
webbrowser.open(url, new = 2)