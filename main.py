import kivy
kivy.require('1.10.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config

from hs_rnn import Neural_Network

#screen classes
from main_menu import Main_Menu
from training_setup import Training_Setup
from generate_setup import Generate_Setup
from card_manager import Card_Manager

Config.read('config.ini')
Builder.load_file('Screens/main.kv')

sm = ScreenManager()
		
		
class myApp(App):
	icon = 'Resources/logo_hearthstone.ico'
	title = 'Hearthstone Card Generation'
	
	nn = Neural_Network()
	
	mainMenu = Main_Menu()
	trainingSetup = Training_Setup(nn)
	generateSetup = Generate_Setup(nn)
	cardManager = Card_Manager()
	
	
	sm.add_widget(mainMenu)
	sm.add_widget(trainingSetup)
	sm.add_widget(generateSetup)
	sm.add_widget(cardManager)
		
	
	def build(self):
		return sm
		


if __name__ == '__main__':
     myApp().run()
	 