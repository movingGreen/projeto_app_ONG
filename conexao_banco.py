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


def commitEFecharConexao(conector):
    # gravando no banco de dados os comandos
    conector.commit()
    # fechando conexão com o banco de dados
    conector.close()

    print("Comandos salvos e conexão fechada")


# criando as tabelas (schema)
def criarTabelas():
    conn, cursor = conectarBancoECursor()

    for comando, script in scriptsCriarTabelas.items():
        cursor.execute(script)
        print("Tabela " + comando + " criada com sucesso")
        
    print("Tabelas criadas com sucesso")

    commitEFecharConexao(conn)


# criando um usuarion admin
def insertUsuario(login, senha):
    conn, cursor = conectarBancoECursor()

    cursor.execute("""
                    INSERT INTO USUARIO ( Login, Senha)
                    VALUES (?, ?)""", (login,  senha))
    
    print("Comandos feitos com sucesso")
    commitEFecharConexao(conn)


def selectUsuario(login):
    conn, cursor = conectarBancoECursor()

    cursor.execute(""" SELECT * FROM USUARIO WHERE login = ?""", (login,))
    resposta = cursor.fetchall()

    commitEFecharConexao(conn)
    
    return resposta


def operar_pessoa(operador, dados=None):
    conn, cursor = conectarBancoECursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        if not dados['nome']:
            cursor.execute(""" SELECT * FROM PESSOA ORDER BY Nome LIMIT 20""")
            resposta = cursor.fetchall()

            commitEFecharConexao(conn)
            return resposta

        cursor.execute(""" SELECT * FROM PESSOA WHERE Nome LIKE ? ORDER BY Nome LIMIT 20""", ('%' + dados['nome'] + '%',))
        resposta = cursor.fetchall()

        commitEFecharConexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO PESSOA (Nome, Endereco, Telefone, Email)
                        VALUES (?, ?, ?, ?)""", (dados['nome'], dados['endereco'], dados['telefone'], dados['email']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE PESSOA set Nome = ?, Endereco = ?, Telefone = ?, Email = ?
                        WHERE ID_Pessoa = ?""",
                       (dados['nome'], dados['endereco'], dados['telefone'], dados['email'], dados['id_pessoa']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM PESSOA WHERE Nome = ?""", (dados['nome'],))
        print("DELETE feito com sucesso")

    commitEFecharConexao(conn)



