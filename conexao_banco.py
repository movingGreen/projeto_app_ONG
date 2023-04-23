import sqlite3
from comandos_criar_BD import scriptsCriarTabelas 

# conexão com banco sqlite
conn = sqlite3.connect('Inventario_ONG.db')

# definindo um cursor
cursor = conn.cursor()

# criando as tabelas (schema)
for comando, script in scriptsCriarTabelas.items():
    cursor.execute(script)
    print("Tabela " + comando + " criada com sucesso")

# criando um usuarion admin
# cursor.execute("""
#                 INSERT INTO USUARIO (id_Usuario, Login, Senha)
#                 VALUES (1, 'admin', '123')
#             """
# )

# print(cursor.execute("""
#                 SELECT * FROM USUARIO
#             """
# ).fetchall())

# gravando no banco de dados os comandos
conn.commit()

print("Comandos executados com sucesso")
conn.close()
