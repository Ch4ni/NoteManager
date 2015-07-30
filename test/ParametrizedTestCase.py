import unittest


class ParametrizedTestCase(unittest.TestCase):
    def __init__(self, method_name="runTest", param=None):
        super(ParametrizedTestCase, self).__init__(method_name)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(testcase_klass(name, param=param))
        return suite


