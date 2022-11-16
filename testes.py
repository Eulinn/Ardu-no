import sqlite3


banco = sqlite3.connect('./banco/arducontole.db')
cursor = banco.cursor()



cursor.execute('''

CREATE TABLE usuario(id_usu int(11) not null, nome_usu text(30) not null,senha_usu text(50) not null, permic_usu int(2) not null,
PRIMARY KEY (id_usu)
);
''')


cursor.execute('''CREATE TABLE historico(id_usu int(11) not null, data_evento date not null, tipo_evento text(50) not null);''')


cursor.execute('''CREATE TABLE modulos(id_modulo int(11) not null);''')

banco.commit()