import kivy
kivy.require('1.10.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config

from NeuralNetwork.NeuralNetwork import NeuralNetwork

#screen classes
from UI.MainMenu import MainMenu
from UI.TrainingSetup import TrainingSetup
from UI.GenerateSetup import GenerateSetup
from UI.CardManager import CardManager
from UI.TrainingStats import TrainingStats
from UI.Help import Help

import logging
import datetime



# create logger with 'myApp'
logger = logging.getLogger('myApp')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log/log_' + str(datetime.datetime.now().date()) + '.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('*****************Appication started*****************')

#app specific config
Config.read('config.ini')
Builder.load_file('UI/Screens/main.kv')

sm = ScreenManager()
		
		
class myApp(App):
	icon = 'Resources/logo_hearthstone.ico'
	title = 'Hearthstone Card Generation'
	
	nn = NeuralNetwork()
	
	mainMenu = MainMenu()
	trainingSetup = TrainingSetup(nn)
	generateSetup = GenerateSetup(nn)
	cardManager = CardManager()
	help = Help()
	trainingStats = TrainingStats(nn)
	
	sm.add_widget(mainMenu)
	sm.add_widget(trainingSetup)
	sm.add_widget(generateSetup)
	sm.add_widget(cardManager)
	sm.add_widget(help)	
	sm.add_widget(trainingStats)	
	
	def build(self):
		logger.info('Application Building')
		return sm
		
	def on_stop(self):
		logger.info('*****************Application Closed*****************')

if __name__ == '__main__':
	myApp().run()
	 