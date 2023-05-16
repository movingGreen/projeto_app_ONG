from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from conexao_banco import conectarBancoECursor, commitEFecharConexao, selectUsuario


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

                #self.labelMensagem.text = ""

            else:
                toast("Login ou senha inválidos", duration=10)
                print("---Acesso negado---")

                #self.labelMensagem.text = "Senha Incorreta"
        except:
            print("###Erro de BD###")
            toast("Login ou senha inválidos", duration=10)
            #self.labelMensagem.text = "Senha Incorreta"
        finally:
            commitEFecharConexao(conector)


class TelaPrincipal(MDScreen):
    pass


class TelaPessoa(MDScreen):
    pass


class GerenciadorTelas(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        return Builder.load_file("layout_app.kv")


if __name__ == "__main__":
    MyApp().run()
