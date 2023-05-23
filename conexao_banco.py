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
    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        if not dados['nome']:
            cursor.execute(""" SELECT * FROM PESSOA ORDER BY Nome LIMIT 20""")
            resposta = cursor.fetchall()
            return resposta

        cursor.execute(""" SELECT * FROM PESSOA WHERE Nome LIKE ? ORDER BY Nome LIMIT 20""", (dados['nome'],))
        resposta = cursor.fetchall()
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO PESSOA (Nome, Endereco, Telefone, Email)
                        VALUES (?, ?, ?, ?)""", (dados['nome'], dados['endereco'], dados['telefone'], dados['email']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE PESSOA set Nome = ?, Endereco = ?, Telefone = ?, Email = ?
                        WHERE Nome = ?""",
                       (dados['nome'], dados['endereco'], dados['telefone'], dados['email'], dados['nome']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM PESSOA WHERE Nome = ?""", dados['nome'])
        print("DELETE feito com sucesso")




def commitEFecharConexao(conector):
    # gravando no banco de dados os comandos
    conector.commit()
    # fechando conexão com o banco de dados
    conector.close()
    
    print("Comandos salvos e conexão fechada")



