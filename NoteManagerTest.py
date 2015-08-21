__author__ = 'acripps'

import unittest

from NoteManager import *
from test import ParametrizedTestCase


class NoteManagerTest(ParametrizedTestCase):
    def setUp(self):
        self.noteMan = NoteManager(self.param[0], *self.param[1], **self.param[2])
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
        note_id = self.tryAddNoteWithExcept(Note("", ""), EmptyNoteException)
        self.assertExceptionRaised(EmptyNoteException)
        self.assertNoteIdIsNone(note_id)

    def tryAddNoteWithExcept(self, note=None, exception=Exception):
        try:
            return self.noteMan.add_note(note)
        except exception as e:
            self.receivedException = e

    def assertExceptionRaised(self, exception_type):
        self.assertIsNotNone(
            self.receivedException,
            "Param: {}. Expected {!r} was not thrown"
                .format(self.param, exception_type)
        )

    def assertNoteIdIsNone(self, note_id):
        self.assertIsNone(note_id, "note_id is not None: {}".format(note_id))

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        note_id = self.tryAddNoteWithExcept(Note(body="SELECT * FROM SOMETABLE"), exception=EmptyTitleException)
        self.assertExceptionRaised(EmptyTitleException)
        self.assertNoteIdIsNone(note_id)

    def testAddEmptyBodyRaisesEmptyBodyException(self):
        note_id = self.tryAddNoteWithExcept(Note("Blank Note", ""), EmptyBodyException)
        self.assertExceptionRaised(EmptyBodyException)
        self.assertNoteIdIsNone(note_id)

    def testAddValidNote(self):
        note_id = self.tryAddNoteWithExcept(Note("Select everything from table",
                                  "SELECT * FROM X"))
        self.assertExceptionNotRaised()
        self.assertNoteIdIsNotNone(note_id)

    def assertExceptionNotRaised(self):
        self.assertIsNone(
            self.receivedException,
            "Param: {}. Received unexpected Exception: ({!r})"
                .format(self.param, self.receivedException)
        )

    def assertNoteIdIsNotNone(self, note_id):
        self.assertIsNotNone(note_id, "note_id is None")

    def testRetrieveNoteWithExactTitle(self):
        note = Note(title="Select everything from table", body="SELECT * FROM X")
        note.id = self.tryAddNoteWithExcept(note)
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
        note = Note(title="Select everything from table", body="SELECT * FROM X")
        note.id = self.tryAddNoteWithExcept(note)
        self.assertExceptionNotRaised()
        results = self.noteMan.search("Select")
        self.assertNoteInList(note, results)
        self.assertNoteIdsEqual(note, self.__get_note_by_title(note.title, results))

    def testRetrieveAllNotesWithPartialSearchParameter(self):
        notes = [
            Note(title="Select everything from table", body="SELECT * FROM X"),
            Note(title="Select one thing from table",  body="SELECT TOP 1 * FROM X")
        ]
        for note in notes:
            note.id = self.tryAddNoteWithExcept(note)
        self.assertExceptionNotRaised()
        results = self.noteMan.search("Select")
        self.assertEqual(len(notes), len(results))
        for note in notes:
            self.assertNoteInList(note, results)
        self.assertEqual(len(results), len(notes))

    def testRetrieveSomeNotesWithPartialSearchParameter(self):
        non_match_note = Note("Nope, nope, nope", "exec sp_MSforeachtable @command1 = \"DROP TABLE ?\"")
        notes = [
            non_match_note,
            Note("Select everything from table", "SELECT * FROM X"),
            Note("Select one thing from table", "SELECT TOP 1 * FROM X")
        ]
        for note in notes:
            note.id = self.tryAddNoteWithExcept(note)
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
        self.tryAddNoteWithExcept(Note(note_title, "SELECT * FROM X"), DuplicateEntryException)
        self.tryAddNoteWithExcept(Note(note_title, "SELECT ... FROM X"), DuplicateEntryException)
        self.assertExceptionRaised(DuplicateEntryException)

    def testRemoveNoteById(self):
        note = Note(title="Select everything from table", body="SELECT * FROM X")
        note.id = self.tryAddNoteWithExcept(note)
        self.assertExceptionNotRaised()
        self.noteMan.delete_note(id = note.id)
        results = self.noteMan.search(note.title.split(" ")[0])
        self.assertEqual(
                0,
                len(results),
                "Param: {}. Result list should be empty, but is not."
                .format(self.param)
        )


if __name__ == '__main__':
    unittest.main()
