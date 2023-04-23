from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginTela(Screen):
    def validarLogin(self):
        
        """
        app.root.current = "principal"
                    root.manager.transition.direction = "left"
        """
        
        pass
    
    
    pass

class TelaPrincipal(Screen):
    pass

class GerenciadorTelas(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        return Builder.load_file("layout_app.kv")
    
if __name__ == "__main__":
    MyApp().run()