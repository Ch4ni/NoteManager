__author__ = 'acripps'

import unittest

from SQLManager import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sman = SQLManager()

    def testSqlManagerConstructorReturnsNonNone(self):
        self.assertIsNotNone(self.sman, "SQL Manager is none.")

    def testSearchEmptyQueryReturnsEmptyDict(self):
        self.assertEqual(self.sman.search(), {}, "received result")

    def testAddEmptyTitleAndQueryRaisesEmptyQueryException(self):
        exceptionIsThrownByMethod = False
        try:
            result = self.sman.addQuery()
        except EmptyQueryException:
            exceptionIsThrownByMethod = True
        self.assertTrue(exceptionIsThrownByMethod, "Expected EmptyQueryException was not thrown")

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        exceptionIsThrownByMethod = False
        try:
            result = self.sman.addQuery(sql="SELECT * FROM SOMETABLE")
        except EmptyTitleException:
            exceptionIsThrownByMethod = True
        self.assertTrue(exceptionIsThrownByMethod, "Expected EmptyTitleException was not thrown")

    def testAddEmptySqlRaisesEmptySqlException(self):
        exceptionIsThrownByMethod = False
        try:
            result = self.sman.addQuery(title="Blank SQL Query")
        except EmptySqlException:
            exceptionIsThrownByMethod = True
        self.assertTrue(exceptionIsThrownByMethod, "Expected EmptySqlException was not thrown")

if __name__ == '__main__':
    unittest.main()
