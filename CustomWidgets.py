import kivy
kivy.require('1.10.0')

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup 
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle

import re

class HSButton(Button):
	background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	background_down = 	ObjectProperty('Resources/Buttons/SmallButtonHover.png')
	color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)

class HSLabel(Label):
	color = ListProperty([0.20,0.18,0.02,0.9])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	
class HSTextInput(TextInput):
	foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	background_color = ListProperty([1, 1, 1, 0.5])
	#background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	multiline=False
	
class HSNumericInput(TextInput):
	foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	background_color = ListProperty([1, 1, 1, 0.5])
	#background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	multiline=False	
	
	
	def enforce_int(self, text_input):
		""" Ensure the text input contains only numeric characters or nothing"""
		if not text_input.text.isdigit():
			digit_list = [num for num in text_input.text if num.isdigit()]
			text_input.text = ''.join(digit_list)
		'''
		if text_input.text == '':
			text_input.text = '0'
		
		if float(text_input.text) < min:
			text_input.text = "".join(min)
		if float(text_input.text) > max:
			text_input.text = "".join(max)
		'''	

	def enforce_float(self, text_input):
		""" Ensure the text input contains a float"""
		regex = re.compile(r'[+-]?((\d+\.?\d*)|(\.\d+))$')
		
		if regex.match(text_input.text) == None:
			text_input.text = ''
		
	
class HSConfirmPopup(Popup):
	#foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	#background_color = ListProperty([ 0.4, 0.37, 0.32, 0.8])
	#font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	#font_size = NumericProperty(18)
	
	
	def show(self, _title, _text):
		mytext = _text
		content = BoxLayout(orientation = 'vertical', 
							padding = (10),
							spacing= 20)
		content.add_widget(HSLabel(text = mytext, color = [1,1,1,1]))
		
		hsbutton = HSButton(text = "OK!", size_hint=(.5,.75),pos_hint= {'x': .25,'top': 0})
		content.add_widget(hsbutton)
		
		mypopup = Popup(content = content,              
                title = _title,
				title_font = 'Resources/Fonts/Belwe-Medium.ttf',
                auto_dismiss = False,
				size_hint=(.5, .35),
				separator_color = [247/255,143/255,46/255,1])
		
		hsbutton.bind(on_press=mypopup.dismiss)		
		mypopup.open()
		