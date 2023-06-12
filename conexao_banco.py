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

        cursor.execute(""" 
                        SELECT * FROM PESSOA 
                        WHERE Nome LIKE ? ORDER BY Nome LIMIT 20""",
                       ('%' + dados['nome'] + '%',))
        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO PESSOA (Nome, Endereco, Telefone, Email)
                        VALUES (?, ?, ?, ?)""",
                       (dados['nome'], dados['endereco'], dados['telefone'], dados['email']))

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
                        INSERT INTO USUARIO (login, senha, admin)
                        VALUES (?, ?, ?)""",
                       (dados['login'], dados['senha'], dados['admin']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE USUARIO set login = ?, senha = ?, admin = ?
                        WHERE ID_Usuario = ?""",
                       (dados['login'], dados['senha'], dados['admin'], dados['id_usuario']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM USUARIO WHERE id_usuario = ?""",
                       (dados['id_usuario'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_item(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT * FROM ITEM 
                WHERE descricao LIKE ? 
                ORDER BY descricao LIMIT 20""",
            ('%' + dados['descricao'] + '%',))

        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO ITEM (descricao, qtd, id_tipo_item)
                        VALUES (?, ?, ?)""",
                       (dados['descricao'], dados['qtd'], dados['id_tipo_item']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE ITEM set descricao = ?, qtd = ?, id_tipo_item = ?
                        WHERE id_item = ?""",
                       (dados['descricao'], dados['qtd'], dados['id_tipo_item'], dados['id_item']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM ITEM WHERE id_item = ?""",
                       (dados['id_item'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_tipo_item(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT * FROM TIPO_ITEM 
                WHERE descricao LIKE ? 
                ORDER BY descricao LIMIT 20""",
            ('%' + dados['descricao'] + '%',))

        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO TIPO_ITEM (descricao)
                        VALUES (?)""",
                       (dados['descricao'],))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE TIPO_ITEM set descricao = ?
                        WHERE id_tipo_item = ?""",
                       (dados['descricao'], dados['id_tipo_item'],))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM TIPO_ITEM WHERE id_tipo_item = ?""",
                       (dados['id_tipo_item'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_item_saida(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":

        if dados['id_saida'] and not dados['id_item']:

            cursor.execute(
                """ SELECT * FROM ITEM_SAIDA 
                    WHERE id_saida = ? 
                    ORDER BY qt_item LIMIT 20""",
                (dados['id_saida'],))

            resposta = cursor.fetchall()
            commit_e_fechar_conexao(conn)

            return resposta

        if dados['id_item'] and not dados['id_saida']:
            cursor.execute(
                """ SELECT * FROM ITEM_SAIDA 
                    WHERE id_item = ? 
                    ORDER BY qt_item LIMIT 20""",
                (dados['id_item'],))

            resposta = cursor.fetchall()
            commit_e_fechar_conexao(conn)

            return resposta

        cursor.execute(
            """ SELECT * FROM ITEM_SAIDA 
                WHERE  id_saida = ?
                AND id_item = ? 
                ORDER BY qt_item LIMIT 20""",
            (dados['id_saida'], dados['id_item'],))

        resposta = cursor.fetchall()
        commit_e_fechar_conexao(conn)

        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO ITEM_SAIDA (id_saida, id_item, qt_item)
                        VALUES (?, ?, ?)""",
                       (dados['id_saida'], dados['id_item'], dados['qt_item']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE ITEM_SAIDA set qt_item = ?
                        WHERE  id_saida = ?
                        AND id_item = ?""",
                       (dados['qt_item'], dados['id_saida'], dados['id_item']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM ITEM_SAIDA 
                        WHERE  id_saida = ?
                        AND id_item = ?""",
                       (dados['id_saida'], dados['id_item'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_saida(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT * FROM SAIDA 
                WHERE observacao LIKE ? 
                ORDER BY dt_saida LIMIT 20""",
            ('%' + dados['observacao'] + '%',))

        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO SAIDA (dt_saida, observacao, id_tipo_saida)
                        VALUES (?, ?, ?)""",
                       (dados['dt_saida'], dados['observacao'], dados['id_tipo_saida']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE SAIDA set dt_saida = ?, observacao = ?, id_tipo_saida = ?
                        WHERE id_saida = ?""",
                       (dados['dt_saida'], dados['observacao'], dados['id_tipo_saida'], dados['id_saida']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM SAIDA WHERE id_saida = ?""",
                       (dados['id_saida'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_tipo_saida(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT * FROM TIPO_SAIDA 
                WHERE descricao LIKE ? 
                ORDER BY descricao LIMIT 20""",
            ('%' + dados['descricao'] + '%',))

        resposta = cursor.fetchall()

        commit_e_fechar_conexao(conn)
        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO TIPO_SAIDA (descricao)
                        VALUES (?)""",
                       (dados['descricao'],))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE TIPO_SAIDA set descricao = ?
                        WHERE id_tipo_saida = ?""",
                       (dados['descricao'], dados['id_tipo_saida']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM TIPO_SAIDA WHERE id_tipo_saida = ?""",
                       (dados['id_tipo_saida'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_item_doacao(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":

        if dados['id_item'] and not dados['id_doacao']:

            cursor.execute(
                """ SELECT * FROM ITEM_DOACAO 
                    WHERE id_item = ? 
                    ORDER BY qt_item LIMIT 20""",
                (dados['id_item'],))

            resposta = cursor.fetchall()
            commit_e_fechar_conexao(conn)

            return resposta

        if dados['id_doacao'] and not dados['id_item']:
            cursor.execute(
                """ SELECT * FROM ITEM_DOACAO 
                    WHERE id_doacao = ? 
                    ORDER BY qt_item LIMIT 20""",
                (dados['id_doacao'],))

            resposta = cursor.fetchall()
            commit_e_fechar_conexao(conn)

            return resposta

        cursor.execute(
            """ SELECT * FROM ITEM_DOACAO 
                WHERE id_item = ? 
                AND id_doacao = ?
                ORDER BY qt_item LIMIT 20""",
            (dados['id_item'], dados['id_doacao']))

        resposta = cursor.fetchall()
        commit_e_fechar_conexao(conn)

        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO ITEM_DOACAO (id_item, id_doacao, qt_item)
                        VALUES (?, ?, ?)""",
                       (dados['id_item'], dados['id_doacao'], dados['qt_item']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE ITEM_DOACAO set qt_item = ?, 
                        WHERE id_item = ? 
                        AND id_doacao = ?""",
                       (dados['qt_item'], dados['id_item'], dados['id_doacao']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM ITEM_DOACAO 
                        WHERE id_item = ? 
                        AND id_doacao = ?""",
                       (dados['qt_item'], dados['id_item']))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)


def operar_doacao(operador, dados):
    conn, cursor = conectar_banco_e_cursor()

    if dados is None and (operador != "SELECT"):
        return print("dados vazio")

    if operador == "SELECT":
        cursor.execute(
            """ SELECT 
                    id_doacao, dt_doacao, observacao, nome,
                    login, D.id_pessoa, D.id_usuario  
                FROM DOACAO D, PESSOA P, USUARIO U
                WHERE observacao LIKE ?
                AND D.id_pessoa = P.id_pessoa
                AND D.id_usuario = U.id_usuario
                ORDER BY observacao LIMIT 20""",
            ('%' + dados['observacao'] + '%',))

        resposta = cursor.fetchall()
        commit_e_fechar_conexao(conn)

        return resposta

    if operador == "INSERT":
        cursor.execute(""" 
                        INSERT INTO DOACAO (dt_doacao, observacao, id_pessoa, id_usuario)
                        VALUES (?, ?, ?, ?)""",
                       (dados['dt_doacao'], dados['observacao'], dados['id_pessoa'], dados['id_usuario']))

        print("Insert feito com sucesso")

    if operador == "UPDATE":
        cursor.execute("""
                        UPDATE DOACAO set dt_doacao = ?, observacao = ?, id_pessoa = ?
                        WHERE id_doacao = ?""",
                       (dados['dt_doacao'], dados['observacao'], dados['id_doacao'], dados['id_pessoa']))

        print("UPDATE feito com sucesso")

    if operador == "DELETE":
        cursor.execute("""
                        DELETE FROM DOACAO 
                        WHERE id_doacao = ?""",
                       (dados['id_doacao'],))
        print("DELETE feito com sucesso")

    commit_e_fechar_conexao(conn)




