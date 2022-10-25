
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

            Comparacao = valor* appleValor
            dia = time.strftime(r'%d/%m/%Y - %H:%M',time.localtime())
            texto = f"{dia} :: AppleBR - R${str(appleValorBR).replace('.',',')}      AppleEUA - U${appleValor} com Dolar à R${str(round(valor,2)).replace('.',',')} - R${str(round(Comparacao,2)).replace('.',',')} // Economia - R$ {str(round((appleValorBR-Comparacao),2)).replace('.',',')}"
            with open("./Relatorio.txt",'r') as arq:
                listatexto = arq.readlines()
            with open("./Relatorio.txt",'w+') as arq:
                for j in listatexto:
                    arq.writelines(j)
                arq.writelines(texto+'\n')
            


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
        valor = self.Chrome.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
        return float(valor.replace(",","."))


    def ProdutoApple(self):
        self.Chrome.get('https://www.apple.com/shop/buy-iphone/iphone-14-pro')
        time.sleep(3)
        valor = self.Chrome.find_element(By.XPATH,'//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div').text
        ValorReal = ''
        for j in valor.split():
            if '$' in list(j):
                if j.replace('$','').isdigit():
                    ValorReal = int(j.replace('$',''))
        
        return ValorReal
    

    def ProdutoAppleBrasil(self):
        self.Chrome.get('https://www.apple.com/br/shop/buy-iphone/iphone-14-pro')
        valor = self.Chrome.find_element(By.XPATH,'//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div').text
        time.sleep(3)
        ValorReal = ''
        for j in valor.split():
            if j.replace('.',"").isdigit():
                ValorReal = int(j.replace('.',""))
        
        return ValorReal
        


  
Main()