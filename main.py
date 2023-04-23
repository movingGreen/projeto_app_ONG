from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from conexao_banco import conectarBancoECursor, commitEFecharConexao, selectUsuario

# declarando a tela de login
class LoginTela(Screen):
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
            
            if (senhaText == usuarioBD[2]):
                print("---Acesso permitido---")
                self.labelMensagem.text = ""
                self.manager.current = "principal"
            else:
                print("---Acesso negado---")
                self.labelMensagem.text = "Senha Incorreta"
        except:
            print("###Erro de BD###")
            self.labelMensagem.text = "Senha Incorreta"
        finally: 
            commitEFecharConexao(conector)    


class TelaPrincipal(Screen):
    pass

class GerenciadorTelas(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        return Builder.load_file("layout_app.kv")
    
if __name__ == "__main__":
    MyApp().run()