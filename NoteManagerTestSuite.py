import unittest
from test import ParametrizedTestCase
from NoteManagerTest import NoteManagerTest

suite = unittest.TestSuite()
suite.addTest(ParametrizedTestCase.parametrize(NoteManagerTest, param="DictStorage"))
#suite.addTest(ParameterizedTestCase.parametrize(NoteManagerTest, param="FilesystemStorage"))
unittest.TextTestRunner(verbosity=2).run(suite)
