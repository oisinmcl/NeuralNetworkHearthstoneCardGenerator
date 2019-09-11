import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty,ObjectProperty

from UI.CustomWidgets import HSConfirmPopup


import logging
import threading

# create logger
module_logger = logging.getLogger('myApp')


class TrainingStats(Screen):

			   
	def __init__(self, _nn, **kwargs): 
		super(TrainingStats, self).__init__(**kwargs)
		
		self.nn = _nn
		self.statusString = ""
		self.popup = HSConfirmPopup()
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)
		self.statusString = ""
		
		module_logger.info('Creating new thread for training')
		#event from button, starts new thread for StartTraining function
		thread = threading.Thread(target=self.StartTraining, args=())
		#thread.daemon = True # Daemonize thread
		thread.start()
		
	def StartTraining(self):
		module_logger.info('Training Thread Started')
		self.nn.startTraining()
		self.popup.show('Success', 'Training Complete')
		
	def btnStopTraining(self, button):
		module_logger.info('Training Cancelled')
		self.nn.setStopTrainingFlag()
		self.manager.current = 'MainMenu'