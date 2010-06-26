import unittest
from twill import add_wsgi_intercept, remove_wsgi_intercept

from django.conf import settings
from django.core.management import call_command
from django.core.servers.basehttp import AdminMediaHandler
from django.core.handlers.wsgi import WSGIHandler
from django.core.urlresolvers import clear_url_caches
from django.db import transaction, connections, DEFAULT_DB_ALIAS
from django.test.testcases import (
    connections_support_transactions,
    disable_transaction_methods,
    restore_transaction_methods
    )


from .client import Client, hook_twill_command


class TestCase(unittest.TestCase):
     
    domain = "127.0.0.1"
    port = 8080
    hook = True
    
    _Client = Client

    def _pre_setup(self):
        app = AdminMediaHandler(WSGIHandler())
        add_wsgi_intercept(self.domain, self.port, lambda: app)

        prefix = "http://%s:%d"%(self.domain,self.port)

        self.client = self._Client(self.hook and prefix or '', getattr(self, 'url', None))
        self.client.reset_browser()

        hook_twill_command('go', self.client.go)
        hook_twill_command('url', self.client.url)
        
        self._fixture_setup()
        self._urlconf_setup()
        
    
    def _post_teardown(self):
    
        self._urlconf_teardown()
        self._fixture_teardown()
        remove_wsgi_intercept(self.domain, self.port)


    def _fixture_setup(self):
        if not connections_support_transactions():
            raise

        # If the test case has a multi_db=True flag, setup all databases.
        # Otherwise, just use default.
        if getattr(self, 'multi_db', False):
            databases = connections
        else:
            databases = [DEFAULT_DB_ALIAS]

        for db in databases:
            transaction.enter_transaction_management(using=db)
            transaction.managed(True, using=db)
        disable_transaction_methods()

        from django.contrib.sites.models import Site
        Site.objects.clear_cache()

        

        for db in databases:
            if hasattr(self, 'fixtures'):
                fixtures = [ __package__+'_'+fixture for fixture in self.fixtures]
                call_command('loaddata', *fixtures, **{
                                                            'verbosity': 1,
                                                            'commit': False,
                                                            'database': db
                                                            })

    def _fixture_teardown(self):
        if not connections_support_transactions():
            raise

        # If the test case has a multi_db=True flag, teardown all databases.
        # Otherwise, just teardown default.
        if getattr(self, 'multi_db', False):
            databases = connections
        else:
            databases = [DEFAULT_DB_ALIAS]

        restore_transaction_methods()
        for db in databases:
            transaction.rollback(using=db)
            transaction.leave_transaction_management(using=db)

        for connection in connections.all():
            connection.close()

    def _urlconf_setup(self):
        if hasattr(self, 'urls'):
            self._old_root_urlconf = settings.ROOT_URLCONF
            settings.ROOT_URLCONF = self.urls
            clear_url_caches()

    def _urlconf_teardown(self):
        if hasattr(self, '_old_root_urlconf'):
            settings.ROOT_URLCONF = self._old_root_urlconf
            clear_url_caches()

    def __call__(self, result=None):
        if result is None: result = self.defaultTestResult()
        
        result.startTest(self)
        testMethod = getattr(self, self._testMethodName)
        
        try:
            try:
                self._pre_setup()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                import sys
                result.addError(self, sys.exc_info())
                return


            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                return

            ok = False

            try:
                testMethod()
                ok = True
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())

            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                ok = False
            
            try:
                self._post_teardown()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                import sys
                result.addError(self, sys.exc_info())
                ok = False
            
            if ok: result.addSuccess(self) 
        
        finally:
            result.stopTest(self)


