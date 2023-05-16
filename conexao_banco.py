import sqlite3
from comandos_criar_BD import scriptsCriarTabelas 

def conectarBancoECursor():
    # conexão com banco sqlite
    conn = sqlite3.connect('Inventario_ONG.db')
    
    print("Conexão com o banco de dados feita com sucesso")

    # definindo um cursor
    cursor = conn.cursor()
    
    print("cursor criado")
    return [conn, cursor]

# criando as tabelas (schema)
def criarTabelas(cursor):
    for comando, script in scriptsCriarTabelas.items():
        cursor.execute(script)
        print("Tabela " + comando + " criada com sucesso")
        
    print("Tabelas criadas com sucesso")

# criando um usuarion admin
def insertUsuario(cursor, login, senha):
    cursor.execute("""
                    INSERT INTO USUARIO ( Login, Senha)
                    VALUES (?, ?)""", (login,  senha))
    
    print("Comandos feitos com sucesso")

def selectUsuario(cursor, login):
    cursor.execute(""" SELECT * FROM USUARIO WHERE login = ?""", (login,))
    resposta = cursor.fetchall()
    
    return resposta


def operar_pessoa(cursor, operador, dados=None):
    if dados is None:
        dadosInserir = ['']


def commitEFecharConexao(conector):
    # gravando no banco de dados os comandos
    conector.commit()
    # fechando conexão com o banco de dados
    conector.close()
    
    print("Comandos salvos e conexão fechada")



