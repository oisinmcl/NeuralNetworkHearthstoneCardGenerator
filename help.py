import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty,ObjectProperty


import logging

# create logger
module_logger = logging.getLogger('myApp')


class Help(Screen):

	helpText = StringProperty()
			   
	def __init__(self, **kwargs): 
		super(Help, self).__init__(**kwargs)

		self.helpText = ''
		
		with open('help.txt', 'r') as myfile:
			self.helpText = myfile.read()
		
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)
		
