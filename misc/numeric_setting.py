from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty

class NumericSliderSetting(BoxLayout):
    label_text = StringProperty(" ")
    slider = ObjectProperty(None)
    
    step = NumericProperty(0.1)
    slider_bounds = ListProperty([0,1])

    callback = lambda *args : None
