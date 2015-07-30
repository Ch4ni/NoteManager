__author__ = 'acripps'

import unittest
import sys


from NoteManager import *
from test import ParameterizedTestCase

class NoteManagerTest(ParameterizedTestCase):
    def setUp(self):
        self.noteMan = NoteManager(self.param)
        self.exceptionIsThrownByMethod = False
        self.receivedException = None

    def testNoteManagerConstructorReturnsNonNone(self):
        self.assertIsNotNone(self.noteMan, "Note Manager is none.")

    def testSearchEmptyNoteReturnsEmptyDict(self):
        results = self.noteMan.search()
        self.assertEqual(results, {}, "received result: {}".format(results))

    def testAddEmptyTitleAndNoteRaisesEmptyNoteException(self):
        try:
            self.noteMan.addNote()
        except EmptyNoteException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptyNoteException was not thrown")

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        try:
            self.noteMan.addNote(body="SELECT * FROM SOMETABLE")
        except EmptyTitleException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptyTitleException was not thrown")

    def testAddEmptyBodyRaisesEmptyBodyException(self):
        try:
            self.noteMan.addNote(title="Blank Note")
        except EmptyBodyException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected EmptyBodyException was not thrown")

    def testAddValidNote(self):
        try:
            self.noteMan.addNote("Select everything from table", "SELECT * FROM X")
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception: {0!s}".format(self.receivedException))

    def testRetreiveNoteWithExactTitle(self):
        noteTitle = "Select everything from table"
        noteBody   = "SELECT * FROM X"
        try:
            self.noteMan.addNote(noteTitle,noteBody)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addNote".format(self.receivedException))
        results = self.noteMan.search(noteTitle)
        self.assertTrue(results.has_key(noteTitle), "Expected Title not in result set")
        self.assertEqual(results[noteTitle], noteBody, "Note Body does not match Expected result")

    def testRetreiveNoteWithPartialTitle(self):
        noteTitle = "Select everything from table"
        noteBody = "SELECT * FROM X"
        try:
            self.noteMan.addNote(noteTitle, noteBody)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addNote".format(self.receivedException))
        results = self.noteMan.search("Select")
        self.assertTrue(results.has_key(noteTitle), "Expected Title not in result set")
        self.assertEqual(results[noteTitle], noteBody, "Note Body does not match Expected result")

    def testRetrieveAllNotesWithPartialSearchParameter(self):
        notes = {
                    "Select everything from table": "SELECT * FROM X",
                    "Select one thing from table" : "SELECT TOP 1 * FROM X"
                }
        try:
            for k in notes:
                self.noteMan.addNote(k, notes[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addNote".format(self.receivedException))
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes), len(results))
        for k in notes:
            self.assertTrue(results.has_key(k), "Expected Title ({}) not in result set".format(k))
            self.assertEqual(results[k], notes[k], "Note Body does not match expected result")

    def testRetrieveSomeNotesWithPartialSearchParameter(self):
        nonMatchTitle = "Nope, nope, nope"
        notes = {
                    "Select everything from table": "SELECT * FROM X",
                    "Select one thing from table" : "SELECT TOP 1 * FROM X",
                    nonMatchTitle : "exec sp_MSforeachtable @command1 = \"DROP TABLE ?\""
                }
        try:
            for k in notes:
                self.noteMan.addNote(k, notes[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(self.exceptionIsThrownByMethod, "Received unexpected Exception {0!s} during addNote".format(self.receivedException))
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes) - 1, len(results))
        self.assertFalse(results.has_key(nonMatchTitle))
        for k in results:
            self.assertTrue(notes.has_key(k), "Expected Title ({}) not in result set".format(k))
            self.assertEqual(results[k], notes[k], "Note Body does not match expected result")

    def testAddDuplicateNoteTitle(self):
        noteTitle = "Select everything from table"
        note1Sql = "SELECT * FROM X"
        note2Sql = "SELECT col1,col2,...,colN FROM X"
        try:
            self.noteMan.addNote(noteTitle, note1Sql)
            self.noteMan.addNote(noteTitle, note2Sql)
        except DuplicateEntryException as e:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(self.exceptionIsThrownByMethod, "Expected DuplicateEntryException was not thrown")
        
if __name__ == '__main__':
    unittest.main()
