import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from hs_rnn import Neural_Network
from CustomWidgets import HSConfirmPopup, HSFileChooserPopup

import threading
import os
import logging

# create logger
module_logger = logging.getLogger('myApp')

class Training_Setup(Screen):
	nLayers = StringProperty()
	internalSize = StringProperty()
	learningRate = StringProperty()
	epochs = StringProperty()
	
	dataPath = StringProperty()
	
			   
	def __init__(self, _nn, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		#module_logger.info('Training_Setup Initialized')
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		self.internalSize = str(self.nn.internalSize)
		self.learningRate = str(self.nn.learningRate)
		self.epochs = str(self.nn.epochs)
		self.popup = HSConfirmPopup()
		self.dataPath = str(self.nn.trainingDataPath)
		
		#self.dirPicker = HSFileChooserPopup()
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)

	def nLayersChange(self, button):
		#updates nlayers var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try:
				if not self.nn.nLayers == int(button.text):
					self.nn.nLayers = int(button.text)
					module_logger.info('nLayers value changed to: ' + str(self.nn.nLayers))
			except ValueError:
				self.popup.show('Error', "Invalid data in nLayers")
			except:
				self.popup.show('Error', "An unexpected error in nLayers")

	def internalSizeChange(self, button):
		#updates internalSize var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try: 
				if not self.nn.internalSize == int(button.text):
					self.nn.internalSize = int(button.text)
					module_logger.info('internalSize value changed to: ' + str(self.nn.internalSize))
			except ValueError:
				self.popup.show('Error', "Invalid data in internalSize")
			except:
				self.popup.show('Error', "An unexpected error in internalSize")
				
	def learningRateChange(self, button):
		#updates learningRate var in nn to text input value
		button.enforce_float(button)
		if len(button.text) > 0:
			try: 
				if not self.nn.learningRate == float(button.text):
					self.nn.learningRate = float(button.text)
					module_logger.info('learningRate value changed to: ' + str(self.nn.learningRate))
			except ValueError:
				self.popup.show('Error', "Invalid data in learningRate")
			except:
				self.popup.show('Error', "An unexpected error updating learningRate value")
				
	def epochsChange(self, button):
		#updates epochs var in nn to text input value
		if len(button.text) > 0:
			try: 
				button.enforce_int(button)
				if not self.nn.epochs == int(button.text):
					self.nn.epochs = int(button.text)
					module_logger.info('epochs value changed to: ' + str(self.nn.epochs))
			except ValueError:
				self.popup.show('Error', "Invalid data in epochs")
			except:
				self.popup.show('Error', "An unexpected error updating epochs value")				
		
	def dataPathChange(self, widgetText):
		#updates trainingDataPath var in nn to text input value
		if len(widgetText) > 0:
			try: 
				if not self.nn.trainingDataPath == widgetText:
					self.nn.trainingDataPath = widgetText
					module_logger.info('trainingDataPath value changed to: ' + str(self.nn.trainingDataPath))
			except ValueError:
				self.popup.show('Error', "Invalid data in Training Data Path")
			except:
				self.popup.show('Error', "An unexpected error updating Training Data Path value")			
	
	def showFileChooser(self):
		dirPicker = HSFileChooserPopup()
		dirPicker.show('Choose Training Data Location', os.getcwd())
		self.dataPathChange(dirPicker.OKselectedDir)
	
	def showNNStats(self):
		self.popup.show('Test Title', 'Network nLayers: ' + str(self.nn.nLayers) + "\n" + 
									'Network internalSize: ' + str(self.nn.internalSize) + "\n" +
									'Network learningRate: ' + str(self.nn.learningRate) + "\n" +
									'Network epochs: ' + str(self.nn.epochs) + "\n" +
									'Data Path: ' + str(self.nn.trainingDataPath) + "\n")
		
		print('Data Path: ' + str(self.nn.trainingDataPath) )
		print('Data Path: ' + str(self.nn.trainingDataDir) )
	
	def StartTraining(self):
		self.nn.startTraining()
		module_logger.info('Training Started')
		
	def btnStartTraining(self, button):
		#event from button, starts new thread for StartTraining function
		thread = threading.Thread(target=self.StartTraining, args=())
		#thread.daemon = True # Daemonize thread
		thread.start()
		module_logger.info('New thread created for training')
		
		