import sqlite3
from comandos_criar_BD import scriptsCriarTabelas 


def conectar_banco_e_cursor():
    # conexão com banco sqlite
    conn = sqlite3.connect('Inventario_ONG.db')
    
    print("Conexão com o banco de dados feita com sucesso")

    # definindo um cursor
    cursor = conn.cursor()
    
    print("cursor criado")
    return [conn, cursor]


def commit_e_fechar_conexao(conector):
    # gravando no banco de dados os comandos
    conector.commit()
    # fechando conexão com o banco de dados
    conector.close()

    print("Comandos salvos e conexão fechada")


# criando as tabelas (schema)
def criar_tabelas():
    conn, cursor = conectar_banco_e_cursor()

    for comando, script in scriptsCriarTabelas.items():
        cursor.execute(script)
        print("Tabela " + comando + " criada com sucesso")
        
    print("Tabelas criadas com sucesso")

    commit_e_fechar_conexao(conn)


# criando um usuarion admin
def insert_usuario(login, senha):
    conn, cursor = conectar_banco_e_cursor()

    cursor.execute("""
                    INSERT INTO USUARIO ( Login, Senha)
                    VALUES (?, ?)""", (login,  senha))
    
    print("Comandos feitos com sucesso")
    commit_e_fechar_conexao(conn)


def select_um_usuario(login):
    conn, cursor = conectar_banco_e_cursor()

    cursor.execute(""" SELECT * FROM USUARIO WHERE login = ?""", (login,))
    resposta = cursor.fetchall()

    commit_e_fechar_conexao(conn)
    
    return resposta


def operar_pessoa(operador, dados=None):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        if not dados['nome']:
            cursor.execute(""" SELECT * FROM PESSOA ORDER BY Nome LIMIT 20""")
            resposta = cursor.fetchall()

            commit_e_fechar_conexao(conn)
            return resposta

        cursor.execute(""" SELECT * FROM PESSOA WHERE Nome LIKE ? ORDER BY Nome LIMIT 20""", ('%' + dados['nome'] + '%',))
        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
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
                        DELETE FROM PESSOA WHERE id_pessoa = ?""", (dados['id_pessoa'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_usuario(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT * FROM USUARIO 
                WHERE login LIKE ? 
                ORDER BY login LIMIT 20""",
            ('%' + dados['login'] + '%',))

        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO USUARIO (login, senha)
                        VALUES (?, ?)""",
                       (dados['login'], dados['senha']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE USUARIO set login = ?, senha = ?
                        WHERE ID_Usuario = ?""",
                       (dados['login'], dados['senha'], dados['id_usuario']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM USUARIO WHERE id_usuario = ?""",
                       (dados['id_usuario'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


