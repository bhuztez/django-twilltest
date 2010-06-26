from StringIO import StringIO
from inspect import getsourcefile, getsourcelines

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps

from twill.parse import _execute_script


def execute_string(buf, view):
    fp = StringIO(buf)
    f = getsourcefile(view)
    lineno = getsourcelines(view)[1]
    source = "%s:%d %s"%(f, lineno, view.__name__)
    
    return _execute_script(fp, source=source, no_reset=True)
    

def twill_script(view):
    
    @wraps(view)
    def wrapper(self, *args, **kwargs):        
        response = view(self, *args, **kwargs)
                
        if isinstance(response, basestring):
            response = execute_string(response, view)
        
        return response
    
    return wrapper
        
