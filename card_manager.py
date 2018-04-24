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
	
	frameSource = StringProperty()
	raritySource = StringProperty()
	manaSource = StringProperty()
	healthSource = StringProperty()
	attackSource = StringProperty()
	bannerSource = StringProperty()
	raceBannerSource = StringProperty()
	legendaryDragonSource = StringProperty()
			   
	def __init__(self, **kwargs): 
		super(Card_Manager, self).__init__(**kwargs)
		
		self.db = Database_Manager()
		
		self.cardFile = 'test'
		
		#default values for card assets
		self.frameSource = 'Resources/card_assets/frame-minion-neutral.png'
		self.raritySource = 'Resources/card_assets/rarity-minion-legendary.png'
		self.manaSource = 'Resources/card_assets/cost-mana.png'
		self.healthSource = 'Resources/card_assets/cost-health.png'
		self.attackSource = 'Resources/card_assets/attack-minion.png'
		self.bannerSource = 'Resources/card_assets/name-banner-minion.png'
		self.raceBannerSource = 'Resources/card_assets/race-banner.png'
		self.legendaryDragonSource = 'Resources/card_assets/elite-minion.png'
		
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
			