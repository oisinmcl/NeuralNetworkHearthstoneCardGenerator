from hs_rnn import Neural_Network 
from hearthstoneAPI import HearthstoneAPI
from database_manager import Database_Manager

import json


db =  Database_Manager()

data = json.load(open('Output_data\output_1522685014.txt'))
for cards in data:   
	db.push(cards)

	
print(db.get())	

db.delete('-LAYPe_GTk5zVX4lDvF_')

db.put('-LAYPe_GTk5zVX4lDvF_', data[0])

#api = HearthstoneAPI()
#api.getLastestSet()
#api.getCardsByParam('sets', 'Basic')

#nn = Neural_Network()
#nn.startTraining()
#nn.StartGenerating(1000)