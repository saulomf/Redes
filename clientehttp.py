import http.client
import sys

http_server = '127.0.0.2'

conn = http.client.HTTPConnection(http_server)

while 1:
    cmd = input('digite um comando HTTP (ex. GET index.html): ')
    cmd = cmd.split()

    if cmd[0] == 'exit': 
        break

    if len(cmd) == 1:
        cmd.append('')

    conn.request(cmd[0], cmd[1])

    rsp = conn.getresponse()

    print(rsp.status, rsp.reason)
    dados_recebidos = rsp.read()
    print(dados_recebidos)