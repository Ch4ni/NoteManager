import unittest
from test import ParameterizedTestCase
from NoteManagerTest import NoteManagerTest

suite = unittest.TestSuite()
suite.addTest(ParameterizedTestCase.parametrize(NoteManagerTest, param="DictStorage"))
unittest.TextTestRunner(verbosity=2).run(suite)
