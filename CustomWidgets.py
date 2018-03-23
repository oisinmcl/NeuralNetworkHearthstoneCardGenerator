import kivy
kivy.require('1.10.0')

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup 
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

class HSButton(Button):
	background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	background_down = 	ObjectProperty('Resources/Buttons/SmallButtonHover.png')
	color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)

class HSLabel(Label):
	color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	
class HSTextInput(TextInput):
	foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	background_color = ListProperty([1, 1, 1, 0.5])
	#background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	multiline=False
	
class HSPopup(Popup):
	#foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	#background_color = ListProperty([ 0.4, 0.37, 0.32, 0.8])
	#font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	#font_size = NumericProperty(18)
	
	
	def show(self):
		mytext = 'test message'
		
		content = BoxLayout(orientation = 'vertical', 
							padding = (10))
		content.add_widget(HSLabel(text = mytext))
		
		hsbutton = HSButton(text = "OK!", size_hint=(1,.20))
		content.add_widget(hsbutton)
		
		mypopup = Popup(content = content,              
                title = "test",     
                auto_dismiss = False)
				
		hsbutton.bind(on_press=mypopup.dismiss)		
		mypopup.open()