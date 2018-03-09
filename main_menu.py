import kivy
kivy.require('1.10.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder



class Main_Menu(App):
	
    def build(self):
        return Builder.load_file('Screens/main_menu.kv')


if __name__ == '__main__':
    Main_Menu().run()
