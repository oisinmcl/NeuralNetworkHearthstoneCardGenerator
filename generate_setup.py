import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from hs_rnn import Neural_Network
from CustomWidgets import HSConfirmPopup

import threading


class Generate_Setup(Screen):
	nLayers = StringProperty()
	internalSize = StringProperty()
	learningRate = StringProperty()
	epochs = StringProperty()
	
			   
	def __init__(self, _nn, **kwargs): 
		super(Generate_Setup, self).__init__(**kwargs)
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		self.internalSize = str(self.nn.internalSize)
		self.learningRate = str(self.nn.learningRate)
		self.epochs = str(self.nn.epochs)
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
				
	def learningRateChange(self, button):
		#updates learningRate var in nn to text input value
		button.enforce_float(button)
		if len(button.text) > 0:
			try: 
				
				self.nn.learningRate = float(button.text)
			except ValueError:
				self.popup.show('Error', "Invalid data in learningRate")
			except:
				self.popup.show('Error', "An unexpected error in learningRate")
				
	def epochsChange(self, button):
		#updates epochs var in nn to text input value
		if len(button.text) > 0:
			try: 
				button.enforce_int(button)
				self.nn.epochs = int(button.text)
			except ValueError:
				self.popup.show('Error', "Invalid data in epochs")
			except:
				self.popup.show('Error', "An unexpected error in epochs")				
		
	def showNNStats(self):
		self.popup.show('Test Title', 'Network nLayers: ' + str(self.nn.nLayers) + "\n" + 
									'Network internalSize: ' + str(self.nn.internalSize) + "\n" +
									'Network learningRate: ' + str(self.nn.learningRate) + "\n" +
									'Network epochs: ' + str(self.nn.epochs) + "\n")
		
		
	def StartTraining(self):
		self.nn.startTraining()
		
	def btnStartTraining(self, button):
		#event from button, starts new thread for StartTraining function
		thread = threading.Thread(target=self.StartTraining, args=())
		thread.daemon = True # Daemonize thread
		thread.start()
		
		