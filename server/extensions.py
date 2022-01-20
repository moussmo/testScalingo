from extension_model import Extension

extension1 = Extension('myExtension').addCalendar(name='calendar')\
    .addInternship(name='Stages')\
    .addInternship(name='Fiche de stage vide', content='new')
extension2 = Extension('myExtension2').addCalendar(name='calendar').addInternship(name='Stages')

extensions_list = [extension1, extension2]