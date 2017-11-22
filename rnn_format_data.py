import json
from json import dumps
import random
from pprint import pprint

with open('training_data\cards_collectible.JSON', encoding="latin-1") as data_file:    
    data = json.load(data_file)
	
for i in range(0, 2):	
	data+=data
	
random.shuffle(data)
	
file = open(r"training_data\new_data_format.JSON", "w")
file.write(str(json.dumps(data)))
#pprint(data)