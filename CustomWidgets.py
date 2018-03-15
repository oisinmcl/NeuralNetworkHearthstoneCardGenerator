import kivy
kivy.require('1.10.0')

from kivy.uix.button import Button

class HSButton(Button):
	background_normal = 'Resources/Buttons/SmallButton.png'
	background_down = 	'Resources/Buttons/SmallButtonHover.png'
	color = 0.20,0.18,0.02,0.8
	font_name = 'Resources/Fonts/BelweBdBTBold.ttf'
	font_size = 18
