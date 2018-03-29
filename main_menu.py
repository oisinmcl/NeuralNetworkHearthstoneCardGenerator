import kivy
kivy.require('1.10.0')  

from kivy.app import App
from kivy.uix.screenmanager import Screen

import logging

# create logger
module_logger = logging.getLogger('myApp')

class Main_Menu(Screen):
	def __init__(self, **kwargs): 
		super(Main_Menu, self).__init__(**kwargs)
		#module_logger.info('Main_Menu Initialized')
		
		
	def on_enter(self):
		module_logger.info('Screen changed to :	'+ self.name)


		
