import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty,ObjectProperty

from database_manager import Database_Manager

import logging
import threading

# create logger
module_logger = logging.getLogger('myApp')


class Card_Manager(Screen):

	cardFile = StringProperty()
	cardCanvas = ObjectProperty()
	
			   
	def __init__(self, **kwargs): 
		super(Card_Manager, self).__init__(**kwargs)
		
		self.db = Database_Manager()
		
		self.frame_minion_neutral = Image(source='Resources\card_assets\frame-minion-neutral.png')
		self.cardFile = 'none'
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)
		
		#self.cardCanvas.add_widget(self.frame_minion_neutral)


	def changeCardFile(self, text):
		print('change card file')
		
	def showChangeCardChooser(self):
		print('showChangeCardChooser')
		
	def getCardsFromDB(self):
		self.db.get()
	
	def btnGetCardsFromDB(self, button):
		module_logger.info('Creating new thread for getting cards from firebase')
		#event from button, starts new thread for StartGenerating function
		thread = threading.Thread(target=self.getCardsFromDB, args=())
		#thread.daemon = True # Daemonize thread
		thread.start()