
class Tab:
    def __init__(self, tab_type):
        self.tab_type = tab_type
        self.tab_name = tab_type
        self.content = 'default'

    def set_name(self, name):
        self.tab_name = name

    def set_content(self, content):
        self.content = content

class Extension:
    def __init__(self, extension_name, tabs=None):
        self.extension_name = extension_name
        if tabs is None:
            self.tabs = []
        else:
            self.tabs = tabs

    def addCalendar(self, **kwargs):
        tab = Tab('Calendar')

        if 'name' in kwargs:
            tab.set_name(kwargs['name'])

        tabs = self.tabs + [tab]
        return Extension(self.extension_name, tabs)

    def addInternship(self, **kwargs):
        tab = Tab('Internship')

        if 'name' in kwargs:
            tab.set_name(kwargs['name'])

        if 'content' in kwargs:
            tab.set_content(kwargs['content'])

        tabs = self.tabs + [tab]
        return Extension(self.extension_name, tabs)

if __name__=='__main__':
    extensions = []



