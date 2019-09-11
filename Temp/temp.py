#from hs_rnn import Neural_Network 
#from hearthstoneAPI import HearthstoneAPI
#from database_manager import Database_Manager
from collections import Counter

import json
import re

#db =  Database_Manager()


data = json.load(open('Output_data\output_1525082192.txt'))
costs = Counter(k['cost'] for k in data if k.get('cost'))
attacks = Counter(k['attack'] for k in data if k.get('attack'))
healths = Counter(k['health'] for k in data if k.get('health'))
rarities = Counter(k['rarity'] for k in data if k.get('rarity'))
cardClasses = Counter(k['cardClass'] for k in data if k.get('cardClass'))

with open("Temp/temp_output.txt", mode='a') as localfile:     
	localfile.write('Cost: ' + str(costs) + "\n")
	localfile.write('attacks: ' + str(attacks) + "\n")
	localfile.write('healths: '+str(healths) + "\n")
	localfile.write('rarities: '+str(rarities) + "\n")
	localfile.write('cardClasses: '+str(cardClasses) + "\n")





# testCardData = '{"artist": "test artist","cardClass": "NEUTRAL","collectible": true,"cost": 3,"dbfId": 2523,"flavor": "Test Flavor","id": "EX1_322","name": "test card","playerClass": "PRIEST","rarity": "COMMON","set": "GVG","text": "test text", "type": "MINION"}'
# testCardJson = json.loads(testCardData)
# print(testCardJson)
# print(db.push(testCardJson))

# file = open('Output_data\output_1524659790.txt', 'r')
# s = file.read()
# #print(s)
# count = 0
# result = None

# while True:
	# try:
		# result = json.loads(s)   # try to parse...
		# break                    # parsing worked -> exit loop
	# except Exception as e:
		# # "Expecting , delimiter: line 34 column 54 (char 1158)"
		# # position of unexpected character after '"'
		# unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
		# # position of unescaped '"' before that
		# unesc = s.rfind(r'"', 0, unexp)
		# s = s[:unesc] + r'\"' + s[unesc+1:]
		# # position of correspondig closing '"' (+2 for inserted '\')
		# closg = s.find(r'"', unesc + 2)
		# s = s[:closg] + r'\"' + s[closg+1:]
		# count+=1
		# if (count > 1000): 
			# break		
# print(s)
# print(result)


#for cards in data:   
#	db.push(cards)

	
#print(db.get())	

#db.delete('-LAYPe_GTk5zVX4lDvF_')

#db.put('-LAYPe_GTk5zVX4lDvF_', data[0])

# api = HearthstoneAPI()
# api.getLastestSet()
# api.getCardsByParam('20022')

#nn = Neural_Network()
#nn.startTraining()
#nn.StartGenerating(1000)