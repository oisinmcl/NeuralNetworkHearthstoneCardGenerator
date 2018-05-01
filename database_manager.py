from firebase import firebase
from urllib.error import HTTPError

import logging
import traceback
import math
import time
import json
#import urllib2

module_logger = logging.getLogger('myApp')

class Database_Manager:

	def __init__(self):
		self.apiKey = ""
		self.credentials = ""
		self.dbURL = "https://final-year-project-f08b2.firebaseio.com/"
		self.firebase = firebase.FirebaseApplication(self.dbURL, None)
		self.dataDir = 'Output_data'
		self.fileType = '.txt'
	
	def get(self):
		try:
			result = self.firebase.get('/cards', None)
			myJSON = json.dumps(result)
			timestamp = str(math.trunc(time.time()))
			with open(self.dataDir + '/FirebaseCards_' + timestamp +self.fileType, mode='a+') as localfile:     
				localfile.write(myJSON)	
			return result
		except HTTPError as ex: 
			module_logger.error('HTTP Error fetching data from firebase: ' +  e.message)
		except :
			module_logger.error('Error fetching data from firebase: ' + str(traceback.format_exc()))
		
	def push(self, data):
		try:
			ref = self.firebase.post('/cards',data)
			return ref
		except HTTPError as ex: 
			module_logger.error('HTTP Error pushing data to  firebase: ' +  e.message)			
		except :
			module_logger.error('Error pushing data to firebase: '+ str(traceback.format_exc()))
	
	def put(self, id, data):
		try:
			ref = self.firebase.put('/cards',id,data)	
			return ref
		except HTTPError as ex: 
			module_logger.error('HTTP Error putting data to firebase: ' +  e.message)			
		except :
			module_logger.error('Error putting data to firebase: '+ str(traceback.format_exc()))

			
	def delete(self, id):
		try:		
			self.firebase.delete('/cards', id)
		except HTTPError as ex: 
			module_logger.error('HTTP Error deleting data from firebase: ' +  e.message)			
		except :
			module_logger.error('Error deleting data from firebase: ' + str(traceback.format_exc()))		
