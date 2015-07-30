import unittest

class ParameterizedTestCase(unittest.TestCase):
    def __init__(self, methodName="runTest", param=None):
        super(ParameterizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcaseKlass, param=None):
        testLoader = unittest.TestLoader()
        testNames = testLoader.getTestCaseNames(testcaseKlass)
        suite = unittest.TestSuite()
        for name in testNames:
            suite.addTest(testcaseKlass(name, param=param))
        return suite


