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


class Generate_Setup(Screen):
	checkpointFile = StringProperty()
	nLayers = StringProperty()
	internalSize = StringProperty()
	outputDir = StringProperty()
	numOfChars = StringProperty()
	
			   
	def __init__(self, _nn, **kwargs): 
		super(Generate_Setup, self).__init__(**kwargs)
		self.nn = _nn
		
		self.checkpointFile = str(self.nn.checkpoint)
		self.nLayers = str(self.nn.nLayers)
		self.internalSize = str(self.nn.internalSize)
		self.outputDir = str(self.nn.outputDir)
		self.numOfChars = str(self.nn.numOfChars)

		self.dirPicker = HSFileChooserPopup(self, True)
		self.popup = HSConfirmPopup()
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)          

	def nLayersChange(self, button):
		#updates nlayers var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try: 
				self.nn.nLayers = int(button.text)
			except ValueError:
				self.popup.show('Error', "Invalid data in nLayers")
			except:
				self.popup.show('Error', "An unexpected error in nLayers")

	def internalSizeChange(self, button):
		#updates internalSize var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try: 
				self.nn.internalSize = int(button.text)
			except ValueError:
				self.popup.show('Error', "Invalid data in internalSize")
			except:
				self.popup.show('Error', "An unexpected error in internalSize")
	

	def numOfCharsChange(self, button):
		#updates numOfChars var in nn to text input value
		button.enforce_int(button)
		if len(button.text) > 0:
			try: 
				self.nn.numOfChars = int(button.text)
			except ValueError:
				self.popup.show('Error', "Invalid data in numOfChars")
			except:
				self.popup.show('Error', "An unexpected error in numOfChars")
				

	def checkpointFileChange(self, widgetText):
		#updates trainingDataPath var in nn to text input value
		if len(widgetText) > 0:
			try: 
				if not self.nn.checkpoint == widgetText:
					self.nn.checkpoint = widgetText
					module_logger.info('checkpoint value changed to: ' + str(self.nn.checkpoint))
			except ValueError:
				self.popup.show('Error', "Invalid data in checkpoint. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating checkpoint file value. Error: "+ str(traceback.format_exc()))		
	
	def showCheckpointFileChooser(self):
		#dirPicker = HSFileChooserPopup()
		self.dirselect= False
		self.dirPicker.show('Choose a Checkpoint File', os.getcwd()+"Checkpoints")
		if len(self.dirPicker.OKselectedDir) > 0:
			self.checkpointFile = self.dirPicker.OKselectedDir 
			
	def outputPathChange(self, widgetText):
		#updates trainingDataPath var in nn to text input value
		if len(widgetText) > 0:
			try: 
				if not self.nn.outputDir == widgetText:
					self.nn.outputDir = widgetText
					module_logger.info('outputPathChange value changed to: ' + str(self.nn.outputDir))
			except ValueError:
				self.popup.show('Error', "Invalid data in outputPathChange. Error: "+ str(traceback.format_exc()))
			except:
				self.popup.show('Error', "An unexpected error updating outputPathChange value. Error: "+ str(traceback.format_exc()))		
	
	def showOutputDirChooser(self):
		#dirPicker = HSFileChooserPopup()
		self.dirselect= True
		self.dirPicker.show('Choose Output Data Location', os.getcwd())
		if len(self.dirPicker.OKselectedDir) > 0:
			self.outputDir = self.dirPicker.OKselectedDir 		
			
			
	def testingFunction(self):
		numOfFiles =int(numOfFiles) + 1
		print ("numOfFiles: "+str(numOfFiles))						


	def StartGenerating(self):
		module_logger.info('Training Thread Started')
		self.nn.StartGenerating()
		self.popup.show('Success', 'Generating Card Text Complete')
		
	def btnStartGenerating(self, button):
		module_logger.info('Creating new thread for training')
		#event from button, starts new thread for StartGenerating function
		thread = threading.Thread(target=self.StartGenerating, args=())
		#thread.daemon = True # Daemonize thread
		thread.start()

		
		
		
		