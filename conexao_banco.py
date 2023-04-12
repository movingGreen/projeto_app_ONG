import sqlite3
import comando_criar_BD as scriptsDB

# conexão com banco sqlite
conn = sqlite3.connect('clientes.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute(scriptsDB.criarTabelaUsuario)

print("Tabela Usuário criada com sucesso")
conn.close()
