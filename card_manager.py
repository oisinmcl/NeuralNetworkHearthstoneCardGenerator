import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty,ObjectProperty

from database_manager import Database_Manager
from CustomWidgets import HSConfirmPopup, HSFileChooserPopup

import logging
import threading
import json

# create logger
module_logger = logging.getLogger('myApp')


class Card_Manager(Screen):

	cardFile = StringProperty()
	numOfCards = StringProperty()
	
	#imgs for card art
	frameSource = StringProperty()
	raritySource = StringProperty()
	manaSource = StringProperty()
	healthSource = StringProperty()
	attackSource = StringProperty()
	bannerSource = StringProperty()
	raceBannerSource = StringProperty()
	legendaryDragonSource = StringProperty()
	
	#card values
	cardTextSource = StringProperty()
	manaValueSource = StringProperty()
	attackValueSource = StringProperty()
	healthValueSource = StringProperty()
	nameSource = StringProperty()
	
			   
	def __init__(self, **kwargs): 
		super(Card_Manager, self).__init__(**kwargs)
		
		self.db = Database_Manager()
		self.popup = HSConfirmPopup()
		
		
		
		#default values for card assets
		self.transparent = 'Resources/card_assets/transparent.png'
		self.frameSource = 'Resources/card_assets/frame-minion-neutral.png'
		self.raritySource = 'Resources/card_assets/rarity-minion-legendary.png'
		self.manaSource = 'Resources/card_assets/cost-mana.png'
		self.healthSource = 'Resources/card_assets/cost-health.png'
		self.attackSource = 'Resources/card_assets/attack-minion.png'
		self.bannerSource = 'Resources/card_assets/name-banner-minion.png'
		self.raceBannerSource = 'Resources/card_assets/race-banner.png'
		self.cardTextSource = 'Resources/card_assets/elite-minion.png'
		self.legendaryDragonSource = 'Resources/card_assets/elite-minion.png'
		self.cardTextSource = 'Test Text'
		self.manaValueSource = ''

		self.cardFile = 'Output_data\output_1525082192.txt'
		self.currentArray = json.load(open(self.cardFile))
		self.currentCardNum = 0
		self.currentCard = self.currentArray[self.currentCardNum]		
		self.numOfCards = str(len(self.currentArray))
		
		#self.loadJSON()

		
		
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
		
	def loadJSON(self):
		try:
			self.cardFile = 'Output_data/testCard.txt'
			self.currentArray = json.load(open(self.cardFile))
			self.currentCardNum = 0
			self.currentCard = self.currentArray[self.currentCardNum]
			self.updateCard()   
		except:
			self.popup.show('Error', "Error loading JSON")
		
	def updateCard(self):
		try:
			self.currentCard = self.currentArray[self.currentCardNum]
			
			try:
				self.frameSource = 'Resources/card_assets/frame-'+self.currentCard['type']+'-'+self.currentCard['cardClass']+'.png'
			except:	
				self.frameSource = 'Resources/card_assets/frame-minion-neutral.png'
			
			try:
				self.raritySource = 'Resources/card_assets/rarity-minion-'+self.currentCard['rarity']+ '.png'
			except:
				self.raritySource =  'Resources/card_assets/rarity-minion-common.png'
							
			try:
				self.nameSource = str(self.currentCard['name'])
			except:
				self.nameSource = "no name"
				
			try:
				self.cardTextSource = self.currentCard['text']
			except:
				self.cardTextSource = ""
				
			try:
				self.manaValueSource = str(self.currentCard['cost'])
			except:
				self.manaValueSource = "0"
				
			try:
				self.attackValueSource = str(self.currentCard['attack'])
			except:
				self.attackValueSource = "0"
							
			try:
				self.healthValueSource = str(self.currentCard['health'])
			except:
				self.healthValueSource = "0"					

			if(self.currentCard['rarity'].upper() == 'LEGENDARY'):
				self.legendaryDragonSource = 'Resources/card_assets/elite-minion.png'
			else:
				self.legendaryDragonSource = self.transparent	
			
			if(self.currentCard['type'].upper() != 'MINION'):
				self.healthSource = self.transparent	
				self.attackSource = self.transparent
				self.attackValueSource = ""
				self.healthValueSource = ""			
			else:
				self.healthSource = 'Resources/card_assets/cost-health.png'
				self.attackSource = 'Resources/card_assets/attack-minion.png'
		except:
			self.popup.show('Error', "Error Rendering Current Card")
			
	def btnIncCardNum(self, button):
		if (self.currentCardNum < len(self.currentArray)-1): 
			self.currentCardNum+=1
			self.updateCard()
		
	def btnDecCardNum(self, button):
		if (self.currentCardNum > 0): 
			self.currentCardNum-=1
			self.updateCard()	