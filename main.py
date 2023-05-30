from kivy.event import EventDispatcher
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

from conexao_banco import conectarBancoECursor, commitEFecharConexao, selectUsuario, operar_pessoa


# declarando a tela de login
class LoginTela(MDScreen):
    usuario = ObjectProperty(None)
    senha = ObjectProperty(None)
    labelMensagem = ObjectProperty(None)

    def validarLogin(self):
        # recebendo os dados de login
        usuarioText = self.usuario.text
        senhaText = self.senha.text

        # conectando com o banco de dados
        conector, cursor = conectarBancoECursor()
        try:
            # pesquisando no BD o usuario
            [usuarioBD] = selectUsuario(cursor, usuarioText)

            if senhaText == usuarioBD[2]:
                print("---Acesso permitido---")

                self.manager.transition.direction = "left"
                self.manager.current = "principal"

                # self.labelMensagem.text = ""

            else:
                toast("Login ou senha inválidos", duration=10)
                print("---Acesso negado---")

                # self.labelMensagem.text = "Senha Incorreta"
        except:
            print("###Erro de BD###")
            toast("Login ou senha inválidos", duration=10)
            # self.labelMensagem.text = "Senha Incorreta"
        finally:
            commitEFecharConexao(conector)


class TelaPrincipal(MDScreen):
    pass


class TelaEditarPessoa(MDScreen):
    pass


class TelaPessoa(MDScreen):

    def salvar_dados(self, idNome, idEndereco, idTelefone, idEmail):
        print(idNome.text, idEndereco.text, idTelefone.text, idEmail.text)

        [conn, cursor] = conectarBancoECursor()
        operar_pessoa(cursor, "INSERT", dados={
            'nome': idNome.text,
            'endereco': idEndereco.text,
            'telefone': idTelefone.text,
            'email': idEmail.text
        })
        commitEFecharConexao(conn)

        idNome.text = ''
        idEndereco.text = ''
        idTelefone.text = ''
        idEmail.text = ''

    def focus_save_button(self):
        self.ids.salvar_button.focus = True


class PessoaListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, nome='', endereco='', telefone='', email='', btnBuscar=None, **kwargs):
        super(PessoaListItem, self).__init__(**kwargs)
        # self.id_pessoa = id_pessoa
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.texto = f"{nome} | {endereco} | {telefone} | {email}"
        self.btnBuscar = btnBuscar

    def deletar(self):

        try:
            con, cursor = conectarBancoECursor()
            operar_pessoa(cursor, 'DELETE', dados={'nome': self.nome})
            commitEFecharConexao(con)
            self.btnBuscar.trigger_action()
            toast("Registro deletado", duration=5)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class ConsultarPessoa(MDScreen):
    pessoa_list = ObjectProperty(None)

    def pesquisar(self, texto):
        try:
            [conn, cursor] = conectarBancoECursor()
            print(texto)

            lista_pessoas = operar_pessoa(cursor, 'SELECT', dados={'nome': texto.strip()})
            print(lista_pessoas)

            # Limpar a lista de pessoas
            self.ids.pessoa_list.clear_widgets()

            btnBuscar = self.ids.button_buscar

            # Iterar sobre os resultados da consulta
            for row in lista_pessoas:
                id_pessoa, nome, endereco, telefone, email = row

                print('Nome:', nome)

                pessoa_item = PessoaListItem(nome, endereco, telefone, email, btnBuscar)

                # Adicionar o item à lista
                self.ids.pessoa_list.add_widget(pessoa_item)

            # Fechar a conexão com o banco de dados
            commitEFecharConexao(conn)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)

    pass


class GerenciadorTelas(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        Builder.load_file("./telas/LoginTela.kv")
        Builder.load_file("./telas/TelaPrincipal.kv")
        Builder.load_file("./telas/ConsultarPessoa.kv")
        Builder.load_file("./telas/TelaPessoa.kv")

        return Builder.load_file("./telas/GerenciadorTelas.kv")


if __name__ == "__main__":
    MyApp().run()
