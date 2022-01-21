from extension_model import Extension

extension1 = Extension('myExtension').addCalendar(name='calendar').addInternship(name='Stages')\
    .addInternship(name='Fiche de stage vide', content='new')

extension2 = Extension('myExtension2').addInternship(name='Stages').addInternship(name="Creation de fiche", content ="new")\
    .addCalendar(name='Calendrier', color = "Red").addContactsBook(name="Annuaire")

extension3 = Extension('myExtension3').addBugReport().addProfile(name = "Fiche de compétence", content="Compétences")\
    .addCalendar()

extensions_list = [extension1, extension2, extension3]