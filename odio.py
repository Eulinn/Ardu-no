import sqlite3


banco = sqlite3.connect('./banco/arducontole.db')
cursor = banco.cursor()


cursor.execute(f'SELECT * FROM usuario where nome_usu = "aaa" and senha_usu = "123"')
print(cursor.fetchall())

