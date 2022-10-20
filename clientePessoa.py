import socket
from _thread import *

class Main():
    def __init__(self) -> None:
        self.erros=['Arduino inexistente ou não conectado',
        "Enviado"]


    def start(self):
        if(self.server()):
            self.loop()

    def server(self):
        try:
            self.serverP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serverP.connect((socket.gethostname(),2306))
            self.serverP.send("CL".encode())
            return True

        except:
            print("Servidor não aberto")
            return False

    def loop(self):
        while True:
            msg = input("Mensagem: ")
            self.serverP.send(msg.encode())
            while True:
                msg2 = self.serverP.recv(32).decode()
                if msg2:
                    print(msg2)
                    self.erros[int(msg2)]
                    break


Main().start()