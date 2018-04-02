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
		self.apiURL = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards'
		self.dataDir = 'training_data'
		self.key = 'oURgllqixCmshxGUxHbd9g4He5Ydp1n9Z88jsnlY8KWwDal5Wv'
		self.fileType = '.txt'
	
	
	def getLastestSet(self):
		try:
			module_logger.info('Getting Lastest Hearthstone Cards')
			response = requests.get(self.apiURL,
									headers={
									"X-Mashape-Key": self.key})
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


			
	def getCardsByParam(self, param ,id):
		try:
			module_logger.info('Getting Hearthstone Cards with parameter: ' +param+' and value: '+id)
			response = requests.get(self.apiURL+'/'+param +'/'+id,
									headers={
									"X-Mashape-Key": self.key})
			
			response.raise_for_status()
			
			if not os.path.exists(self.dataDir):
				os.mkdir(self.dataDir)
			
			timestamp = str(math.trunc(time.time()))
			with open(self.dataDir + '/' + id + 'Cards_' + timestamp +self.fileType, mode='wb') as localfile:     
				localfile.write(response.content)
		except IOError:
			module_logger.error("IO error getting cards by set. Error: "+ str(traceback.format_exc()))
		except:
			module_logger.error("Unexpected error getting cards by set. Error: "+ str(traceback.format_exc()))
		finally:
			return response.status_code
		
		