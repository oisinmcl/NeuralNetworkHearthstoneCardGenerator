import kivy
kivy.require('1.10.0')

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ObjectProperty, ListProperty

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
	pass
	foreground_color = ListProperty([0.20,0.18,0.02,0.8])
	font_name = ObjectProperty('Resources/Fonts/BelweBdBTBold.ttf')
	font_size = NumericProperty(18)
	background_color = ListProperty([1, 1, 1, 0.5])
	#background_normal = ObjectProperty('Resources/Buttons/SmallButton.png')
	multiline=False
	