import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from hs_rnn import Neural_Network
from CustomWidgets import HSPopup


class Training_Setup(Screen):
	nLayers = StringProperty()
	
	
	def __init__(self, _nn, **kwargs): 
		super(Training_Setup, self).__init__(**kwargs)
		self.nn = _nn
		self.nLayers = str(self.nn.nLayers)
		print('nLayers: ' +self.nLayers)
		
	def nLayersChange(self, value):
		self.nn.nLayers = value
		print('text value: ' + str(value))
		
	def printNlayers(self):
		print('Network nLayers: ' + str(self.nn.nLayers))
		popup = HSPopup()
		popup.show()
		'''
		popup = HSPopup(title='Test popup', 
					content=Label(text='Network nLayers: ' + str(self.nn.nLayers)),
					auto_dismiss=False)
		popup.open()
		'''
		
	
	def btnStartTraining(self, button):
		print ('Button Pressed: ' + button.text)
		