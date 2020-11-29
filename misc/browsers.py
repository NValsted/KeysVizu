from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty

class FileBrowser(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    filter_strings = ListProperty(['*'])
    initial_directory = StringProperty("/")

class ColorBrowser(FloatLayout):
    apply = ObjectProperty(None)
    cancel = ObjectProperty(None)