#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class ServidorHTTPRequestHandler(BaseHTTPRequestHandler):

    #funcao que responde a requisicoes GET
    def do_GET(self):
        rootdir = os.path.dirname(os.path.abspath(__file__)) + '/html'
        try:
            self.f = open(rootdir + '/index.html') #abre o arquivo solicitado

            if self.path.endswith('.html'):
                self.f = open(rootdir + '/' + self.path) #abre o arquivo solicitado

            #responde com o codigo 200
            self.send_response(200)

            #envia headers da resposta
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            #envia conteudo ao cliente
            self.wfile.write(self.f.read().encode())
            self.f.close()
            return

        except IOError:
            self.send_error(404, 'file not found')

def run():
        print('Servidor HTTP sendo iniciado...')

        #ip e porta do servidor
        #por padrao, 80 eh a porta http

        server_address = ('127.0.0.2', 80)
        httpd = HTTPServer(server_address, ServidorHTTPRequestHandler)
        print('Servidor HTTP está funcionando...')
        httpd.serve_forever()

if __name__ == '__main__':
        run()
