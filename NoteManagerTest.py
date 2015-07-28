__author__ = 'acripps'

import unittest

from SQLManager import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sman = SQLManager()
        self.exceptionIsThrownByMethod = False
        self.receivedException = None

    def testSqlManagerConstructorReturnsNonNone(self):
        self.assertIsNotNone(self.sman, "SQL Manager is none.")

    def testSearchEmptyQueryReturnsEmptyDict(self):
        results = self.sman.search()
        self.assertEqual(results, {}, "received result: {}".format(results))

    def testAddEmptyTitleAndQueryRaisesEmptyQueryException(self):
        try:
            self.sman.addQuery()
        except EmptyQueryException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptyQueryException was not thrown")

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        try:
            self.sman.addQuery(sql="SELECT * FROM SOMETABLE")
        except EmptyTitleException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptyTitleException was not thrown")

    def testAddEmptySqlRaisesEmptySqlException(self):
        try:
            self.sman.addQuery(title="Blank SQL Query")
        except EmptySqlException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptySqlException was not thrown")

    def testAddValidQuery(self):
        try:
            self.sman.addQuery("Select everything from table", "SELECT * FROM X")
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception: {0!s}".format(self.receivedException))

    def testRetreiveQueryWithExactTitle(self):
        queryTitle = "Select everything from table"
        querySql   = "SELECT * FROM X"
        try:
            self.sman.addQuery(title=queryTitle, sql=querySql)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addQuery".format(self.receivedException))
        results = self.sman.search(queryTitle)
        self.assertTrue(results.has_key(queryTitle), "Expected Query title not in result set")
        self.assertEqual(results[queryTitle], querySql, "Query SQL does not match Expected result")

    def testRetreiveQueryWithPartialTitle(self):
        queryTitle = "Select everything from table"
        querySql = "SELECT * FROM X"
        try:
            self.sman.addQuery(queryTitle, querySql)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addQuery".format(self.receivedException))
        results = self.sman.search("Select")
        self.assertTrue(results.has_key(queryTitle), "Expected Query title not in result set")
        self.assertEqual(results[queryTitle], querySql, "Query SQL does not match Expected result")

    def testRetrieveAllQueriesWithPartialSearchParameter(self):
        queries = {
                    "Select everything from table": "SELECT * FROM X",
                    "Select one thing from table" : "SELECT TOP 1 * FROM X"
                }
        try:
            for k in queries:
                self.sman.addQuery(k, queries[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addQuery".format(self.receivedException))
        results = self.sman.search("Select")
        self.assertEqual(len(queries), len(results))
        for k in queries:
            self.assertTrue(results.has_key(k), "Expected query title ({}) not in result set".format(k))
            self.assertEqual(results[k], queries[k], "Query SQL does not match expected result")

    def testRetrieveSomeQueriesWithPartialSearchParameter(self):
        nonMatchTitle = "Nope, nope, nope"
        queries = {
                    "Select everything from table": "SELECT * FROM X",
                    "Select one thing from table" : "SELECT TOP 1 * FROM X",
                    nonMatchTitle : "exec sp_MSforeachtable @command1 = \"DROP TABLE ?\""
                }
        try:
            for k in queries:
                self.sman.addQuery(k, queries[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addQuery".format(self.receivedException))
        results = self.sman.search("Select")
        self.assertEqual(len(queries) - 1, len(results))
        self.assertFalse(results.has_key(nonMatchTitle))
        for k in results:
            self.assertTrue(queries.has_key(k), "Expected query title ({}) not in result set".format(k))
            self.assertEqual(results[k], queries[k], "Query SQL does not match expected result")

    def testAddDuplicateQueryTitle(self):
        queryTitle = "Select everything from table"
        query1Sql = "SELECT * FROM X"
        query2Sql = "SELECT col1,col2,...,colN FROM X"
        try:
            self.sman.addQuery(queryTitle, query1Sql)
            self.sman.addQuery(queryTitle, query2Sql)
        except DuplicateEntryException as e:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected DuplicateEntryException was not thrown")
        
if __name__ == '__main__':
    unittest.main()
