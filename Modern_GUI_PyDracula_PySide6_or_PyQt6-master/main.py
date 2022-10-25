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

import sys
import os
import platform
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
        self.mensagens=['Arduino inexistente ou não conectado!!',
        "Enviado",
        "Conectando ao server...",
        "Server conectado, vá para a aba de controles!",
        "Servidor Não Conectado, tentando conectar novamente!",
        "Login Inválido!",
        "Login validado",
        "Erro no servidor"]

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
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.Login.clicked.connect(self.buttonClick)

        widgets.botaoenviar.clicked.connect(self.buttonClick)


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

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        
        if btnName == "login":
            if (widgets.titleRightInfo.text() != self.mensagens[4] and widgets.titleRightInfo.text() != self.mensagens[2]):
                widgets.stackedWidget.setCurrentWidget(widgets.login_page) # SET PAGE
                UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
                btn.setStyleSheet('background-image: url(:/icons/images/icons/cil-user.png)')
            else:
                widgets.Login.setText(QCoreApplication.translate("MainWindow", u"Login Inacessível", None))
                btn.setStyleSheet('background-image: url(:/icons/images/icons/cil-user.png)')
                UIFunctions.toggleMenu(self, True)

        if btnName == "Logenviar" and self.usuario == None:
            if(widgets.usuario.text() != "" and widgets.senha.text() != ""):
                start_new_thread(self.validarLogin,(widgets,None))
                
                








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


    def server(self,widgets,a):
        contador = 1
        while True:
            try:
                self.serverP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.serverP.connect((socket.gethostname(),2306))
                self.serverP.send("CL".encode())
                widgets.titleRightInfo.setText(self.mensagens[3])
                break
    
            except:
                widgets.titleRightInfo.setText(self.mensagens[4])
                contador+=1
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
