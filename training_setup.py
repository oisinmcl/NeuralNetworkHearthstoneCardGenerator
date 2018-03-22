import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from hs_rnn import Neural_Network


class Training_Setup(Screen):
	nLayers = StringProperty()
	
	
	def __init__(self, _nn, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		print('nLayers: ' +self.nLayers)
		
	def printNlayers(self):
		print('network nLayers: ' + str(self.nn.nLayers))
		print('Screen nLayers: ' + str(self.nLayers))
		
	
	def btnStartTraining(self, button):
		print ('Button Pressed: ' + button.text)
		