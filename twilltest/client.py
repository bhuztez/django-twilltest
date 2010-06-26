from twill import commands as c
from twill import execute_string


# dirty hack
from twill.namespaces import global_dict

def hook_twill_command(command, func):
     global_dict[command] = func
   

class Client:
    
    def __init__(self, prefix, default_url=None):
        self.prefix = prefix
        self.default_url = default_url
    
    def go(self, url=None):
        url = url or self.default_url
        if not url.startswith('http://'):
            url = self.prefix+url
        return c.go(url)

    def url(self, should_be=None):
        should_be = should_be or self.default_url
        if not should_be.startswith('http://'):
            should_be = self.prefix+should_be
        return c.url(should_be)
    

    execute = staticmethod(execute_string)
    
    
    get_browser = staticmethod(c.get_browser)
    reset_browser = staticmethod(c.reset_browser)
    extend_with = staticmethod(c.extend_with)
    exit = staticmethod(c.exit)
    reload = staticmethod(c.reload)
    code = staticmethod(c.code)
    follow = staticmethod(c.follow)
    find = staticmethod(c.find)
    notfind = staticmethod(c.notfind)
    back = staticmethod(c.back)
    show = staticmethod(c.show)
    echo = staticmethod(c.echo)
    save_html = staticmethod(c.save_html)
    sleep = staticmethod(c.sleep)
    agent = staticmethod(c.agent)
    showforms = staticmethod(c.showforms)
    showlinks = staticmethod(c.showlinks)
    showhistory = staticmethod(c.showhistory)
    submit = staticmethod(c.submit)
    formvalue = staticmethod(c.formvalue)
    fv = staticmethod(c.fv)
    formaction = staticmethod(c.formaction)
    fa = staticmethod(c.fa)
    formclear = staticmethod(c.formclear)
    formfile = staticmethod(c.formfile)
    getinput = staticmethod(c.getinput)
    getpassword = staticmethod(c.getpassword)
    save_cookies = staticmethod(c.save_cookies)
    load_cookies = staticmethod(c.load_cookies)
    clear_cookies = staticmethod(c.clear_cookies)
    show_cookies = staticmethod(c.show_cookies)
    add_auth = staticmethod(c.add_auth)
    run = staticmethod(c.run)
    runfile = staticmethod(c.runfile)
    setglobal = staticmethod(c.setglobal)
    setlocal = staticmethod(c.setlocal)
    debug = staticmethod(c.debug)
    title = staticmethod(c.title)
    exit = staticmethod(c.exit)
    config = staticmethod(c.config)
    tidy_ok = staticmethod(c.tidy_ok)
    redirect_output = staticmethod(c.redirect_output)
    reset_output = staticmethod(c.reset_output)
    redirect_error = staticmethod(c.redirect_error)
    reset_error = staticmethod(c.reset_error)
    add_extra_header = staticmethod(c.add_extra_header)
    show_extra_headers = staticmethod(c.show_extra_headers)
    clear_extra_headers = staticmethod(c.clear_extra_headers)
    info = staticmethod(c.info)


