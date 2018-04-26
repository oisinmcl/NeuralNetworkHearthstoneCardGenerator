import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from hs_rnn import Neural_Network
from CustomWidgets import HSConfirmPopup, HSFileChooserPopup

from data_tools import Data_Tools
from hearthstoneAPI import HearthstoneAPI

import threading
import os
import logging
import traceback

# create logger
module_logger = logging.getLogger('myApp')

class Training_Setup(Screen):
	nLayers = StringProperty()
	internalSize = StringProperty()
	learningRate = StringProperty()
	epochs = StringProperty()
	
	dataPath = StringProperty()
	numOfFiles = StringProperty()
	fileSizes = StringProperty()
	
	accuracyTarget = StringProperty()
	
			   
	def __init__(self, _nn, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		#module_logger.info('Training_Setup Initialized')
		self.txt = Data_Tools()
		self.api = HearthstoneAPI()
		
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		self.internalSize = str(self.nn.internalSize)
		self.learningRate = str(self.nn.learningRate)
		self.epochs = str(self.nn.epochs)
		self.popup = HSConfirmPopup()
		self.dataPath = str(self.nn.trainingDataPath)
		self.accuracyTarget = str(self.nn.accuracyTarget)

		self.dirPicker = HSFileChooserPopup(self)
		
		self.numOfFiles = str(0)
		self.fileSizes = str(0)
		
		self.updateTrainingDataStats()
		
		
		

	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)
		self.updateTrainingDataStats()

	def nLayersChange(self, button):
		#updates nlayers var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try:
				if not self.nn.nLayers == int(button.text):
					self.nn.nLayers = int(button.text)
					module_logger.info('nLayers value changed to: ' + str(self.nn.nLayers))
			except ValueError:
				self.popup.show('Error', "Invalid data in nLayers. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error in nLayers. Error: "+ str(traceback.format_exc()))

	def internalSizeChange(self, button):
		#updates internalSize var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try: 
				if not self.nn.internalSize == int(button.text):
					self.nn.internalSize = int(button.text)
					module_logger.info('internalSize value changed to: ' + str(self.nn.internalSize))
			except ValueError:
				self.popup.show('Error', "Invalid data in internalSize. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error in internalSize. Error: "+ str(traceback.format_exc()))
				
	def learningRateChange(self, button):
		#updates learningRate var in nn to text input value
		button.enforce_float(button)
		if len(button.text) > 0:
			try: 
				if not self.nn.learningRate == float(button.text):
					self.nn.learningRate = float(button.text)
					module_logger.info('learningRate value changed to: ' + str(self.nn.learningRate))
			except ValueError:
				self.popup.show('Error', "Invalid data in learningRate. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating learningRate value. Error: "+ str(traceback.format_exc()))
				
	def epochsChange(self, button):
		#updates epochs var in nn to text input value
		if len(button.text) > 0:
			try: 
				button.enforce_int(button)
				if not self.nn.epochs == int(button.text):
					self.nn.epochs = int(button.text)
					module_logger.info('epochs value changed to: ' + str(self.nn.epochs))
			except ValueError:
				self.popup.show('Error', "Invalid data in epochs. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating epochs value. Error: "+ str(traceback.format_exc()))		

	def accuracyTargetChange(self, button):
		#updates accuracyTarget var in nn to text input value
		if len(button.text) > 0:
			try: 
				button.enforce_float(button)
				if not self.nn.accuracyTarget == float(button.text):
					self.nn.accuracyTarget = float(button.text)
					module_logger.info('Accuracy target value changed to: ' + str(self.nn.accuracyTarget))
			except ValueError:
				self.popup.show('Error', "Invalid data in accuracy target. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating accuracy target value. Error: "+ str(traceback.format_exc()))						
		
	def dataPathChange(self, widgetText):
		#updates trainingDataPath var in nn to text input value
		if len(widgetText) > 0:
			try: 
				if not self.nn.trainingDataPath == widgetText:
					self.nn.trainingDataPath = widgetText
					module_logger.info('trainingDataPath value changed to: ' + str(self.nn.trainingDataPath))
			except ValueError:
				self.popup.show('Error', "Invalid data in Training Data Path. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating Training Data Path value. Error: "+ str(traceback.format_exc()))		
	
	def showFileChooser(self):
		#dirPicker = HSFileChooserPopup()
		self.dirPicker.show('Choose Training Data Location', os.getcwd())
		if len(self.dirPicker.OKselectedDir) > 0:
			self.dataPath = self.dirPicker.OKselectedDir 
	
	def showNNStats(self):
		self.popup.show('Test Title', 'Network nLayers: ' + str(self.nn.nLayers) + "\n" + 
									'Network internalSize: ' + str(self.nn.internalSize) + "\n" +
									'Network learningRate: ' + str(self.nn.learningRate) + "\n" +
									'Network epochs: ' + str(self.nn.epochs) + "\n" +
									'Data Path: ' + str(self.nn.trainingDataPath) + "\n")
		
		print('Data Path: ' + str(self.nn.trainingDataPath) )
		print('Data Path: ' + str(self.nn.trainingDataDir) )
		
	def testingFunction(self):
		numOfFiles =int(numOfFiles) + 1
		print ("numOfFiles: "+str(numOfFiles))
		
	def getLastestCards(self):
		try:
			status = self.api.getLastestSet()
			self.updateTrainingDataStats()
			if status == 200:
				self.popup.show('Success', 'Cards Downloaded To ' + self.dataPath)
			else:
				self.popup.show('Error', 'There was a HTTP error getting cards')
		except Exception:
			self.popup.show('Error', 'Error getting lastest cards.')				
		
	def getCardsByParam(self, param='18336'):
		try:
			status = self.api.getCardsByParam(param)
			self.updateTrainingDataStats()
			
			if status == 200:
				self.popup.show('Success', 'Cards Downloaded To ' + self.dataPath)
			else:
				self.popup.show('Error', 'There was a HTTP error getting cards')
			
		except Exception:
			self.popup.show('Error', 'Error getting cards by parameter.')		

	def btnGetLastestCards(self):
		#event from button, starts new thread for getLastestCards function
		thread = threading.Thread(target=self.getLastestCards, args=())
		thread.start()					
		
	def btnGetCardsByParam(self, param='18336',):
		#event from button, starts new thread for getCardsByParam function
		thread = threading.Thread(target=self.getCardsByParam, args=())
		thread.start()				
		
	def updateTrainingDataStats(self):
		self.numOfFiles = str(self.txt.countNumberOfFiles(self.dataPath))
		self.fileSizes = self.txt.convert_bytes(self.txt.calcFileSizes(self.dataPath))
		#self.fileSizes = str(self.txt.calcFileSizes(self.dataPath))
		#print ("numOfFiles: "+str(self.numOfFiles))
		#print ("fileSizes: "+str(self.fileSizes))
	

	def StartTraining(self):
		module_logger.info('Training Thread Started')
		self.nn.startTraining()
		
	def btnStartTraining(self, button):
		module_logger.info('Creating new thread for training')
		#event from button, starts new thread for StartTraining function
		thread = threading.Thread(target=self.StartTraining, args=())
		#thread.daemon = True # Daemonize thread
		thread.start()

		
		