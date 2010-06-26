from django.contrib.auth import authenticate
from django.db.models import get_app
import django.test

from . import TestCase
from .decorators import twill_script
from .simple import get_tests

class TestLoaderTestCase(django.test.TestCase):

    def testImportError(self):
        app = get_app(__package__)
        self.assertRaises(ImportError, get_tests, app, __package__)
        

class FixtureTestCaseA(TestCase):

    fixtures = ['twilltest_fixturea']
    
    def testSuccessA(self):
        user = authenticate(username='a', password='a')
        self.failIf(user is None)
    

    def testFailureB(self):
        user = authenticate(username='b', password='b')
        self.assertTrue(user is None)

class FixtureTestCaseB(TestCase):

    fixtures = ['twilltest_fixtureb']

    def testSuccessB(self):
        user = authenticate(username='b', password='b')
        self.failIf(user is None)
    

    def testFailureA(self):
        user = authenticate(username='a', password='a')
        self.assertTrue(user is None)


class HookTestCase(TestCase):
    
    urls = __package__ + '.urls'

    def testClient(self):
        self.client.go('/')
        self.client.code(200)
        self.client.url('/')
        self.client.find('OK')
    
    def testClientExecute(self):
        self.client.execute('''
go /
code 200
url /
find OK ''')
    
    @twill_script
    def testScript(self):
        return '''
go /
code 200
url /
find OK '''

    
class DefaultURLTestCase(TestCase):

    urls = __package__ + '.urls'
    url = '/'

    def testClient(self):
        self.client.go()
        self.client.code(200)
        self.client.url()
        self.client.find('OK')
    
    def testClientExecute(self):
        self.client.execute('''
go
code 200
url
find OK ''')
    
    @twill_script
    def testScript(self):
        return '''
go
code 200
url
find OK '''


try:
    from _mechanize_dist._mechanize import BrowserStateError
except ImportError:
    from mechanize import BrowserStateError
    

class NoHookTestCase(TestCase):
    
    urls = __package__ + '.urls'
    hook = False

    def testClient(self):        
        self.assertRaises(BrowserStateError, self.client.go, '/')

    def testClientExecute(self):
        self.assertRaises(BrowserStateError, self.client.execute, 'go /')
        
    @twill_script
    def _testScript(self):
        return '''go /'''
        
    def testScript(self):
        self.assertRaises(BrowserStateError, self._testScript)
    




