import sqlite3
from comandos_criar_BD import scriptsCriarTabelas 

# conexão com banco sqlite
conn = sqlite3.connect('Inventario_ONG.db')

# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
for comando, script in scriptsCriarTabelas.items():
    cursor.execute(script)
    print("Tabela " + comando + " criada com sucesso")

print("Banco de dados criado com sucesso")
conn.close()
