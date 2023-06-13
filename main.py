from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

from conexao_banco import select_um_usuario, operar_pessoa, operar_usuario, operar_doacao, operar_item_doacao, \
    operar_item


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
        Builder.load_file("./telas/Doacao/ConsultarDoacao.kv")
        Builder.load_file("./telas/Doacao/TelaDoacao.kv")
        Builder.load_file("./telas/Doacao/DoacaoOuItemDoacao.kv")
        Builder.load_file("./telas/Doacao/ConsultarItemDoacao.kv")
        Builder.load_file("./telas/Doacao/TelaItemDoacao.kv")

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

                usuario_atual = usuarioBD
                self.manager.transition.direction = "left"
                self.manager.current = "principal"

            else:
                toast("Login ou senha inválidos", duration=10)
                print("---Acesso negado---")

        except:
            print("###Erro de BD###")
            toast("Login ou senha inválidos", duration=10)


class TelaPrincipal(MDScreen):

    def verificar_usuario(self):
        print(123)
        global usuario_atual

        if not usuario_atual[3] == 1:
            toast("Acesso permitido somente ao administrador!")
            return

        self.manager.transition.direction = 'left'
        self.manager.current = 'consultar_usuario'


class TelaItens(MDScreen):
    pass


class DoacaoOuItemDoacao(MDScreen):
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
        tela_usuario.ids['is_admin_switch'].active = False
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
                id_usuario, login, senha, is_admin = row

                if is_admin == 1:
                    is_admin = True
                else:
                    is_admin = False

                usuario_item = UsuarioListItem(id_usuario, login, senha, is_admin, btn_buscar)

                # Adicionar o item à lista
                self.ids.usuario_list.add_widget(usuario_item)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class UsuarioListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, id_usuario, login='', senha='', is_admin=False, btn_buscar=None, **kwargs):
        super(UsuarioListItem, self).__init__(**kwargs)
        self.id_usuario = id_usuario
        self.login = login
        self.senha = senha
        self.admin = is_admin
        self.texto = f"{login} | {self.admin}"
        self.btn_buscar = btn_buscar

    # metodo do botao engrenagem
    def editar(self):
        global gt

        # alterando os dados da tela usuario para os do usuario a ser editado
        tela_usuario = gt.get_screen('usuario')
        tela_usuario.ids['usuario_label'].text = 'Editar\nUsuario'
        tela_usuario.ids['usuario_login'].text = self.login
        tela_usuario.ids['usuario_login'].readonly = True
        tela_usuario.ids['is_admin_switch'].active = self.admin
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
        self.ids['is_admin_switch'].active = False
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

        if self.ids.is_admin_switch.active:
            self.admin = 1
        else:
            self.admin = 0

        operar_usuario("UPDATE", dados={
            'login': self.ids.usuario_login.text,
            'senha': self.ids.usuario_senha.text,
            'admin': self.admin,
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

        if self.ids.is_admin_switch.active:
            self.admin = 1
        else:
            self.admin = 0

        operar_usuario("INSERT", dados={
            'login': self.ids.usuario_login.text,
            'senha': self.ids.usuario_senha.text,
            'admin': self.admin
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


# --------------------- DOACAO ----------------
class ConsultarDoacao(MDScreen):
    doacao_list = ObjectProperty(None)

    def cadastrar(self):
        tela_doacao = self.manager.get_screen('tela_doacao')

        tela_doacao.ids['doacaoLabel'].text = 'Cadastrar\nDoação'
        tela_doacao.editar = False
        self.manager.transition.direction = 'left'
        self.manager.current = 'tela_doacao'

    def pesquisar(self, texto):
        try:
            print(texto)

            doacao_resposta_bd = operar_doacao('SELECT', dados={'observacao': texto.strip()})
            print(doacao_resposta_bd)

            # Limpar a lista de doacao
            self.ids.doacao_list.clear_widgets()

            btn_buscar = self.ids.button_buscar

            # Iterar sobre os resultados da consulta
            for row in doacao_resposta_bd:
                id_doacao, dt_doacao, observacao, nome, login, id_pessoa, id_usuario = row
                doacao_item = DoacaoListItem(id_doacao, dt_doacao, observacao,
                                             nome, login, id_pessoa, id_usuario, btn_buscar)

                # Adicionar o item à lista
                self.ids.doacao_list.add_widget(doacao_item)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class DoacaoListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, id_doacao, dt_doacao='', observacao='',
                 nome='', login='', id_pessoa='', id_usuario='',
                 btn_buscar=None, **kwargs):
        super(DoacaoListItem, self).__init__(**kwargs)
        self.id_doacao = id_doacao
        self.dt_doacao = dt_doacao
        self.observacao = observacao
        self.id_pessoa = id_pessoa
        self.id_usuario = id_usuario
        self.nome = nome
        self.login = login
        self.btn_buscar = btn_buscar

        self.texto = f"|obs: {observacao} |data: {dt_doacao} |pessoa: {nome}"

    # metodo do botao engrenagem
    def editar(self):
        global gt

        # alterando os dados da tela doacao para os do doacao a ser editado
        tela_doacao = gt.get_screen('tela_doacao')
        tela_doacao.ids['doacaoLabel'].text = 'Editar\nDoação'
        tela_doacao.ids['doacaoData'].text = self.dt_doacao
        tela_doacao.ids['doacaoObservacao'].text = self.observacao
        tela_doacao.ids['doacaoPessoa'].text = self.nome
        tela_doacao.editar = True
        tela_doacao.id_doacao_editar = self.id_doacao
        tela_doacao.id_pessoa = self.id_pessoa

        gt.transition.direction = 'left'
        gt.current = 'tela_doacao'

    # metodo do botao menos
    def deletar(self):
        def confirmar_exclusao_doacao():
            try:
                operar_doacao('DELETE', dados={'id_doacao': self.id_doacao})
                self.btn_buscar.trigger_action()
                toast("Registro deletado", duration=5)

            except Exception as e:
                toast(f"Error: {e}", duration=5)
                print(e)

        popup = ConfirmationPopup(
            callback=confirmar_exclusao_doacao,
            nome_registro=f"id: {self.id_doacao} '{self.observacao}'"
        )
        popup.open()


class TelaDoacao(MDScreen):
    editar = False
    id_doacao_editar = 0
    id_pessoa = 0

    def on_enter(self, *args):
        self.lista_pessoas = []
        resposta_pessoas = operar_pessoa('SELECT', dados={'nome': ''})

        # Iterar sobre os resultados da consulta
        for row in resposta_pessoas:
            id_pessoa, nome, endereco, telefone, email = row

            list_item_pessoa = {
                "viewclass": "OneLineListItem",
                "text": f"{id_pessoa} | {nome}",
                "on_release": lambda x=[id_pessoa, nome]: self.definir_pessoa(x)
            }

            self.lista_pessoas.append(list_item_pessoa)

    def dropdown_lista_pessoas(self):
        self.dropdown_pessoas = MDDropdownMenu(
            caller = self.ids.pesquisar_pessoa,
            items = self.lista_pessoas,
            width_mult = 4
        )
        self.dropdown_pessoas.open()

    def definir_pessoa(self, dados_pessoa):
        [id_pessoa, nome] = dados_pessoa
        self.id_pessoa = id_pessoa
        self.ids['doacaoPessoa'].text = nome

    def on_leave(self):
        self.ids['doacaoData'].text = ''
        self.ids['doacaoObservacao'].text = ''
        self.ids['doacaoPessoa'].text = ''
        self.id_doacao_editar = 0
        self.id_pessoa = 0

    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_doacao"

    def salvar_ou_editar_dados(self):
        if self.editar:
            self.editar_dados()
        else:
            self.salvar_dados()

    def editar_dados(self):
        print(
            'Atualizando:',
            self.ids.doacaoObservacao.text
        )

        operar_doacao("UPDATE", dados={
            'dt_doacao': self.ids['doacaoData'].text,
            'observacao': self.ids['doacaoObservacao'].text,
            'id_doacao': self.id_doacao_editar,
            'id_pessoa': self.id_pessoa
        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_doacao"

    def salvar_dados(self):
        global usuario_atual

        print(
            'Salvando:',
            self.ids.doacaoObservacao.text,
            self.ids.doacaoData.text
        )

        operar_doacao("INSERT", dados={
            'dt_doacao': self.ids['doacaoData'].text,
            'observacao': self.ids['doacaoObservacao'].text,
            'id_pessoa': self.id_pessoa,
            'id_usuario': usuario_atual[0]

        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_doacao"

# ---------------------------------------------


# --------------------- ITEM DOACAO ----------------
class ConsultarItemDoacao(MDScreen):
    scroll_list_registros = ObjectProperty(None)

    def cadastrar(self):
        tela_item_doacao = self.manager.get_screen('tela_item_doacao')

        tela_item_doacao.ids['itemDoacaoLabel'].text = 'Cadastrar\nItem Doacao'
        tela_item_doacao.editar = False
        self.manager.transition.direction = 'left'
        self.manager.current = 'tela_item_doacao'

    def pesquisar(self, texto):
        try:
            print(texto)

            item_doacao_resposta_bd = operar_item_doacao('SELECT', {})
            print(item_doacao_resposta_bd)

            # Limpar a lista de doacao
            self.ids.scroll_list_registros.clear_widgets()

            btn_buscar = self.ids.button_buscar

            # Iterar sobre os resultados da consulta
            for row in item_doacao_resposta_bd:
                qt_item, id_item, id_doacao = row

                item = operar_item('SELECT', {'id_item': id_item})
                doacao = operar_doacao('SELECT', {'id_doacao': id_doacao})

                item_registro = ItemDoacaoListItem(qt_item, id_item, item[0][1], id_doacao, doacao[0][2], btn_buscar)

                # Adicionar o item à lista
                self.ids.scroll_list_registros.add_widget(item_registro)

        except Exception as e:
            toast(f"Error: {e}", duration=5)
            print(e)


class ItemDoacaoListItem(OneLineAvatarIconListItem, EventDispatcher):
    texto = StringProperty('')

    def __init__(self, qt_item, id_item, descricao_item, id_doacao, obs_doacao, btn_buscar, **kwargs):
        super(ItemDoacaoListItem, self).__init__(**kwargs)
        self.qt_item = qt_item
        self.id_item = id_item
        self.descricao_item = descricao_item
        self.id_doacao = id_doacao
        self.obs_doacao = obs_doacao
        self.btn_buscar = btn_buscar

        self.texto = f"|quantidade: {qt_item} |item: {id_item} {self.descricao_item}|doacao: {obs_doacao}"

    # metodo do botao engrenagem
    def editar(self):
        global gt

        # alterando os dados da tela doacao para os do doacao a ser editado
        tela_item_doacao = gt.get_screen('tela_item_doacao')
        tela_item_doacao.ids['itemDoacaoLabel'].text = 'Editar\nItem Doação'
        tela_item_doacao.ids['quantidadeItem'].text = f'{self.qt_item}'
        tela_item_doacao.ids['nomeItem'].text = self.descricao_item
        tela_item_doacao.ids['obsDoacao'].text = self.obs_doacao
        tela_item_doacao.editar = True
        tela_item_doacao.id_item = self.id_item
        tela_item_doacao.id_doacao = self.id_doacao
        tela_item_doacao.id_item_antes_edicao = self.id_item
        tela_item_doacao.id_doacao_antes_edicao = self.id_doacao

        gt.transition.direction = 'left'
        gt.current = 'tela_item_doacao'

    # metodo do botao menos
    def deletar(self):
        def confirmar_exclusao_registro():
            try:
                operar_item_doacao('DELETE', dados={'id_doacao': self.id_doacao, 'id_item': self.id_item})
                self.btn_buscar.trigger_action()
                toast("Registro deletado", duration=5)

            except Exception as e:
                toast(f"Error: {e}", duration=5)
                print(e)

        popup = ConfirmationPopup(
            callback=confirmar_exclusao_registro,
            nome_registro=f"id_item: {self.id_item} | id_doacao: {self.id_doacao}"
        )
        popup.open()


class TelaItemDoacao(MDScreen):
    editar = False
    id_item_antes_edicao = 0
    id_doacao_antes_edicao = 0
    id_item = 0
    id_doacao = 0

    def on_enter(self, *args):
        self.lista_item = []
        self.lista_doacao = []

        resposta_item = operar_item('SELECT', dados={'descricao': ''})
        resposta_doacao = operar_doacao('SELECT', dados={'observacao': ''})

        # Iterar sobre os resultados da consulta
        for row in resposta_item:
            id_item, descricao, *_ = row

            list_item = {
                "viewclass": "OneLineListItem",
                "text": f"{id_item} | {descricao}",
                "on_release": lambda x=[id_item, descricao]: self.definir_item(x)
            }

            self.lista_item.append(list_item)

        # Iterar sobre os resultados da consulta
        for row in resposta_doacao:
            id_doacao, _, observacao, *_ = row

            list_doacao = {
                "viewclass": "OneLineListItem",
                "text": f"{id_doacao} | {observacao}",
                "on_release": lambda x=[id_doacao, observacao]: self.definir_doacao(x)
            }

            self.lista_doacao.append(list_doacao)

    def dropdown_lista_item(self):
        self.dropdown_item = MDDropdownMenu(
            caller = self.ids.pesquisarItem,
            items = self.lista_item,
            width_mult = 4
        )
        self.dropdown_item.open()

    def dropdown_lista_doacao(self):
        self.dropdown_doacao = MDDropdownMenu(
            caller = self.ids.pesquisarDoacao,
            items = self.lista_doacao,
            width_mult = 4
        )
        self.dropdown_doacao.open()

    def definir_item(self, dados_item):
        [id_item, descricao] = dados_item
        self.id_item = id_item
        self.ids['nomeItem'].text = descricao

    def definir_doacao(self, dados_doacao):
        [id_doacao, observacao] = dados_doacao
        self.id_doacao = id_doacao
        self.ids['obsDoacao'].text = observacao

    def on_leave(self):
        self.ids['quantidadeItem'].text = ''
        self.ids['nomeItem'].text = ''
        self.ids['obsDoacao'].text = ''
        self.id_item = 0
        self.id_doacao = 0

    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_item_doacao"

    def salvar_ou_editar_dados(self):
        if self.editar:
            self.editar_dados()
        else:
            self.salvar_dados()

    def editar_dados(self):
        print(
            'Atualizando:',
            self.id_item,
            self.id_doacao
        )

        operar_item_doacao("UPDATE", dados={
            'qt_item': self.ids['quantidadeItem'].text,
            'id_item': self.id_item,
            'id_doacao': self.id_doacao,
            'id_item_antes_edicao': self.id_item_antes_edicao,
            'id_doacao_antes_edicao': self.id_doacao_antes_edicao
        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_item_doacao"

    def salvar_dados(self):
        print(
            'Salvando:',
            self.id_item,
            self.id_doacao
        )

        operar_item_doacao("INSERT", dados={
            'qt_item': self.ids['quantidadeItem'].text,
            'id_item': self.id_item,
            'id_doacao': self.id_doacao
        })

        self.manager.transition.direction = 'right'
        self.manager.current = "consultar_item_doacao"

# ---------------------------------------------



usuario_atual = [1, 'admin', '123', 1]
gt = None
if __name__ == "__main__":
    MyApp().run()
