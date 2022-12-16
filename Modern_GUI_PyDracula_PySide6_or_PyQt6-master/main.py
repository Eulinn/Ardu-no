# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

from time import sleep
import sys
import os
import socket
from _thread import start_new_thread

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        self.pins = []
        self.msgs = True
        self.conected = False
        self.mensagens=['Arduino inexistente ou não conectado!!',
        "Enviado",#1
        "Conectando ao server...",#2
        "Server conectado, vá para a aba de LOGIN!",#3
        "Servidor Não Conectado, tentando conectar novamente!",#4
        "Login Inválido!",#5
        "Login validado",#6
        "Erro no servidor",#7
        "Esperando resposta...",#8
        "Dispositivo Ligado",#9
        "Dispositivo Desligado",#10
        "Login indisponível sem conexão!",#11
        "Conecte-se para acessar dispositivos!",#12
        "PinOut0 ligado",#13
        "PinOut0 Desligado",#14
        "PinOut2 ligado",#15
        "PinOut2 Desligado",#16
        "PinOut0 Já está ligado",#17
        "PinOut0 Já está Desligado",#18
        "PinOut2 Já está ligado",#19
        "PinOut2 Já está Desligado",#20
        "Dispositivo com Erro",#21
        "Mensagem Inesperada",#22
        "Usuário Já Existente",#23
        "Cadastrado"#24
        ]

        self.usuario = None
        
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Dispositivos"
        description = self.mensagens[2]
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)


        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))



        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)


        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////


        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_dispositivos.clicked.connect(self.buttonClick)
        widgets.Login.clicked.connect(self.buttonClick)
        widgets.botaocadastro.clicked.connect(self.buttonClick)
        widgets.botaologin.clicked.connect(self.buttonClick)
        widgets.historico.clicked.connect(self.buttonClick)

        widgets.botaoenviar.clicked.connect(self.buttonClick)
        widgets.btn_lig_1.clicked.connect(self.buttonClick)
        widgets.btn_lig_2.clicked.connect(self.buttonClick)
        widgets.btn_deslig_1.clicked.connect(self.buttonClick)
        widgets.btn_deslig_2.clicked.connect(self.buttonClick)
        widgets.botaoenviar_cad.clicked.connect(self.buttonClick)


        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # Aqui abre uma aba no canto direito  ein, pode ser usado posteriormente viu viu viu
        '''def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)'''

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        start_new_thread(self.server,(widgets,None))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            print(btn.styleSheet())

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_dispositivos" and self.usuario != None:
            widgets.stackedWidget.setCurrentWidget(widgets.Dispositivos) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        else:
            start_new_thread(self.MSGTemp,(12,2,widgets))
        
        if btnName == "Cadastro":
            widgets.stackedWidget.setCurrentWidget(widgets.cad_page)
        

        if btnName == 'Ligar1':
            start_new_thread(self.enviarcomando,('pin-0=on',''))
        if btnName == 'Ligar2':
            start_new_thread(self.enviarcomando,('pin-2=on',''))
        if btnName == 'Desligar1':
            start_new_thread(self.enviarcomando,('pin-0=off',''))
        if btnName == 'Desligar2':
            start_new_thread(self.enviarcomando,('pin-2=off',''))
        
        print(f"botao clicado {btnName}")


        if btnName == "login_2":
            widgets.stackedWidget.setCurrentWidget(widgets.login_page)


        if btnName == "login":
            if(self.conected):
                widgets.stackedWidget.setCurrentWidget(widgets.login_page) # SET PAGE
                UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            else:
                start_new_thread(self.MSGTemp,(11,2,widgets))
        
        if btnName == "Cadenviar":
            if(widgets.usuario_cad.text() != "" and widgets.senha_cad.text() != ""):
                start_new_thread(self.validarLogin,(widgets,None))
                

        if btnName == "Logenviar" and self.usuario == None:
            if(widgets.usuario.text() != "" and widgets.senha.text() != ""):
                start_new_thread(self.validarLogin,(widgets,None))
        
        if btnName == "historico":
            widgets.stackedWidget.setCurrentWidget(widgets.Historico_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
                
                



    def AlimentarHistorico(self,widgets,valor_usu,valor_acao,valor_data,valor_horario):
        usuario = QTableWidgetItem(valor_usu)
        acao = QTableWidgetItem(valor_acao)
        data = QTableWidgetItem(valor_data)
        horario = QTableWidgetItem(valor_horario)
        qnt = widgets.TabelaHitorico.rowCount()
        widgets.TabelaHitorico.setRowCount(qnt+1)
        widgets.TabelaHitorico.setItem(qnt,0,usuario)
        widgets.TabelaHitorico.setItem(qnt,1,horario)
        widgets.TabelaHitorico.setItem(qnt,2,data)
        widgets.TabelaHitorico.setItem(qnt,3,acao)
            





    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


    def validarLogin(self,widgets,a):
        us = widgets.usuario.text()
        sh = widgets.senha.text()

        self.serverP.send(f'lg-{us};{sh}'.encode())
        while True:
            
            msg = self.serverP.recv(32).decode("utf-8")
            if msg:
                if int(msg) == 5:
                    widgets.titleRightInfo.setText(self.mensagens[5] + " Tente novamente.")
                    break
                elif int(msg) == 6:
                    widgets.titleRightInfo.setText(self.mensagens[6]+f" Bem Vindo(a), {us}")
                    widgets.Login.setText(QCoreApplication.translate("MainWindow", u"Logado", None))
                    self.usuario = us
                    break
                elif int(msg) == 7:
                    widgets.titleRightInfo.setText(self.mensagens[7])
                    break
    
    def validarCadastro(self,widgets,a):
        us = widgets.usuario_cad.text()
        sh = widgets.senha_cad.text()

        self.serverP.send(f'cad-{us};{sh}'.encode())
        while True:
            
            msg = self.serverP.recv(32).decode("utf-8")
            if msg:
                if int(msg) == 23:
                    widgets.titleRightInfo.setText(self.mensagens[23] + " Tente novamente.")
                    break
                elif int(msg) == 24:
                    widgets.titleRightInfo.setText(self.mensagens[24]+f" Bem Vindo(a), {us}")
                    widgets.Login.setText(QCoreApplication.translate("MainWindow", u"Logado", None))
                    self.usuario = us
                    break
                elif int(msg) == 22:
                    widgets.titleRightInfo.setText(self.mensagens[22])
                    break


    def server(self,widgets,a):
        contador = 1
        while True:
            try:
                self.serverP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.serverP.connect((socket.gethostname(),2306))
                self.serverP.send("CL".encode())
                widgets.titleRightInfo.setText(self.mensagens[3])
                self.conected = True
                break

            except:
                if self.msgs:
                    widgets.titleRightInfo.setText(self.mensagens[4])
                contador+=1
    

    def MSGTemp(self,msg,temp,widgets):
        self.msgs = False
        widgets.titleRightInfo.setText(self.mensagens[msg])
        sleep(temp)
        self.msgs = True
    

    def enviarcomando(self,comando,a):
        try:
            self.serverP.send(comando.encode())
            while True:
                msg = self.serverP.recv(32).decode('utf-8')
                if msg:
                    widgets.titleRightInfo.setText(self.mensagens[int(msg)])
                    break
        except OSError as erro:
            widgets.titleRightInfo.setText(self.mensagens[7])
            print(erro)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
