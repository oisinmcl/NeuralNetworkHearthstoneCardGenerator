from firebase import firebase

class Database_Manager:

	def __init__(self):
		self.apiKey = ""
		self.credentials = ""
		self.dbURL = "https://final-year-project-f08b2.firebaseio.com/"
		self.firebase = firebase.FirebaseApplication(self.dbURL, None)
	
	def get(self):
		try:
			result = self.firebase.get('/cards', None)
			return result
		except :
			print('Error fetching data from firebase')
		
	def push(self, data):
		try:
			ref = self.firebase.post('/cards',data)
		except :
			print('Error pushing data to firebase')
	
	def put(self, id, data):
		try:
			self.firebase.put('/cards',id,data)		
		except :
			print('Error putting data to firebase')	

			
	def delete(self, id):
		try:		
			self.firebase.delete('/cards', id)
		except :
			print('Error deleting data from firebase')			
