from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class GerenciarTelas(ScreenManager):
    pass

class TelaMenu(Screen):
    pass

class TelaGame(Screen):
    pass

class TelaGameOver(Screen):
    pass

class Aplicativo(App):
    pass

Aplicativo().run()