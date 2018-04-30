import unittest
import json

from database_manager import Database_Manager

from urllib.error import HTTPError

class Test_Database_Manager(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.db = Database_Manager()
		self.testCardData = '{"artist": "test artist","cardClass": "NEUTRAL","collectible": true,"cost": 3,"dbfId": 2523,"flavor": "Test Flavor","id": "EX1_322","name": "test card","playerClass": "PRIEST","rarity": "COMMON","set": "GVG","text": "test text", "type": "MINION"}'
		self.testCardJson = json.loads(self.testCardData)
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_get(self):
		self.assertIsNotNone(self.db.get())
		
	def test_push_httpError(self):
		self.assertRaises(HTTPError, self.db.push('this should fail'))
		
	def test_push(self):
		ref = self.db.push(self.testCardJson)
		self.assertIsNotNone(ref)
		#delete test card after test
		self.db.delete(ref['name'])
		
	def test_push_httpError(self):
		self.assertRaises(HTTPError, self.db.put('this should fail','this should fail'))	
		self.assertRaises(HTTPError, self.db.put('this should fail',self.testCardData))	
		
		
	def test_put(self):
		#add card for editing
		ref = self.db.push(self.testCardJson)
		#edit the card
		testCardData2 = '{"artist": "test artist 2","cardClass": "NEUTRAL","collectible": true,"cost": 3,"dbfId": 2523,"flavor": "Test Flavor 2","id": "EX1_322","name": "test card","playerClass": "PRIEST","rarity": "COMMON","set": "GVG","text": "test text", "type": "MINION"}'
		ref2 = self.db.put(ref['name'],self.testCardJson)
		#check return value is not null
		self.assertIsNotNone(ref2)
		#delete test card after test
		self.db.delete(ref['name'])
