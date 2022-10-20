
import socket
from _thread import *

class Main():
    def __init__(self) -> None:
        self.arduino = {}
        self.clientes = []

    def mensagemClientes(self):
        pass
 
    def start(self):
        if(self.server()):
            self.loop()



    def server(self):
        try:
            self.serverP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serverP.bind((socket.gethostname(),2306))
            self.serverP.listen()
            return True

        except:
            print("Servidor não aberto")
            return False

    def loop(self):
        while True:
            client, addr = self.serverP.accept()
            mensagem_arduino = client.recv(32).decode("utf-8")
            
            if len(mensagem_arduino) == 0:
                client.close()

            elif str(mensagem_arduino) == "AD":
                self.arduino["AD"] = client
            
            elif str(mensagem_arduino) == "CL":
                self.clientes.append(client)
                start_new_thread(self.controleCLiente,(client,0))
            


            

    def controleCLiente(self,cliente,a):
        while True:
            msg = cliente.recv(32)
            if msg:
                try:
                    self.arduino["AD"].send(msg) #Envia mandamento pro arduino
                    while True:
                        msg_volta = self.arduino["AD"].recv(32)#espera uma mensagem  do arduino sendo boa ou ruim
                        if msg_volta:
                            cliente.send(msg_volta)
                            break
                except:
                    cliente.send("0".encode())
                    print("mandou pro cliente")


            

    




            


Main().start()