import unittest
import tempfile

from test import ParametrizedTestCase
from NoteManagerTest import NoteManagerTest

suite = unittest.TestSuite()
suite.addTest(
    ParametrizedTestCase.parametrize(
        NoteManagerTest,
        param=("DictStorage", [], {})
    )
)
suite.addTest(
    ParametrizedTestCase.parametrize(
        NoteManagerTest,
        param=("FilesystemStorage", [], {"base_path": tempfile.mkdtemp()})
    )
)
unittest.TextTestRunner(verbosity=2).run(suite)
