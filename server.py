import socket


class Main():
    def server(self):
        try:
            self.serverP = socket.socket()
            self.serverP.bind((socket.gethostname(),2306))
            self.serverP.listen(0)

        except:
            print("Servidor não aberto")


        while True:
 
            client, addr = self.serverP.accept()

            while True:
                mensagem_arduino = client.recv(32)
        
                if len(mensagem_arduino) == 0: break

                else:
                    print(mensagem_arduino)

            print("Conexão encerrada com o aruduíno!")
            client.close()
