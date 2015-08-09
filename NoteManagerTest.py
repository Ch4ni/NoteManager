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
        note_id = None
        try:
            note_id = self.noteMan.add_note("", "")
        except EmptyNoteException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyNoteException was not thrown"
            .format(self.param)
        )
        self.assertIsNone(note_id, "note_id is not None: {}".format(note_id))

    def testAddEmptyTitleRaisesEmptyTitleException(self):
        note_id = None
        try:
            note_id = self.noteMan.add_note(body="SELECT * FROM SOMETABLE")
        except EmptyTitleException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyTitleException was not thrown"
            .format(self.param)
        )
        self.assertIsNone(note_id, "note_id is not None: {}".format(note_id))

    def testAddEmptyBodyRaisesEmptyBodyException(self):
        note_id = None
        try:
            note_id = self.noteMan.add_note(title="Blank Note")
        except EmptyBodyException:
            self.exceptionIsThrownByMethod = True
        self.assertTrue(
            self.exceptionIsThrownByMethod,
            "Param: {}. Expected EmptyBodyException was not thrown"
            .format(self.param)
        )
        self.assertIsNone(note_id, "note_id is not None: {}".format(note_id))

    def testAddValidNote(self):
        note_id = None
        try:
            note_id = self.noteMan.add_note("Select everything from table",
                                  "SELECT * FROM X")
        except Exception as e:
            self.exceptionIsThrownByMethod = True
            self.receivedException = e
        self.assertFalse(
            self.exceptionIsThrownByMethod,
            "Param: {}. Received unexpected Exception: ({!r})"
            .format(self.param, self.receivedException)
        )
        self.assertIsNotNone(
                note_id,
                "Param: {}. note_id is None"
                .format(self.param)
        )

    def testRetrieveNoteWithExactTitle(self):
        note_title = "Select everything from table"
        note_body = "SELECT * FROM X"
        note_id = None
        try:
            note_id = self.noteMan.add_note(note_title, note_body)
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
            self.__note_title_is_in_results(note_title, results),
            "Param: {}. Expected Title not in result set"
            .format(self.param)
        )
        self.assertEqual(
            self.__get_note_body_by_title(note_title, results),
            note_body,
            "Param: {}. Note Body does not match Expected result"
            .format(self.param)
        )
        retreived_note = self.__get_note_by_title(note_title, results)
        self.assertEqual(
            retreived_note.id,
            note_id,
            "Param: {}. note_id ({}) does not match result: ({})"
            .format(self.param, note_id, retreived_note.id)
        )

    def __note_title_is_in_results(self, note_title, results):
        return note_title in [n.title for n in results],

    def __get_note_body_by_title(self, note_title, results):
        return self.__get_note_by_title(note_title, results).body

    def __get_note_by_title(self, note_title, results):
        notes = filter(lambda x: x.title == note_title, results)
        if len(notes) > 0:
            return notes[0]

    def testRetrieveNoteWithPartialTitle(self):
        note_title = "Select everything from table"
        note_body = "SELECT * FROM X"
        note_id = None
        try:
            note_id = self.noteMan.add_note(note_title, note_body)
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
            self.__note_title_is_in_results(note_title, results),
            "Param: {}. Expected Title not in result set"
            .format(self.param)
        )
        result_note = self.__get_note_by_title(note_title, results)
        self.assertEqual(
            result_note.body,
            note_body,
            "Param: {}. Note Body does not match Expected result"
            .format(self.param)
        )
        self.assertEqual(
            result_note.id,
            note_id,
            "Param: {}. note_id ({}) does not match result: ({})"
            .format(self.param, note_id, result_note.id)
        )

    def testRetrieveAllNotesWithPartialSearchParameter(self):
        notes = {
            "Select everything from table": "SELECT * FROM X",
            "Select one thing from table": "SELECT TOP 1 * FROM X"
        }
        note_ids = []
        try:
            for k in notes:
                note_ids.append(self.noteMan.add_note(k, notes[k]))
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
        for note_title in notes:
            self.assertTrue(
                self.__note_title_is_in_results(note_title, results),
                "Param: {}. Expected Title ({}) not in result set"
                .format(self.param, k)
            )
            note_body = self.__get_note_body_by_title(note_title, results)
            self.assertEqual(
                note_body,
                notes[note_title],
                "Param: {}. Note Body ({}) does not match expected result: {}"
                .format(self.param, notes[note_title], note_title, note_body, results)
            )
        self.assertEqual(len(results), len(note_ids))
        for note in results:
            self.assertTrue(
                note.id in note_ids,
                "Param: {}. note_id ({}) not present in note_ids: ({})"
                .format(self.param, note.id, note_ids)
            )

    def testRetrieveSomeNotesWithPartialSearchParameter(self):
        non_match_title = "Nope, nope, nope"
        notes = {
            "Select everything from table": "SELECT * FROM X",
            "Select one thing from table": "SELECT TOP 1 * FROM X",
            non_match_title:
                "exec sp_MSforeachtable @command1 = \"DROP TABLE ?\""
        }
        note_ids = []
        try:
            for k in notes:
                note_ids.append(self.noteMan.add_note(k, notes[k]))
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
        for note in results:
            self.assertTrue(
                self.__note_title_is_in_results(note, results),
                "Param: {}. Expected Title ({}) not in result set"
                .format(self.param, note)
            )
            self.assertEqual(
                notes[note.title],
                note.body,
                "Param: {}. Note Body ({}) does not match expected result: {}"
                .format(self.param, note.body, notes[note.title])
            )
            self.assertTrue(note.id in note_ids)

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
