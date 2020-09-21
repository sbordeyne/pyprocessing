import unittest


class ProcessingSketch:
    def setup(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()


class TestCase(unittest.TestCase):
    '''
    Base test case for PyProcessing
    '''

    def setUp(self):
        '''
        Set up testing environement

        Use the Tk renderer to test things out by default, since it's
        only using the standard library
        '''
