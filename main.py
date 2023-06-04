from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

from conexao_banco import selectUsuario, operar_pessoa


# declarando a tela de login
class LoginTela(MDScreen):
    usuario = ObjectProperty(None)
    senha = ObjectProperty(None)
    labelMensagem = ObjectProperty(None)

    def validarLogin(self):
        # recebendo os dados de login
        usuarioText = self.usuario.text
        senhaText = self.senha.text

        try:
            # pesquisando no BD o usuario
            [usuarioBD] = selectUsuario(usuarioText)

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


class TelaPrincipal(MDScreen):
    pass


class TelaEditarPessoa(MDScreen):
    pass


class TelaPessoa(MDScreen):
    editar = False
    id_pessoa_editar = 0

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
                operar_pessoa('DELETE', dados={'nome': self.nome})
                self.btnBuscar.trigger_action()
                toast("Registro deletado", duration=5)

            except Exception as e:
                toast(f"Error: {e}", duration=5)
                print(e)

        popup = ConfirmationPopup(callback=confirmar_exclusao, nome_registro=f"id: {self.id_pessoa} '{self.nome}'")
        popup.open()


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


class MyApp(MDApp):
    def build(self):
        Builder.load_file("./telas/LoginTela.kv")
        Builder.load_file("./telas/TelaPrincipal.kv")
        Builder.load_file("./telas/ConsultarPessoa.kv")
        Builder.load_file("./telas/TelaPessoa.kv")
        Builder.load_file("./telas/EditarPessoa.kv")
        Builder.load_file("./telas/Popup.kv")
        global gt
        gt = Builder.load_file("./telas/GerenciadorTelas.kv")

        return gt


gt = None
if __name__ == "__main__":
    MyApp().run()
