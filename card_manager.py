import kivy
kivy.require('1.10.0')  

from kivy.uix.screenmanager import Screen

import logging

# create logger
module_logger = logging.getLogger('myApp')


class Card_Manager(Screen):

			   
	def __init__(self, **kwargs): 
		super(Card_Manager, self).__init__(**kwargs)
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)

		
		
		