import requests
import math
import time
import os

import logging
import traceback

# create logger
module_logger = logging.getLogger('myApp')

class HearthstoneAPI:

	def __init__(self):
		self.apiURL = 'https://api.hearthstonejson.com'
		self.dataDir = 'NeuralNetwork/training_data'
		self.key = 'oURgllqixCmshxGUxHbd9g4He5Ydp1n9Z88jsnlY8KWwDal5Wv'
		self.fileType = '.txt'
		self.region = 'enUS'
		self.lastestSet = 'v1/latest'
		self.collectible = 'cards.collectible.json'
	
	
	def getLastestSet(self):
		try:
			module_logger.info('Getting Lastest Hearthstone Cards')
			response = requests.get(self.apiURL+'/'+ 
								self.lastestSet+'/'+
								self.region+'/'+
								self.collectible)
			response.raise_for_status()
			
			if not os.path.exists(self.dataDir):
				os.mkdir(self.dataDir)
			
			timestamp = str(math.trunc(time.time()))
			with open(self.dataDir + '/lastestCards_' + timestamp +self.fileType, mode='wb') as localfile:     
				localfile.write(response.content)
		except IOError:
			module_logger.error("IO error getting lastest cards. Error: "+ str(traceback.format_exc()))
		except:
			module_logger.error("Unexpected error getting lastest cards. Error: "+ str(traceback.format_exc()))
		finally:
			return response.status_code


			
	def getCardsByParam(self, param = '18336'):
		try:
			module_logger.info('Getting Hearthstone Cards with set number: ' +param)
			response = requests.get(self.apiURL+'/v1/'+ 
								param+'/'+
								self.region+'/'+
								self.collectible)
			
			response.raise_for_status()
			
			if not os.path.exists(self.dataDir):
				os.mkdir(self.dataDir)
			
			timestamp = str(math.trunc(time.time()))
			with open(self.dataDir + '/Set_' + param + '_' + timestamp +self.fileType, mode='wb') as localfile:     
				localfile.write(response.content)
		except IOError:
			module_logger.error("IO error getting cards by set. Error: "+ str(traceback.format_exc()))
		except:
			module_logger.error("Unexpected error getting cards by set. Error: "+ str(traceback.format_exc()))
		finally:
			return response.status_code
		
		