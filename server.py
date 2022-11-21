import requests
import socket
from _thread import *
import sqlite3

class Main():
    def __init__(self) -> None:
        self.clientes = []

    def mensagemClientes(self):
        pass
 
    def start(self):
        if(self.server()):
            self.loop()



    def server(self):
        try:
            self.banco = sqlite3.connect('./banco/arducontole.db')
            self.cursor = self.banco.cursor()
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
            
            elif str(mensagem_arduino) == "CL":
                self.clientes.append(client)
                start_new_thread(self.controleCLiente,(client,0))
            
    
    def EnviarComando(self,valor):
        

        try:
            rq = requests.get(f'http://192.168.0.101/?relay{valor}')
            if (rq.text == r'[{relay0:off}]'):
                return 14
            elif (rq.text == r'[{relay0:on}]'):
                return 13
            elif (rq.text == r'[{relay2:off}]'):
                return 16
            elif (rq.text == r'[{relay2:on}]'):
                return 15
            elif (rq.text == r'[{relay0:justoff}]'):
                return 18
            elif (rq.text == r'[{relay0:juston}]'):
                return 17
            elif (rq.text == r'[{relay2:justoff}]'):
                return 20
            elif (rq.text == r'[{relay2:juston}]'):
                return 19
            else:
                return 22
        except OSError as erro:
            return 21

            

    def controleCLiente(self,cliente,a):
        while True:
            msg = cliente.recv(32).decode("utf-8")
            if msg:
                try:
                    ver = msg.split('-')
                    if ver[0] == "lg":
                        Verificar = ver[1].split(";")
                        if(self.verificarUsuario(Verificar[0],Verificar[1])):
                            cliente.send("6".encode())
                        else:
                            cliente.send('5'.encode())
                    if ver[0] == 'pin':
                        cliente.send(str(self.EnviarComando(ver[1])).encode())

                except:
                    try:
                        cliente.send("7".encode())
                    except:
                        self.clientes.remove(cliente)
    

    def verificarUsuario(self,nome,senha):
        try:
            self.cursor.execute(f'SELECT * FROM usuario WHERE nome_usu = "{nome}" and senha_usu = "{senha}"')
            if(len(self.cursor.fetchall()) == 1):
                return True
            else:
                return False
        
        except:
            return False


    def Cadastro(self,nome,senha):
        try:
            self.cursor.execute(f'SELECT * FROM usuario WHERE nome_usu = "{nome}"')
            if(len(self.cursor.fetchall()) == 1):
                return 23
            else:
                self.cursor.execute(f"INSERT INTO usuario ()")
                return 24
        
        except:
            return 22

            

    




            


Main().start()