from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty

class FileBrowser(FloatLayout):
    cancel = ObjectProperty(None)
    filter_strings = ListProperty(['*'])
    initial_directory = StringProperty("/")
    filechooser = ObjectProperty(None)

    def selection_path_feedback(self, *args):
        pass

class LoadDialog(FileBrowser):
    load = ObjectProperty(None)

class SaveDialog(FileBrowser):
    save = ObjectProperty(None)
    path_input = ObjectProperty(None)

    def selection_path_feedback(self,selection):
        self.path_input.text = selection and selection[0] or ''

class ColorBrowser(FloatLayout):
    apply = ObjectProperty(None)
    cancel = ObjectProperty(None)