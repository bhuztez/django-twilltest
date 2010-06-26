# copied from django.test.simple
import unittest
from django.db.models import get_app, get_apps
from django.test.simple import reorder_suite, DjangoTestSuiteRunner
from django.test.utils import setup_test_environment

TEST_MODULE = __package__ + 's'

def get_tests(app_module, TEST_MODULE=TEST_MODULE):
    try:
        app_path = 'test_'+'_'.join(app_module.__name__.split('.')[:-1])
        test_module = __import__(TEST_MODULE+'.'+app_path, {}, {}, app_path)
        return test_module
        
    except ImportError, e:
        import os.path
        from imp import find_module
        try:
            path = os.path.dirname(__import__(TEST_MODULE).__file__)
            mod = find_module(app_path, [path])
        except ImportError:
            test_module = None
        else:
            if mod[0]:
                mod[0].close()
            raise
    

def build_suite(app_module):
    suite = unittest.TestSuite()

    test_module = get_tests(app_module)
    if test_module:
        if hasattr(test_module, 'suite'):
            suite.addTest(test_module.suite())
        else:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_module))
    return suite


class TwillTestSuiteRunner(DjangoTestSuiteRunner):

    def setup_test_environment(self):
        setup_test_environment()
    
    def build_suite(self, test_labels, extra_tests=None):
        suite = unittest.TestSuite()
        
        if test_labels:
            for label in test_labels:
                app = get_app(label)
                suite.addTest(build_suite(app))
        else:
            for app in get_apps():
                suite.addTest(build_suite(app))
        
        return suite
    


def run_tests(test_labels, verbosity=1):
    test_runner = TwillTestSuiteRunner(verbosity=verbosity)
    return test_runner.run_tests(test_labels)




