import sqlite3

#tabela usuario tem q por o nome,senha e adm
#tabela historico quem q por a fk do usuario(id_usu), ação e data

#self.verificarUsuario(Verificar[0],Verificar[1])

db = sqlite3.connect('./banco/arducontole.db')
cursor = db.cursor()

cursor.execute(f'SELECT * FROM usuario WHERE nome="eulin" and senha="1234"')
lista = cursor.fetchall()
print(lista)



