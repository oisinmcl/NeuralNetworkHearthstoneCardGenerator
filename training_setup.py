import kivy
kivy.require('1.10.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.config import Config
from hs_rnn import Neural_Network

Config.read('config.ini')

class Training_Setup(FloatLayout):
	def __init__(self, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		self.builder = Builder.load_file('Screens/Training_Setup.kv')

		
class myApp(App):
	icon = 'Resources/logo_hearthstone.ico'
	title = 'Hearthstone Card Generation'
	def build(self):
		return Training_Setup().builder

if __name__ == '__main__':
     myApp().run()