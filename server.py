import socket,threading


class Main():

    def Componetes(self):
        self.lista_clientes = {}


    def server(self):
        try:
            self.serverP = socket.socket()
            self.serverP.bind((socket.gethostname(),2306))
            self.serverP.listen()

        except:
            print("Servidor não aberto")

    def loop(self):
        while True:
 
            client, addr = self.serverP.accept()

            while True:
                mensagem_arduino = client.recv(32)
        
                if len(mensagem_arduino) == 0: break

                else:
                    print(mensagem_arduino)

            print("Conexão encerrada com o aruduíno!")
            client.close()


Main().start()