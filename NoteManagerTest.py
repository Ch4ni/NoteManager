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
            [],
            "Param: {}. Received result: []".format(self.param, results)
        )

    def testAddEmptyTitleAndNoteRaisesEmptyNoteException(self):
        note_id = self.tryAddNoteWithExcept("", "", EmptyNoteException)
        self.assertExceptionRaised(EmptyNoteException)
        self.assertNoteIdIsNone(note_id)

    def tryAddNoteWithExcept(self, title="", body="", exception=Exception):
        try:
            return self.noteMan.add_note(title, body)
        except exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e

    def assertExceptionRaised(self, exception_type):
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected {!r} was not thrown"
                .format(self.param, exception_type)
        )

    def assertNoteIdIsNone(self, note_id):
        self.assertIsNone(note_id, "note_id is not None: {}".format(note_id))

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        note_id = self.tryAddNoteWithExcept(body="SELECT * FROM SOMETABLE", exception=EmptyTitleException)
        self.assertExceptionRaised(EmptyTitleException)
        self.assertNoteIdIsNone(note_id)

    def testAddEmptyBodyRaisesEmptyBodyException(self):
        note_id = self.tryAddNoteWithExcept("Blank Note", "", EmptyBodyException)
        self.assertExceptionRaised(EmptyBodyException)
        self.assertNoteIdIsNone(note_id)

    def testAddValidNote(self):
        note_id = self.tryAddNoteWithExcept(title="Select everything from table",
                                  body="SELECT * FROM X")
        self.assertExceptionNotRaised()
        self.assertNoteIdIsNotNone(note_id)

    def assertExceptionNotRaised(self):
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception: ({!r})"
                .format(self.param, self.receivedException)
        )

    def assertNoteIdIsNotNone(self, note_id):
        self.assertIsNotNone(note_id, "note_id is None")

    def testRetrieveNoteWithExactTitle(self):
        note = Note(title="Select everything from table", body="SELECT * FROM X")
        note.id = self.tryAddNoteWithExcept(note.title, note.body)
        self.assertExceptionNotRaised()
        results = self.noteMan.search(note.title)
        self.assertNoteInList(note, results)
        self.assertNoteIdsEqual(note, self.__get_note_by_title(note.title, results))

    def assertNoteInList(self, note, results):
        self.assertTrue(
            self.__note_title_is_in_results(note.title, results),
            "Param: {}. Expected Title ({}) not in result set"
                .format(self.param, note.title)
        )
        result_note = self.__get_note_by_title(note.title, results)
        self.assertEqual(
            note.body,
            result_note.body,
            "Param: {}. Note Body does not match Expected result\nExpected: {}\nActual: {}"
                .format(self.param, note.body, result_note.body)
        )
        self.assertEqual(
            note.id,
            result_note.id,
            "Param: {}. Note ID does not match expected result: {}"
            .format(self.param, note.id)
        )

    def assertNoteIdsEqual(self, note, retreived_note):
        self.assertEqual(
            retreived_note.id,
            note.id,
            "Param: {}. note_id ({}) does not match result: ({})"
                .format(self.param, note.id, retreived_note.id)
        )

    def __note_title_is_in_results(self, note_title, results):
        return note_title in [n.title for n in results],

    def __get_note_by_title(self, note_title, results):
        notes = filter(lambda x: x.title == note_title, results)
        if len(notes) > 0:
            return notes[0]

    def testRetrieveNoteWithPartialTitle(self):
        note = Note(id=None, title="Select everything from table", body="SELECT * FROM X")
        note.id = self.tryAddNoteWithExcept(title=note.title, body=note.body)
        self.assertExceptionNotRaised()
        results = self.noteMan.search("Select")
        self.assertNoteInList(note, results)
        self.assertNoteIdsEqual(note, self.__get_note_by_title(note.title, results))

    def testRetrieveAllNotesWithPartialSearchParameter(self):
        notes = [
            Note(id=0, title="Select everything from table", body="SELECT * FROM X"),
            Note(id=0, title="Select one thing from table",  body="SELECT TOP 1 * FROM X")
        ]
        for k in notes:
            k.id = self.tryAddNoteWithExcept(title=k.title, body=k.body)
        self.assertExceptionNotRaised()
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes), len(results))
        for note in notes:
            self.assertNoteInList(note, results)
        self.assertEqual(len(results), len(notes))

    def testRetrieveSomeNotesWithPartialSearchParameter(self):
        non_match_note = Note(title="Nope, nope, nope", body="exec sp_MSforeachtable @command1 = \"DROP TABLE ?\"")
        notes = [
            non_match_note,
            Note(title="Select everything from table", body="SELECT * FROM X"),
            Note(title="Select one thing from table", body="SELECT TOP 1 * FROM X")
        ]
        for k in notes:
            k.id = self.tryAddNoteWithExcept(title=k.title, body=k.body)
        self.assertExceptionNotRaised()
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes) - 1, len(results))
        self.assertNoteNotInList(non_match_note, results)
        for note in results:
            self.assertNoteInList(note, notes)

    def assertNoteNotInList(self, note, list):
        for n in list:
            self.assertNotEqual(
                n,
                note,
                "Param: {}. Note should not be in result list, but is: \nID: {}\nTitle: {}\nBody: {}"
                .format(self.param, note.id, note.title, note.body)
            )

    def testAddDuplicateNoteTitle(self):
        note_title = "select everything"
        self.tryAddNoteWithExcept(note_title, "SELECT * FROM X", DuplicateEntryException)
        self.tryAddNoteWithExcept(note_title, "SELECT ... FROM X", DuplicateEntryException)
        self.assertExceptionRaised(DuplicateEntryException)

if __name__ == '__main__':
    unittest.main()
