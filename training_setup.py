import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from hs_rnn import Neural_Network
from CustomWidgets import HSConfirmPopup


class Training_Setup(Screen):
	nLayers = StringProperty()
	internalSize = StringProperty()
	learningRate = StringProperty()
	epochs = StringProperty()
	
	
	def __init__(self, _nn, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		self.internalSize = str(self.nn.internalSize)
		self.learningRate = str(self.nn.learningRate)
		self.epochs = str(self.nn.epochs)
		
		print('nLayers: ' +self.nLayers)
		
	def nLayersChange(self, value):
		self.nn.nLayers = value
		print('text value: ' + str(value))
		
	def printNlayers(self):
		print('Network nLayers: ' + str(self.nn.nLayers))
		popup = HSConfirmPopup()
		popup.show('Test Title', 'Test Text')

		
	def btnStartTraining(self, button):
		#print ('Button Pressed: ' + button.text)
		self.nn.startTraining()
		