from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

from conexao_banco import select_um_usuario, operar_pessoa, operar_usuario


class MyApp(MDApp):
    def build(self):
        global gt

        Builder.load_file("./telas/LoginTela.kv")
        Builder.load_file("./telas/TelaPrincipal.kv")
        Builder.load_file("./telas/Pessoa/ConsultarPessoa.kv")
        Builder.load_file("./telas/Pessoa/TelaPessoa.kv")
        Builder.load_file("./telas/Popup.kv")
        Builder.load_file("./telas/Usuario/ConsultarUsuario.kv")
        Builder.load_file("./telas/Usuario/TelaUsuario.kv")
        Builder.load_file("./telas/Item/TelaItens.kv")

        gt = Builder.load_file("./telas/GerenciadorTelas.kv")

        return gt


class ConfirmationPopup(Popup):
    texto_popup = ObjectProperty()

    def __init__(self, callback, nome_registro,  **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)
        self.callback = callback
        self.ids.texto_popup.text = f"Deseja mesmo excluir o registro {nome_registro}?"

    def confirm(self):
        self.callback()
        self.dismiss()


class GerenciadorTelas(ScreenManager):
    pass


# declarando a tela de login
class LoginTela(MDScreen):
    usuario = ObjectProperty(None)
    senha = ObjectProperty(None)
    labelMensagem = ObjectProperty(None)

    def validarLogin(self):
        global usuario_atual

        # recebendo os dados de login
        usuarioText = self.usuario.text
        senhaText = self.senha.text

        try:
            # pesquisando no BD o usuario
            [usuarioBD] = select_um_usuario(usuarioText)

            if senhaText == usuarioBD[2]:
                print("---Acesso permitido---")

                usuario_atual = usuarioText
                self.manager.transition.direction = "left"
                self.manager.current = "principal"

            else:
                toast("Login ou senha inválidos", duration=10)
                print("---Acesso negado---")

                # self.labelMensagem.text = "Senha Incorreta"
        except:
            print("###Erro de BD###")
            toast("Login ou senha inválidos", duration=10)
            # self.labelMensagem.text = "Senha Incorreta"


class TelaPrincipal(MDScreen):

    def verificar_usuario(self):
        print(123)
        global usuario_atual

        if not usuario_atual == 'admin':
            toast("Acesso permitido somente ao administrador!")
            return

        self.manager.transition.direction = 'left'
        self.manager.current = 'consultar_usuario'


class TelaItens(MDScreen):
    pass

# ------------------ PESSOA ----------------
class TelaPessoa(MDScreen):
    editar = False
    id_pessoa_editar = 0

    def voltar(self):
        self.ids.pessoaNome.text = ''
        self.ids.pessoaEndereco.text = ''
        self.ids.pessoaTelefone.text = ''
        self.ids.pessoaEmail.text = ''
        self.id_pessoa_editar = 0

        self.manager.transition.direction = 'right'
        self.manager.current = "lista_pessoa"

    def salvar_ou_editar_dados(self):
        if self.editar:
            self.editar_dados()
        else:
            self.salvar_dados()

    def editar_dados(self):
        print('Salvando:', self.ids.pessoaNome.text, self.ids.pessoaEndereco.text, self.ids.pessoaTelefone.text,
              self.ids.pessoaEmail.text)

        operar_pessoa("UPDATE", dados={
            'nome': self.ids.pessoaNome.text,
            'endereco': self.ids.pessoaEndereco.text,
            'telefone': self.ids.pessoaTelefone.text,
            'email': self.ids.pessoaEmail.text,
            'id_pessoa': self.id_pessoa_editar
        })

        self.ids.pessoaNome.text = ''
        self.ids.pessoaEndereco.text = ''
        self.ids.pessoaTelefone.text = ''
        self.ids.pessoaEmail.text = ''
        self.id_pessoa_editar = 0

        self.manager.transition.direction = 'right'
        self.manager.current = "lista_pessoa"

    def salvar_dados(self):
        print('Salvando:', self.ids.pessoaNome.text, self.ids.pessoaEndereco.text, self.ids.pessoaTelefone.text, self.ids.pessoaEmail.text)

        operar_pessoa("INSERT", dados={
            'nome': self.ids.pessoaNome.text,
            'endereco': self.ids.pessoaEndereco.text,
            'telefone': self.ids.pessoaTelefone.text,
            'email': self.ids.pessoaEmail.text
        })

        self.ids.pessoaNome.text = ''
        self.ids.pessoaEndereco.text = ''
        self.ids.pessoaTelefone.text = ''
        self.ids.pessoaEmail.text = ''

        self.manager.transition.direction = 'right'
        self.manager.current = "lista_pessoa"


class ConsultarPessoa(MDScreen):
    pessoa_list = ObjectProperty(None)

    def cadastrar(self):
        tela_pessoa = self.manager.get_screen('pessoa')

        tela_pessoa.ids['pessoaLabel'].text = 'Cadastrar\nPessoa'
        tela_pessoa.editar = False
        self.manager.transition.direction = 'left'
        self.manager.current = 'pessoa'


    def pesquisar(self, texto):
        try:
            print(texto)

            lista_pessoas = operar_pessoa('SELECT', dados={'nome': texto.strip()})
            print(lista_pessoas)

            # Limpar a lista de pessoas
            self.ids.pessoa_list.clear_widgets()

            btnBuscar = self.ids.button_buscar

            # Iterar sobre os resultados da consulta
            for row in lista_pessoas:
                id_pessoa, nome, endereco, telefone, email = row
                pessoa_item = PessoaListItem(id_pessoa, nome, endereco, telefone, email, btnBuscar)

                # Adicionar o item à lista
                self.ids.pessoa_list.add_widget(pessoa_item)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class PessoaListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, id_pessoa, nome='', endereco='', telefone='', email='', btnBuscar=None, **kwargs):
        super(PessoaListItem, self).__init__(**kwargs)
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.texto = f"{nome} | {endereco} | {telefone} | {email}"
        self.btnBuscar = btnBuscar

    def editar(self):
        global gt

        # alterando os dados da tela pessoa para os da pessoa a ser editada
        tela_pessoa = gt.get_screen('pessoa')
        tela_pessoa.ids['pessoaLabel'].text = 'Editar\nPessoa'
        tela_pessoa.ids['pessoaNome'].text = self.nome
        tela_pessoa.ids['pessoaEndereco'].text = self.endereco
        tela_pessoa.ids['pessoaTelefone'].text = self.telefone
        tela_pessoa.ids['pessoaEmail'].text = self.email
        tela_pessoa.editar = True
        tela_pessoa.id_pessoa_editar = self.id_pessoa

        gt.transition.direction = 'left'
        gt.current = 'pessoa'

    def deletar(self):
        def confirmar_exclusao():
            try:
                operar_pessoa('DELETE', dados={'id_pessoa': self.id_pessoa})
                self.btnBuscar.trigger_action()
                toast("Registro deletado", duration=5)

            except Exception as e:
                toast(f"Error: {e}", duration=5)
                print(e)

        popup = ConfirmationPopup(callback=confirmar_exclusao, nome_registro=f"id: {self.id_pessoa} '{self.nome}'")
        popup.open()
# ---------------------


# --------------------- USUARIO ----------------
class ConsultarUsuario(MDScreen):
    usuario_list = ObjectProperty(None)

    def cadastrar(self):
        tela_usuario = self.manager.get_screen('usuario')

        tela_usuario.ids['usuario_label'].text = 'Cadastrar\nPessoa'
        tela_usuario.ids['usuario_login'].readonly = False
        tela_usuario.editar = False
        self.manager.transition.direction = 'left'
        self.manager.current = 'usuario'

    def pesquisar(self, texto):
        try:
            print(texto)

            lista_usuario = operar_usuario('SELECT', dados={'login': texto.strip()})
            print(lista_usuario)

            # Limpar a lista de usuarios
            self.ids.usuario_list.clear_widgets()

            btn_buscar = self.ids.button_buscar

            # Iterar sobre os resultados da consulta
            for row in lista_usuario:
                id_usuario, login, senha = row
                usuario_item = UsuarioListItem(id_usuario, login, senha, btn_buscar)

                # Adicionar o item à lista
                self.ids.usuario_list.add_widget(usuario_item)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class UsuarioListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, id_usuario, login='', senha='', btn_buscar=None, **kwargs):
        super(UsuarioListItem, self).__init__(**kwargs)
        self.id_usuario = id_usuario
        self.login = login
        self.senha = senha
        self.texto = f"{login} |"
        self.btn_buscar = btn_buscar

    # metodo do botao engrenagem
    def editar(self):
        global gt

        # alterando os dados da tela usuario para os do usuario a ser editado
        tela_usuario = gt.get_screen('usuario')
        tela_usuario.ids['usuario_label'].text = 'Editar\nUsuario'
        tela_usuario.ids['usuario_login'].text = self.login
        tela_usuario.ids['usuario_login'].readonly = True
        tela_usuario.editar = True
        tela_usuario.id_usuario_editar = self.id_usuario

        gt.transition.direction = 'left'
        gt.current = 'usuario'

    # metodo do botao menos
    def deletar(self):
        def confirmar_exclusao_usuario():
            try:
                operar_usuario('DELETE', dados={'id_usuario': self.id_usuario})
                self.btn_buscar.trigger_action()
                toast("Registro deletado", duration=5)

            except Exception as e:
                toast(f"Error: {e}", duration=5)
                print(e)

        popup = ConfirmationPopup(
            callback=confirmar_exclusao_usuario,
            nome_registro=f"id: {self.id_usuario} '{self.login}'"
        )
        popup.open()


class TelaUsuario(MDScreen):
    editar = False
    id_usuario_editar = 0

    def on_leave(self):
        self.ids['usuario_login'].text = ''
        self.ids['usuario_senha'].text = ''
        self.ids['usuario_senha_confirmar'].text = ''
        self.id_usuario_editar = 0

    def voltar(self):

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_usuario"

    def salvar_ou_editar_dados(self):
        if self.editar:
            self.editar_dados()
        else:
            self.salvar_dados()

    def editar_dados(self):
        if not self.validar_senha(self.ids.usuario_senha.text, self.ids.usuario_senha_confirmar.text):
            return

        print(
            'Atualizando:',
            self.ids.usuario_login.text,
            self.ids.usuario_senha.text
        )

        operar_usuario("UPDATE", dados={
            'login': self.ids.usuario_login.text,
            'senha': self.ids.usuario_senha.text,
            'id_usuario': self.id_usuario_editar
        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_usuario"

    def salvar_dados(self):
        if not self.validar_senha(self.ids.usuario_senha.text, self.ids.usuario_senha_confirmar.text):
            return

        print(
            'Salvando:',
            self.ids.usuario_login.text,
            self.ids.usuario_senha.text
        )

        operar_usuario("INSERT", dados={
            'login': self.ids.usuario_login.text,
            'senha': self.ids.usuario_senha.text
        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_usuario"

    def validar_senha(self, senha, confirmar_senha):
        senha = senha.strip()
        confirmar_senha = confirmar_senha.strip()

        if senha != confirmar_senha:
            toast("Senhas devem ser iguais!")
            return False

        if not senha:
            toast("Senha inválida!")
            return False

        return True

# ---------------------------------------------




usuario_atual = ''
gt = None
if __name__ == "__main__":
    MyApp().run()
