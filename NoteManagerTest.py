__author__ = 'acripps'

import unittest

from NoteManager import *
from test import ParametrizedTestCase


class NoteManagerTest(ParametrizedTestCase):
    def setUp(self):
        self.noteMan = NoteManager(self.param[0], *self.param[1], **self.param[2])
        self.exceptionIsThrownByMethod = False
        self.receivedException = None

    def tearDown(self):
        self.noteMan._purge_all_notes()

    def testNoteManagerConstructorReturnsNonNone(self):
        self.assertIsNotNone(
            self.noteMan,
            "Param: {}. Note Manager is none.".format(self.param)
        )

    def testSearchEmptyNoteReturnsEmptyDict(self):
        results = self.noteMan.search()
        self.assertEqual(
            results,
            {},
            "Param: {}. Received result: {}".format(self.param, results)
        )

    def testAddEmptyTitleAndNoteRaisesEmptyNoteException(self):
        try:
            self.noteMan.add_note()
        except EmptyNoteException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyNoteException was not thrown"
            .format(self.param)
        )

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        try:
            self.noteMan.add_note(body="SELECT * FROM SOMETABLE")
        except EmptyTitleException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyTitleException was not thrown"
            .format(self.param)
        )

    def testAddEmptyBodyRaisesEmptyBodyException(self):
        try:
            self.noteMan.add_note(title="Blank Note")
        except EmptyBodyException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyBodyException was not thrown"
            .format(self.param)
        )

    def testAddValidNote(self):
        try:
            self.noteMan.add_note("Select everything from table",
                                  "SELECT * FROM X")
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception: ({!r})"
            .format(self.param, self.receivedException)
        )

    def testRetrieveNoteWithExactTitle(self):
        note_title = "Select everything from table"
        note_body = "SELECT * FROM X"
        try:
            self.noteMan.add_note(note_title, note_body)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception ({!r}) during addNote"
            .format(self.param, self.receivedException)
        )
        results = self.noteMan.search(note_title)
        self.assertTrue(
            note_title in results,
            "Param: {}. Expected Title not in result set"
            .format(self.param)
        )
        self.assertEqual(
            results[note_title],
            note_body,
            "Param: {}. Note Body does not match Expected result"
            .format(self.param)
        )

    def testRetrieveNoteWithPartialTitle(self):
        note_title = "Select everything from table"
        note_body = "SELECT * FROM X"
        try:
            self.noteMan.add_note(note_title, note_body)
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception ({!r}) during addNote"
            .format(self.param, self.receivedException)
        )
        results = self.noteMan.search("Select")
        self.assertTrue(
            note_title in results,
            "Param: {}. Expected Title not in result set"
            .format(self.param)
        )
        self.assertEqual(
            results[note_title],
            note_body,
            "Param: {}. Note Body does not match Expected result"
            .format(self.param)
        )

    def testRetrieveAllNotesWithPartialSearchParameter(self):
        notes = {
            "Select everything from table": "SELECT * FROM X",
            "Select one thing from table": "SELECT TOP 1 * FROM X"
        }
        try:
            for k in notes:
                self.noteMan.add_note(k, notes[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception ({!r}) during addNote"
            .format(self.param, self.receivedException)
        )
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes), len(results))
        for k in notes:
            self.assertTrue(
                k in results,
                "Param: {}. Expected Title ({}) not in result set"
                .format(self.param, k)
            )
            self.assertEqual(
                results[k],
                notes[k],
                "Param: {}. Note Body does not match expected result"
                .format(self.param)
            )

    def testRetrieveSomeNotesWithPartialSearchParameter(self):
        non_match_title = "Nope, nope, nope"
        notes = {
            "Select everything from table": "SELECT * FROM X",
            "Select one thing from table": "SELECT TOP 1 * FROM X",
            non_match_title:
                "exec sp_MSforeachtable @command1 = \"DROP TABLE ?\""
        }
        try:
            for k in notes:
                self.noteMan.add_note(k, notes[k])
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception ({!r}) during addNote"
            .format(self.param, self.receivedException)
        )
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes) - 1, len(results))
        self.assertFalse(non_match_title in results)
        for k in results:
            self.assertTrue(
                k in notes,
                "Param: {}. Expected Title ({}) not in result set"
                .format(self.param, k)
            )
            self.assertEqual(
                results[k],
                notes[k],
                "Param: {}. Note Body does not match expected result"
                .format(self.param)
            )

    def testAddDuplicateNoteTitle(self):
        note_title = "Select everything from table"
        note1_body = "SELECT * FROM X"
        note2_body = "SELECT col1,col2,...,colN FROM X"
        try:
            self.noteMan.add_note(note_title, note1_body)
            self.noteMan.add_note(note_title, note2_body)
        except DuplicateEntryException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected DuplicateEntryException was not thrown"
            .format(self.param)
        )


if __name__ == '__main__':
    unittest.main()
