import unittest

loader = unittest.TestLoader()
testDir = 'Tests'
suite = loader.discover(testDir)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)