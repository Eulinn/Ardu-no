import requests
import socket
from _thread import *
import sqlite3
import time
from datetime import date

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
            self.banco = sqlite3.connect('./banco/arducontole.db',check_same_thread=False)
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
            
    
    def EnviarComando(self,valor,usuario):

        try:
            rq = requests.get(f'http://192.168.0.101/?relay{valor}')
            if (rq.text == r'[{relay0:off}]'):
                self.adicionarhistorico(usuario,"Desligou PinOut0")
                return 14
            elif (rq.text == r'[{relay0:on}]'):
                self.adicionarhistorico(usuario,"Ligou PinOut0")
                return 13
            elif (rq.text == r'[{relay2:off}]'):
                self.adicionarhistorico(usuario,"Desligou PinOut2")
                return 16
            elif (rq.text == r'[{relay2:on}]'):
                self.adicionarhistorico(usuario,"Ligou PinOut2")
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
                        if(self.verificarUsuario(Verificar[0],Verificar[1],cliente)):
                            print("passou login")
                        else:
                            cliente.send('5'.encode())
                    if ver[0] == 'pin':
                        Verificar = ver[1].split(";")
                        cliente.send(str(self.EnviarComando(Verificar[0],Verificar[1])).encode())
                    if ver[0] == 'bloq':
                        Verificar = ver[1].split(";")
                        cliente.send(str(self.bloquear(Verificar[0],Verificar[1])).encode())
                    if ver[0] == 'desbloq':
                        Verificar = ver[1].split(";")
                        cliente.send(str(self.desbloquear(Verificar[0],Verificar[1])).encode())
                    if ver[0] == 'hist':
                        print("enviou")
                        cliente.send(str(self.enviarhist(ver[1])).encode())
                        print("recebeu")
                    if ver[0] == 'cad':
                         Verificar = ver[1].split(";")
                         rrr = self.Cadastro(Verificar[0],Verificar[1])
                         print(rrr, "rrr aqui")
                         cliente.send(str(rrr).encode())



                except OSError as erro:
                    print(erro)
                    try:
                        cliente.send("7".encode())
                    except:
                        self.clientes.remove(cliente)
    

    def verificarUsuario(self,nome,senha,cliente):
        try:
            self.cursor.execute(f'SELECT * FROM usuario WHERE nome="{nome}" and senha="{senha}"')
            com = self.cursor.fetchall()
            if(len(com) == 1):
                print("len passou")
                self.banco.commit()
                if(com[0][3] == 0):
                    cliente.send("6 0".encode())
                    print("aa1")
                else:
                    cliente.send("6 1".encode())
                    print("aa2")

                return True
            else:
                self.banco.commit()
                return False
        
        except OSError as erro:
            self.banco.commit()
            print(erro)
            return False


    def Cadastro(self,nome,senha):
        print(nome)
        try:
            self.cursor.execute(f'SELECT * FROM usuario WHERE nome="{nome}";')
            print("Mandou o select")
            tt = self.cursor.fetchall()
            print(tt)
            if(len(tt) == 1):
                print("Esse usuário já existe")
                self.banco.commit()
                return 23
            else:
                print("E vamos de mandar")
                self.cursor.execute(f'INSERT INTO usuario(nome,senha,adm) VALUES("{nome}","{senha}",0)')
                print("Mandou")
                self.banco.commit()
                return 24
            
        
        except OSError as err:
            print(err)
            return 22



    def pegarID(self,usuario):
        try:
            self.cursor.execute(f'SELECT id_usu FROM usuario WHERE nome = "{usuario}"')
            numero = self.cursor.fetchall()
            self.banco.commit()
            return numero[0][0]
        
        except OSError as erro:
            print(erro)
            return False
    
    def bloquear(self,usuario,dispositivo):
        id = self.pegarID(usuario)
        if(id != False):
            usuario = id
            try:
                self.cursor.execute(f'INSERT INTO bloqueio(id_usu,dispositivo) VALUES({usuario},{dispositivo});')
                self.banco.commit()
                return 28
            
            except:
                return 22
        else:
            return 22
    
    def desbloquear(self,usuario,dispositivo):
        id = self.pegarID(usuario)
        if(id != False):
            usuario = id
            try:
                self.cursor.execute(f'DELETE FROM bloqueio WHERE id_usu = {usuario} and dispositivo = {dispositivo}')
                self.banco.commit()
                return 29
            
            except:
                return 22
        else:
            return 22


    def adicionarhistorico(self,usuario,acao):
        id = self.pegarID(usuario)
        if(id != False):
            usuario = id

            data = date.today()
            hora = time.strftime("%H:%M:%S")

            try:
                self.cursor.execute(f'INSERT INTO historico(id_usu,data,horario,acao) VALUES({usuario},{data},{hora},{acao});')
                self.banco.commit()
            
            except:
                return

        else:
            return 22


    def enviarhist(self,usuario):
        id = self.pegarID(usuario)
        if(id != False):
            usuario = id

            try:
                self.cursor.execute(f'SELECT * FROM historico WHERE id_usu={usuario};')
                listahist = self.cursor.fetchall()
                self.banco.commit()

                textofinal = ''
                for j in listahist:
                    texto2 = ''
                    for k in j:
                        texto2+=str(k)+';'
                    textofinal+=texto2+'#'
                
                return textofinal

            except OSError as err:
                print(err)
                return 30

        else:
            return 30




            


Main().start()