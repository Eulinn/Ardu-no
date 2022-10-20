import socket,threading


class Main():

    def start(self):
        if(self.server()):
            self.loop()

    def Componetes(self):
        self.lista_clientes = {}


    def server(self):
        try:
            self.serverP = socket.socket()
            self.serverP.bind((socket.gethostname(),2306))
            self.serverP.listen()
            return True

        except:
            print("Servidor não aberto")
            return False

    def loop(self):
        while True:
 
            client, addr = self.serverP.accept()

            while True:
                mensagem_arduino = client.recv(32)
        
                if len(mensagem_arduino) == 0: break

                elif str(mensagem_arduino).decode("utf-8") == "ad":
                    self.lista_clientes['AD'] = client
                
                else:
                    self.lista_clientes["CL"] = client
                    

            print("Conexão encerrada com o aruduíno!")
            client.close()


Main().start()