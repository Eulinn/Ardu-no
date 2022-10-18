
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Main():
    def __init__(self):
        if(self.VerificarDriver()):
            self.Chrome.get("https://www.instagram.com/accounts/login/")
            
            
        else:
            print("Driver Do Chrome Não Encontrado")
    

    def VerificarDriver(self):
        try:
            self.Chrome = webdriver.Chrome(ChromeDriverManager().install())
            return True
        except:
            return False


  
Main()