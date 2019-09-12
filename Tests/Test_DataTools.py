import unittest

from Tools.DataTools import DataTools

class Test_DataTools(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.dataTools = DataTools()
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_encodeChar(self):
		self.assertEqual(self.dataTools.encodeChar(ord('A')), 35)
		self.assertEqual(self.dataTools.encodeChar(ord('a')), 67)
		self.assertEqual(self.dataTools.encodeChar(ord('X')), 58)
		self.assertEqual(self.dataTools.encodeChar(ord('x')), 90)
		self.assertEqual(self.dataTools.encodeChar(ord('[')), 61)
		self.assertEqual(self.dataTools.encodeChar(ord(']')), 63)
		self.assertEqual(self.dataTools.encodeChar(ord(';')), 29)
		self.assertEqual(self.dataTools.encodeChar(ord('<')), 61)
		self.assertEqual(self.dataTools.encodeChar(ord('>')), 63)
		
	def test_decodeChar(self):
		self.assertEqual(chr(self.dataTools.decodeChar(35)), 'A')
		self.assertEqual(chr(self.dataTools.decodeChar(67)), 'a')
		self.assertEqual(chr(self.dataTools.decodeChar(58)), 'X')
		self.assertEqual(chr(self.dataTools.decodeChar(90)), 'x')
		self.assertEqual(chr(self.dataTools.decodeChar(61)), '[')
		self.assertEqual(chr(self.dataTools.decodeChar(63)), ']')
		self.assertEqual(chr(self.dataTools.decodeChar(29)), ';')
		
		
	def test_encode_text(self):
		self.assertEqual(self.dataTools.encode_text('abcABC[];'), [67,68,69,35,36,37,61,63,29])
	
	def test_decode_text(self):
		self.assertEqual(self.dataTools.decode_text([67,68,69,35,36,37,61,63,29]),'abcABC[];')
		
	def test_convert_bytes(self):
		self.assertEqual(self.dataTools.convert_bytes(1), '1.0 B')
		self.assertEqual(self.dataTools.convert_bytes(1028), '1.0 KB')
		self.assertEqual(self.dataTools.convert_bytes(999), '999.0 B')
		self.assertEqual(self.dataTools.convert_bytes(1073741824), '1.0 GB')
		self.assertEqual(self.dataTools.convert_bytes(1024*1024*1024), '1.0 GB')
		
	def test_countNumberOfFiles(self):
		self.assertEqual(self.dataTools.countNumberOfFiles('Tests/Count_Files_Test'), 4)

	def test_calcFileSizes(self):
		self.assertEqual(self.dataTools.calcFileSizes('Tests/Count_Files_Test'), 339664)
		
		
		