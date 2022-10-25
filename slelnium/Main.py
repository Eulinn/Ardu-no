
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Main():
    def __init__(self):
        if(self.VerificarDriver()):
            self.Chrome.get('https://www.google.com/')
            valor =  self.pesquisarDolar()
            appleValor = self.ProdutoApple()
            appleValorBR = self.ProdutoAppleBrasil()
            print()


            
            
  
            input()
        else:
            print("Driver Do Chrome Não Encontrado")
    

    def VerificarDriver(self):
        try:
            self.Chrome = webdriver.Chrome(ChromeDriverManager().install())
            return True
        except:
            return False
    

    def pesquisarDolar(self):
        self.Chrome.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Dolar hoje')
        self.Chrome.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]').click()
        return self.Chrome.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text

    def ProdutoApple(self):
        self.Chrome.get('https://www.apple.com/shop/buy-iphone/iphone-14-pro')
        #time.sleep(5)
        valor = self.Chrome.find_element(By.XPATH,'//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div').text
        ValorReal = ''
        for j in valor.split():
            if '$' in list(j) or j.isdigit():
                if j.replace('$','').isdigit():
                    ValorReal = int(j.replace('$',''))
        
        return ValorReal
    

    def ProdutoAppleBrasil(self):
        self.Chrome.get('https://www.apple.com/br/shop/buy-iphone/iphone-14-pro')
        valor = self.Chrome.find_element(By.XPATH,'//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div').text
        ValorReal = ''
        for j in valor.split():
            if '$' in list(j) or j.isdigit():
                if j.replace('$','').isdigit():
                    ValorReal = int(j.replace('$',''))
        
        return ValorReal
        


  
Main()