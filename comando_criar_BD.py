criarTabelaPessoa = """
    CREATE TABLE PESSOA (
    ID_Pessoa  SERIAL PRIMARY KEY,
    Nome VARCHAR(50),
    Endereco VARCHAR(100),
    Telefone VARCHAR(11),
    Email VARCHAR(30)
    );
"""

criarTabelaTipo_item = """
    CREATE TABLE Tipo_Item (
    ID_Tipo_Item SERIAL PRIMARY KEY,
    Descricao VARCHAR(50)
    );
"""

criarTabelaTipo_saida = """
    CREATE TABLE TIPO_SAIDA (
    ID_Tipo_Saida SERIAL PRIMARY KEY,
    Descricao VARCHAR(30)
    );
"""

criarTabelaSaida = """
    CREATE TABLE SAIDA (
    ID_Saida SERIAL PRIMARY KEY,
    DT_Saida DATE,
    Observacao VARCHAR(100),
    ID_Tipo_Saida INTEGER,
    FOREIGN KEY(ID_Tipo_Saida) REFERENCES TIPO_SAIDA (ID_Tipo_Saida)
    );
"""

criarTabelaUsuario = """
    ID_Usuario SERIAL PRIMARY KEY,
    CREATE TABLE USUARIO (
    Login VARCHAR(30),
    Senha VARCHAR(50)
    );
"""

criarTabelaDoacao = """
    CREATE TABLE DOACAO (
    ID_Doacao SERIAL PRIMARY KEY,
    DT_Doacao DATE,
    Observacao VARCHAR(50),
    ID_Pessoa  INTEGER,
    ID_Usuario INTEGER,
    FOREIGN KEY(ID_Pessoa ) REFERENCES PESSOA (ID_Pessoa),
    FOREIGN KEY(ID_Usuario) REFERENCES USUARIO (ID_Usuario)
    );
"""

criarTabelaItem = """
    CREATE TABLE ITEM (
    ID_Item SERIAL PRIMARY KEY,
    Descricao VARCHAR(100),
    Qtd INTEGER,
    ID_Tipo_Item INTEGER,
    FOREIGN KEY(ID_Tipo_Item) REFERENCES Tipo_Item (ID_Tipo_Item)
    );
"""

criarTabelaItem_doacao = """
    CREATE TABLE ITEM_DOACAO (
    QT_Item INTEGER,
    ID_Item INTEGER,
    ID_Doacao INTEGER,
    PRIMARY KEY(ID_Item,ID_Doacao),
    FOREIGN KEY(ID_Item) REFERENCES ITEM (ID_Item),
    FOREIGN KEY(ID_Doacao) REFERENCES DOACAO (ID_Doacao)
    );
"""

criarTabelaItem_saida = """
    CREATE TABLE ITEM_SAIDA (
    QT_Item INTEGER,
    ID_Saida INTEGER,
    ID_Item INTEGER,
    PRIMARY KEY(ID_Saida,ID_Item),
    FOREIGN KEY(ID_Item) REFERENCES ITEM (ID_Item),
    FOREIGN KEY(ID_Saida) REFERENCES SAIDA (ID_Saida)
    );
"""
