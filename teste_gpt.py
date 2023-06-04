from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class Screen1(Screen):
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Digite algo:')
        self.input = TextInput()
        self.button = Button(text='Enviar', on_press=self.send_data)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def send_data(self, instance):
        data = self.input.text
        # Acessa o gerenciador de tela e troca para a próxima tela
        # self.manager.get_screen('screen2').update_label(data)
        self.manager.get_screen('screen2').ids['teste123'].text = data
        self.manager.current = 'screen2'


class Screen2(Screen):
    def __init__(self, **kwargs):
        super(Screen2, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Dado recebido:')
        self.output = Label(text='')
        self.ids['teste123'] = self.output
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.output)
        self.add_widget(self.layout)

    def update_label(self, data):
        self.output.text = data


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen1(name='screen1'))
        sm.add_widget(Screen2(name='screen2'))
        return sm


if __name__ == '__main__':
    MyApp().run()
