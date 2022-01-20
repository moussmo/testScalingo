class Tab:
    def __init__(self, tab_type):
        self.tab_type = tab_type
        self.tab_name = tab_type
        self.content = 'default'

    def set_route(self):
        if self.tab_type == 'calendar':
            self.route = '/calendar'
        elif self.tab_type == 'internship':
            if self.content == 'new':
                self.route = '/internships/new'
            else:
                self.route = '/internships'
        else:
            self.route = '/base_extension'

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
        tab = Tab('calendar')

        if 'name' in kwargs:
            tab.set_name(kwargs['name'])

        tab.set_route()
        tabs = self.tabs + [tab]
        return Extension(self.extension_name, tabs)

    def addInternship(self, **kwargs):
        tab = Tab('internship')
        if 'name' in kwargs:
            tab.set_name(kwargs['name'])
        else:
            tab.set_name('Tab '+ str(len(self.tabs)))

        if 'content' in kwargs:
            tab.set_content(kwargs['content'])

        tab.set_route()
        tabs = self.tabs + [tab]
        return Extension(self.extension_name, tabs)




